#!/usr/bin/env python3
"""Disposable on-chain mint timing probe. Not production code.

Goals:
- detect recent ERC-721 / ERC-1155 mint logs with range eth_getLogs calls;
- detect and subdivide exactly-1,000-log responses so Robinhood truncation is visible;
- estimate deploy-to-first-mint timing without Trace/Debug APIs;
- emit one bounded JSON measurement object and fail soft per chain.
"""

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

USER_AGENT = "nft-mint-radar-onchain-spike/0.1"

ZERO_TOPIC = "0x" + ("0" * 64)


def _assert_topic(name: str, value: str) -> str:
    """A malformed topic silently matches nothing, which reads as 'no mints found'.

    Two of these constants were wrong when this probe was first written - one had a
    hallucinated tail, one was 63 hex characters instead of 64 - which would have made
    every ERC-1155 mint invisible and produced a confident, false 'on-chain is thin'
    result. Fail loudly at import instead.
    """
    if not (value.startswith("0x") and len(value) == 66):
        raise ValueError(f"{name} must be 0x + 64 hex chars, got {len(value) - 2}: {value}")
    int(value, 16)
    return value

ERC721_TRANSFER_TOPIC0 = _assert_topic("ERC721_TRANSFER_TOPIC0", "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef")
ERC1155_TRANSFER_SINGLE_TOPIC0 = _assert_topic("ERC1155_TRANSFER_SINGLE_TOPIC0", "0xc3d58168c5ae7397731d063d5bbf3d657854427343f4c083240f7aacaa2d0f62")
ERC1155_TRANSFER_BATCH_TOPIC0 = _assert_topic("ERC1155_TRANSFER_BATCH_TOPIC0", "0x4a39dc06d4c0dbc64b70af90fd698a233a518aa5d07e595d983b8c0526c8f7fb")

CHAINS = {
    "ethereum": {
        "name": "ethereum",
        "chain_id": 1,
        "rpc_url": "https://ethereum.publicnode.com",
        "approx_block_time_seconds": 12.0,
        "explorer_api_url": None,
    },
    "base": {
        "name": "base",
        "chain_id": 8453,
        "rpc_url": "https://mainnet.base.org",
        "approx_block_time_seconds": 2.0,
        "explorer_api_url": "https://base.blockscout.com/api",
    },
    "robinhood": {
        "name": "robinhood",
        "chain_id": 4663,
        "rpc_url": "https://rpc.mainnet.chain.robinhood.com",
        "approx_block_time_seconds": 0.1,
        "explorer_api_url": "https://explorer.mainnet.chain.robinhood.com/api",
    },
}

CHAIN_ALIASES = {
    "eth": "ethereum",
    "ethereum": "ethereum",
    "mainnet": "ethereum",
    "base": "base",
    "base-mainnet": "base",
    "robinhood": "robinhood",
    "robinhood-chain": "robinhood",
    "hood": "robinhood",
}

LOG_QUERIES = [
    {
        "name": "erc721_transfer_mint",
        "standard": "erc721",
        "topics": [ERC721_TRANSFER_TOPIC0, ZERO_TOPIC],
    },
    {
        "name": "erc1155_transfer_single_mint",
        "standard": "erc1155",
        "topics": [ERC1155_TRANSFER_SINGLE_TOPIC0, None, ZERO_TOPIC],
    },
    {
        "name": "erc1155_transfer_batch_mint",
        "standard": "erc1155",
        "topics": [ERC1155_TRANSFER_BATCH_TOPIC0, None, ZERO_TOPIC],
    },
]


class RpcBudgetExceeded(Exception):
    pass


class JsonRpcError(Exception):
    def __init__(self, message, code=None, http_status=None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.http_status = http_status


class RpcBudget:
    def __init__(self, limit):
        self.limit = max(1, int(limit))
        self.used = 0

    @property
    def remaining(self):
        return max(0, self.limit - self.used)

    def consume(self):
        if self.used >= self.limit:
            raise RpcBudgetExceeded(f"hard RPC call cap reached ({self.limit})")
        self.used += 1


class RpcClient:
    def __init__(self, url, budget):
        self.url = url
        self.budget = budget
        self.method_counts = {}

    def call(self, method, params):
        self.budget.consume()
        self.method_counts[method] = self.method_counts.get(method, 0) + 1
        payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode("utf-8")
        req = urllib.request.Request(
            self.url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": USER_AGENT,
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                body = json.load(resp)
        except urllib.error.HTTPError as exc:
            text = exc.read(1000).decode("utf-8", "replace")
            raise JsonRpcError(summarize_error_text(text) or f"HTTP {exc.code}", http_status=exc.code)
        except Exception as exc:
            raise JsonRpcError(f"{type(exc).__name__}: {exc}")
        if not isinstance(body, dict):
            raise JsonRpcError(f"malformed JSON-RPC response type {type(body).__name__}")
        if body.get("error"):
            err = body["error"]
            if isinstance(err, dict):
                raise JsonRpcError(str(err.get("message") or "JSON-RPC error"), code=err.get("code"))
            raise JsonRpcError(str(err))
        return body.get("result")


def summarize_error_text(text):
    if not text:
        return ""
    text = " ".join(text.split())
    return text[:300]


def hex_to_int(value):
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        return int(value, 16) if value.startswith("0x") else int(value)
    raise ValueError(f"cannot parse integer from {type(value).__name__}")


def int_to_hex(value):
    return hex(int(value))


def normalize_address(value):
    return str(value or "").lower()


def log_sort_key(log):
    return (
        hex_to_int(log.get("blockNumber", "0x0")),
        hex_to_int(log.get("transactionIndex", "0x0")),
        hex_to_int(log.get("logIndex", "0x0")),
    )


def looks_like_range_error(error):
    text = (getattr(error, "message", "") or str(error)).lower()
    needles = ("more than", "too many", "limit", "range", "response size", "query returned")
    return any(needle in text for needle in needles)


def looks_like_auth_error(error):
    text = (getattr(error, "message", "") or str(error)).lower()
    if getattr(error, "http_status", None) in (401, 403):
        return True
    needles = ("api key", "apikey", "unauthorized", "forbidden", "authentication", "auth")
    return any(needle in text for needle in needles)


def split_range(start_block, end_block):
    mid = (start_block + end_block) // 2
    return (start_block, mid), (mid + 1, end_block)


def get_logs_range(rpc, base_filter, start_block, end_block):
    logs = []
    stats = {
        "truncation_count": 0,
        "truncation_unresolved_count": 0,
        "range_error_subdivision_count": 0,
        "unresolved_ranges": [],
        "warnings": [],
    }
    stack = [(start_block, end_block)]
    complete = True
    while stack:
        start, end = stack.pop()
        query_filter = dict(base_filter)
        query_filter["fromBlock"] = int_to_hex(start)
        query_filter["toBlock"] = int_to_hex(end)
        try:
            result = rpc.call("eth_getLogs", [query_filter])
        except JsonRpcError as exc:
            if start < end and looks_like_range_error(exc):
                stats["range_error_subdivision_count"] += 1
                left, right = split_range(start, end)
                stack.append(right)
                stack.append(left)
                continue
            if looks_like_auth_error(exc):
                raise JsonRpcError(f"eth_getLogs rejected by public RPC without usable unauthenticated access: {exc.message}", code=exc.code, http_status=exc.http_status)
            raise
        if not isinstance(result, list):
            raise JsonRpcError(f"eth_getLogs returned {type(result).__name__}, expected list")
        if len(result) == 1000:
            stats["truncation_count"] += 1
            if start == end:
                complete = False
                logs.extend(result)
                stats["truncation_unresolved_count"] += 1
                stats["unresolved_ranges"].append({"from_block": start, "to_block": end, "returned_logs": len(result)})
                stats["warnings"].append("EXACTLY_1000_LOGS_IN_ONE_BLOCK_CANNOT_BE_SUBDIVIDED_RESULTS_MAY_BE_TRUNCATED")
                continue
            left, right = split_range(start, end)
            stack.append(right)
            stack.append(left)
            continue
        logs.extend(result)
    if stats["truncation_count"] >= 5:
        stats["warnings"].append("HIGH_TRUNCATION_COUNT_WINDOW_IS_TOO_WIDE_FOR_THIS_CHAIN")
    elif stats["truncation_count"] > 0:
        stats["warnings"].append("TRUNCATION_DETECTED_AND_SUBDIVIDED")
    return logs, stats, complete


def get_block_timestamp(rpc, block_number, cache):
    if block_number in cache:
        return cache[block_number]
    block = rpc.call("eth_getBlockByNumber", [int_to_hex(block_number), False])
    if not isinstance(block, dict) or not block.get("timestamp"):
        raise JsonRpcError(f"missing block timestamp for block {block_number}")
    timestamp = hex_to_int(block["timestamp"])
    cache[block_number] = timestamp
    return timestamp


def fetch_recent_mints(chain, rpc, max_blocks):
    latest = hex_to_int(rpc.call("eth_blockNumber", []))
    start = max(0, latest - max_blocks + 1)
    end = latest
    timestamp_cache = {}
    start_timestamp = get_block_timestamp(rpc, start, timestamp_cache)
    end_timestamp = get_block_timestamp(rpc, end, timestamp_cache)

    contracts = {}
    total_events_by_query = {}
    total_events_by_standard = {}
    truncation_count = 0
    truncation_unresolved_count = 0
    range_error_subdivision_count = 0
    complete = True
    warnings = []
    unresolved_ranges = []

    for log_query in LOG_QUERIES:
        base_filter = {"topics": log_query["topics"]}
        query_logs, query_stats, query_complete = get_logs_range(rpc, base_filter, start, end)
        complete = complete and query_complete
        count = len(query_logs)
        total_events_by_query[log_query["name"]] = count
        total_events_by_standard[log_query["standard"]] = total_events_by_standard.get(log_query["standard"], 0) + count
        truncation_count += query_stats["truncation_count"]
        truncation_unresolved_count += query_stats["truncation_unresolved_count"]
        range_error_subdivision_count += query_stats["range_error_subdivision_count"]
        warnings.extend(query_stats["warnings"])
        unresolved_ranges.extend(query_stats["unresolved_ranges"])
        for row in query_logs:
            address = normalize_address(row.get("address"))
            if not address:
                continue
            block_number = hex_to_int(row.get("blockNumber", "0x0"))
            event = {
                "address": address,
                "standard": log_query["standard"],
                "first_mint_block": block_number,
                "first_mint_tx_hash": row.get("transactionHash"),
                "first_mint_log_index": hex_to_int(row.get("logIndex", "0x0")),
                "sort_key": log_sort_key(row),
            }
            existing = contracts.get(address)
            if existing is None or event["sort_key"] < existing["sort_key"]:
                contracts[address] = event

    ordered_contracts = sorted(contracts.values(), key=lambda item: item["sort_key"])
    for item in ordered_contracts:
        item.pop("sort_key", None)
        item["first_mint_timestamp"] = get_block_timestamp(rpc, item["first_mint_block"], timestamp_cache)

    warnings = list(dict.fromkeys(warnings))
    return {
        "latest_block": latest,
        "from_block": start,
        "to_block": end,
        "blocks_scanned": end - start + 1,
        "chain_time_span_seconds": max(0, end_timestamp - start_timestamp),
        "approx_block_time_seconds": chain["approx_block_time_seconds"],
        "distinct_minting_contracts_seen": len(ordered_contracts),
        "total_mint_events": sum(total_events_by_query.values()),
        "total_mint_events_by_query": total_events_by_query,
        "total_mint_events_by_standard": total_events_by_standard,
        "eth_getLogs_calls": rpc.method_counts.get("eth_getLogs", 0),
        "truncation_count": truncation_count,
        "truncation_unresolved_count": truncation_unresolved_count,
        "range_error_subdivision_count": range_error_subdivision_count,
        "complete": complete,
        "warnings": warnings,
        "unresolved_ranges": unresolved_ranges[:10],
        "contracts": ordered_contracts,
        "_timestamp_cache": timestamp_cache,
    }


def http_get_json(url, params):
    full_url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(full_url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = json.load(resp)
            return {"ok": True, "status": resp.status, "latency_ms": round((time.perf_counter() - started) * 1000, 1), "body": body}
    except urllib.error.HTTPError as exc:
        text = exc.read(1000).decode("utf-8", "replace")
        return {"ok": False, "status": exc.code, "latency_ms": round((time.perf_counter() - started) * 1000, 1), "error": summarize_error_text(text)}
    except Exception as exc:
        return {"ok": False, "status": None, "latency_ms": round((time.perf_counter() - started) * 1000, 1), "error": f"{type(exc).__name__}: {exc}"}


def parse_explorer_result(body, contract_address):
    if not isinstance(body, dict):
        return None, "explorer response was not an object"
    result = body.get("result")
    if isinstance(result, str):
        return None, result[:200]
    if isinstance(result, dict):
        rows = [result]
    elif isinstance(result, list):
        rows = result
    else:
        return None, "explorer response missing result rows"

    wanted = normalize_address(contract_address)
    for row in rows:
        if not isinstance(row, dict):
            continue
        row_address = normalize_address(row.get("contractAddress") or row.get("contract_address") or row.get("address"))
        if row_address and row_address != wanted:
            continue
        return row, None
    return None, "contract not present in explorer result"


def parse_optional_int(value):
    if value in (None, ""):
        return None
    try:
        return hex_to_int(value)
    except Exception:
        return None


def try_explorer_creation(chain, rpc, contract_address, timestamp_cache):
    api_url = chain.get("explorer_api_url")
    if not api_url:
        return None, {"source": "explorer", "ok": False, "reason": "no public Blockscout-style explorer API configured"}
    params = {
        "module": "contract",
        "action": "getcontractcreation",
        "contractaddresses": contract_address,
    }
    response = http_get_json(api_url, params)
    if not response["ok"]:
        return None, {
            "source": "explorer",
            "ok": False,
            "status": response.get("status"),
            "latency_ms": response.get("latency_ms"),
            "reason": response.get("error") or "request failed",
        }
    row, reason = parse_explorer_result(response.get("body"), contract_address)
    if not row:
        return None, {"source": "explorer", "ok": False, "status": response.get("status"), "latency_ms": response.get("latency_ms"), "reason": reason}

    block_number = parse_optional_int(row.get("blockNumber") or row.get("block_number") or row.get("block"))
    timestamp = parse_optional_int(row.get("timestamp") or row.get("timeStamp") or row.get("createdAtBlockTimestamp"))
    tx_hash = row.get("txHash") or row.get("transactionHash") or row.get("tx_hash")

    if block_number is None and tx_hash:
        receipt = rpc.call("eth_getTransactionReceipt", [tx_hash])
        if isinstance(receipt, dict) and receipt.get("blockNumber"):
            block_number = hex_to_int(receipt["blockNumber"])
    if block_number is None:
        return None, {"source": "explorer", "ok": False, "status": response.get("status"), "latency_ms": response.get("latency_ms"), "reason": "explorer result lacked block number and usable tx hash"}
    if timestamp is None:
        timestamp = get_block_timestamp(rpc, block_number, timestamp_cache)
    return {
        "creation_block": block_number,
        "creation_timestamp": timestamp,
        "creation_tx_hash": tx_hash,
        "creation_source": "blockscout_getcontractcreation",
    }, {"source": "explorer", "ok": True, "status": response.get("status"), "latency_ms": response.get("latency_ms")}


def code_exists_at(rpc, address, block_number):
    code = rpc.call("eth_getCode", [address, int_to_hex(block_number)])
    return isinstance(code, str) and code not in ("", "0x", "0x0")


def find_creation_by_code_search(rpc, address, first_mint_block, timestamp_cache):
    if first_mint_block < 0:
        return None, "invalid first mint block"
    if not code_exists_at(rpc, address, first_mint_block):
        return None, "no code at first mint block"
    low = 0
    high = first_mint_block
    while low < high:
        mid = (low + high) // 2
        if code_exists_at(rpc, address, mid):
            high = mid
        else:
            low = mid + 1
    timestamp = get_block_timestamp(rpc, high, timestamp_cache)
    return {
        "creation_block": high,
        "creation_timestamp": timestamp,
        "creation_tx_hash": None,
        "creation_source": "eth_getCode_binary_search",
    }, None


def estimate_creation_search_rpc_calls(first_mint_block):
    return max(1, int(first_mint_block).bit_length()) + 2


def timing_distribution(values):
    if not values:
        return {"min": None, "median": None, "p90": None, "max": None}
    ordered = sorted(values)
    count = len(ordered)
    mid = count // 2
    if count % 2:
        median = ordered[mid]
    else:
        median = (ordered[mid - 1] + ordered[mid]) / 2
    p90_index = max(0, min(count - 1, ((9 * count + 9) // 10) - 1))
    return {"min": ordered[0], "median": median, "p90": ordered[p90_index], "max": ordered[-1]}


def run_timing(chain, rpc, contracts, max_contracts, timestamp_cache):
    selected = contracts[:max(0, max_contracts)]
    rows = []
    known_seconds = []
    unknown_count = 0
    warnings = []
    stopped_reason = None
    for contract in selected:
        address = contract["address"]
        first_mint_block = contract["first_mint_block"]
        first_mint_timestamp = contract["first_mint_timestamp"]
        row = {
            "address": address,
            "standard": contract.get("standard"),
            "first_mint_block": first_mint_block,
            "first_mint_timestamp": first_mint_timestamp,
            "first_mint_tx_hash": contract.get("first_mint_tx_hash"),
            "creation_block": None,
            "creation_timestamp": None,
            "creation_source": None,
            "deploy_to_first_mint_seconds": None,
            "unknown_reason": None,
        }

        try:
            creation, explorer_meta = try_explorer_creation(chain, rpc, address, timestamp_cache)
        except JsonRpcError as exc:
            creation = None
            explorer_meta = {
                "source": "explorer",
                "ok": False,
                "reason": f"rpc_error_during_explorer_creation_lookup: {exc.message}",
                "code": exc.code,
                "http_status": exc.http_status,
            }
        row["creation_lookup"] = explorer_meta
        if creation is None:
            estimated_calls = estimate_creation_search_rpc_calls(first_mint_block)
            if rpc.budget.remaining < estimated_calls:
                row["unknown_reason"] = f"insufficient_rpc_budget_for_bounded_binary_search: need_about_{estimated_calls}_remaining_calls"
                rows.append(row)
                unknown_count += 1
                stopped_reason = "creation_lookup_stopped_by_rpc_call_budget"
                warnings.append("TIMING_STOPPED_BECAUSE_BINARY_SEARCH_WOULD_EXCEED_RPC_CALL_BUDGET")
                break
            try:
                creation, reason = find_creation_by_code_search(rpc, address, first_mint_block, timestamp_cache)
            except RpcBudgetExceeded as exc:
                row["unknown_reason"] = f"rpc_budget_exhausted_during_binary_search: {exc}"
                rows.append(row)
                unknown_count += 1
                stopped_reason = "creation_lookup_stopped_by_rpc_call_budget"
                warnings.append("TIMING_STOPPED_BECAUSE_BINARY_SEARCH_EXCEEDED_RPC_CALL_BUDGET")
                break
            except JsonRpcError as exc:
                creation = None
                reason = f"binary_search_rpc_error: {exc.message}"
            if creation is None:
                row["unknown_reason"] = reason or "creation lookup failed"

        if creation is not None:
            if creation["creation_block"] > first_mint_block:
                row["unknown_reason"] = "creation_block_after_first_mint_block_inconsistent"
                unknown_count += 1
            else:
                row.update(creation)
                row["deploy_to_first_mint_seconds"] = first_mint_timestamp - creation["creation_timestamp"]
                known_seconds.append(row["deploy_to_first_mint_seconds"])
        else:
            unknown_count += 1
        rows.append(row)

    not_attempted = max(0, len(contracts) - len(rows))
    if not_attempted:
        warnings.append("TIMING_SAMPLE_LIMITED_BY_MAX_CONTRACTS_OR_RPC_BUDGET")
    return {
        "sample_size": len(rows),
        "contracts_detected": len(contracts),
        "contracts_not_attempted": not_attempted,
        "known_count": len(known_seconds),
        "unknown_count": unknown_count,
        "distribution_seconds": timing_distribution(known_seconds),
        "contracts": rows,
        "warnings": list(dict.fromkeys(warnings)),
        "stopped_reason": stopped_reason,
    }


def resolve_chains(value):
    requested = [item.strip() for item in value.split(",") if item.strip()]
    resolved = []
    unresolved = []
    for item in requested:
        key = CHAIN_ALIASES.get(item.lower())
        if not key:
            unresolved.append(item)
            continue
        if key not in resolved:
            resolved.append(key)
    return requested, resolved, unresolved


def run_chain(chain, mode, max_blocks, max_contracts, budget):
    rpc = RpcClient(chain["rpc_url"], budget)
    started = time.perf_counter()
    result = {
        "ok": False,
        "chain_id": chain["chain_id"],
        "rpc_url": chain["rpc_url"],
        "mode": mode,
        "detect": None,
        "timing": None,
        "rpc_method_counts": rpc.method_counts,
        "error": None,
        "elapsed_ms": None,
    }
    try:
        detection = fetch_recent_mints(chain, rpc, max_blocks)
        timestamp_cache = detection.pop("_timestamp_cache")
        contracts = detection.pop("contracts")
        result["detect"] = detection
        if mode == "timing":
            result["timing"] = run_timing(chain, rpc, contracts, max_contracts, timestamp_cache)
        result["ok"] = result["detect"].get("complete", False)
    except RpcBudgetExceeded as exc:
        result["error"] = {"type": "RpcBudgetExceeded", "message": str(exc)}
    except JsonRpcError as exc:
        result["error"] = {"type": "JsonRpcError", "message": exc.message, "code": exc.code, "http_status": exc.http_status}
    except Exception as exc:
        result["error"] = {"type": type(exc).__name__, "message": str(exc)}
    finally:
        result["rpc_method_counts"] = dict(rpc.method_counts)
        result["elapsed_ms"] = round((time.perf_counter() - started) * 1000, 1)
    return result


def aggregate_sample_size(chains):
    seen = 0
    attempted = 0
    known = 0
    unknown = 0
    for chain_result in chains.values():
        detect = chain_result.get("detect") or {}
        timing = chain_result.get("timing") or {}
        seen += detect.get("distinct_minting_contracts_seen") or 0
        attempted += timing.get("sample_size") or 0
        known += timing.get("known_count") or 0
        unknown += timing.get("unknown_count") or 0
    return {
        "distinct_minting_contracts_seen": seen,
        "timing_contracts_attempted": attempted,
        "timing_known": known,
        "timing_unknown": unknown,
    }


def aggregate_distribution(chains):
    values = []
    for chain_result in chains.values():
        timing = chain_result.get("timing") or {}
        for row in timing.get("contracts") or []:
            value = row.get("deploy_to_first_mint_seconds")
            if value is not None:
                values.append(value)
    return timing_distribution(values)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("detect", "timing"), default="timing")
    parser.add_argument("--chains", default="ethereum,base,robinhood")
    parser.add_argument("--max-blocks", type=int, default=2000)
    parser.add_argument("--max-contracts", type=int, default=10)
    parser.add_argument("--max-rpc-calls", type=int, default=500)
    args = parser.parse_args()

    requested, chain_keys, unresolved = resolve_chains(args.chains)
    budget = RpcBudget(args.max_rpc_calls)
    chains = {}
    stopped_reason = None

    for key in chain_keys:
        if budget.remaining <= 0:
            stopped_reason = "global_rpc_call_budget_exhausted_before_all_chains_ran"
            break
        chains[key] = run_chain(CHAINS[key], args.mode, max(1, args.max_blocks), max(0, args.max_contracts), budget)
        if isinstance(chains[key].get("error"), dict) and chains[key]["error"].get("type") == "RpcBudgetExceeded":
            stopped_reason = "global_rpc_call_budget_exhausted"
            break

    for key in chain_keys:
        if key not in chains:
            chains[key] = {
                "ok": False,
                "chain_id": CHAINS[key]["chain_id"],
                "rpc_url": CHAINS[key]["rpc_url"],
                "mode": args.mode,
                "detect": None,
                "timing": None,
                "rpc_method_counts": {},
                "error": {"type": "Skipped", "message": stopped_reason or "not run"},
                "elapsed_ms": 0,
            }

    output = {
        "ok": bool(chains) and all(item.get("ok") for item in chains.values()),
        "probe": "onchain_mint_detection_and_timing",
        "disposable_spike": True,
        "mode": args.mode,
        "requested_chains": requested,
        "resolved_chains": chain_keys,
        "unresolved_chains": unresolved,
        "limits": {
            "max_blocks_per_chain": max(1, args.max_blocks),
            "max_contracts_per_chain_for_timing": max(0, args.max_contracts),
            "max_rpc_calls_total": budget.limit,
        },
        "rpc_calls_used_total": budget.used,
        "stopped_reason": stopped_reason,
        "sample_size": aggregate_sample_size(chains),
        "aggregate_timing_distribution_seconds": aggregate_distribution(chains) if args.mode == "timing" else None,
        "chains": chains,
        "caveats": [
            "Deploy-to-first-mint is a lower bound on lead time versus a public announcement; announcements are not observable on-chain, so this probe measures deploy-to-mint, which is different and weaker than deploy-to-announcement.",
            "The probe only observes ERC-721 Transfer mints and ERC-1155 TransferSingle/TransferBatch mints in the selected recent block window.",
            "Public unauthenticated RPC endpoints are rate-limited and not production infrastructure; errors are reported per chain instead of retried indefinitely.",
            "Contract creation found by eth_getCode binary search is the first block where runtime code is observable, not a Trace/Debug enumeration of CREATE or CREATE2 operations.",
        ],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if output["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
