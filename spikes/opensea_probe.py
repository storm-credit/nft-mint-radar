#!/usr/bin/env python3
"""Disposable OpenSea operational probe. Not production code.

Goals:
- require no user-created API key when OpenSea instant-key issuance is available;
- verify supported chain identifiers;
- fetch upcoming drops;
- fetch drop details for a bounded sample;
- summarize campaign/stage/price fields without pretending this is production mapping.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://api.opensea.io/api/v2"
USER_AGENT = "nft-mint-radar-spike/1.1"


def http_json(method: str, path: str, api_key: str | None = None):
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if api_key:
        headers["X-API-KEY"] = api_key
    req = urllib.request.Request(BASE + path, headers=headers, method=method)
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = json.load(resp)
            return {
                "ok": True,
                "status": resp.status,
                "latency_ms": round((time.perf_counter() - started) * 1000, 1),
                "body": body,
            }
    except urllib.error.HTTPError as exc:
        return {
            "ok": False,
            "status": exc.code,
            "latency_ms": round((time.perf_counter() - started) * 1000, 1),
            "error": exc.read(2000).decode("utf-8", "replace"),
        }
    except Exception as exc:
        return {
            "ok": False,
            "status": None,
            "latency_ms": round((time.perf_counter() - started) * 1000, 1),
            "error": f"{type(exc).__name__}: {exc}",
        }


def resolve_api_key():
    existing = os.getenv("OPENSEA_API_KEY")
    if existing:
        return existing, "environment", None

    issued = http_json("POST", "/auth/keys")
    if not issued["ok"]:
        return None, "instant-key-failed", issued
    body = issued.get("body") if isinstance(issued.get("body"), dict) else {}
    key = body.get("api_key")
    if not key:
        return None, "instant-key-malformed", {
            "ok": False,
            "status": issued.get("status"),
            "latency_ms": issued.get("latency_ms"),
            "error": "instant-key response did not contain api_key",
            "response_keys": sorted(body.keys()),
        }
    return key, "instant-free-tier", {
        "status": issued.get("status"),
        "latency_ms": issued.get("latency_ms"),
        "expires_at": body.get("expires_at"),
        "rate_limits": body.get("rate_limits"),
    }


def list_from_body(body, *keys):
    if isinstance(body, list):
        return body
    if isinstance(body, dict):
        for key in keys:
            value = body.get(key)
            if isinstance(value, list):
                return value
    return []


def chain_identity(item):
    if not isinstance(item, dict):
        return {"key": str(item), "name": str(item)}
    key = item.get("chain") or item.get("identifier") or item.get("slug") or item.get("id")
    name = item.get("name") or item.get("display_name") or key
    return {"key": key, "name": name, "raw": item}


def resolve_requested_chains(requested, chain_rows):
    identities = [chain_identity(row) for row in chain_rows]
    resolved = []
    unresolved = []
    for wanted in requested:
        w = wanted.strip().lower()
        exact = next(
            (
                c
                for c in identities
                if str(c.get("key") or "").lower() == w
                or str(c.get("name") or "").lower() == w
            ),
            None,
        )
        fuzzy = exact or next(
            (
                c
                for c in identities
                if w in str(c.get("name") or "").lower()
                or w in str(c.get("key") or "").lower()
            ),
            None,
        )
        if fuzzy and fuzzy.get("key"):
            resolved.append(str(fuzzy["key"]))
        else:
            unresolved.append(wanted)
    return list(dict.fromkeys(resolved)), unresolved, identities


def extract_slug(drop):
    if not isinstance(drop, dict):
        return None
    for key in ("collection", "collection_slug", "slug"):
        value = drop.get(key)
        if isinstance(value, str) and value:
            return value
        if isinstance(value, dict):
            nested = value.get("slug") or value.get("collection")
            if isinstance(nested, str) and nested:
                return nested
    return None


def summarize_asset(value):
    if value is None:
        return None
    if isinstance(value, (str, int, float)):
        return value
    if not isinstance(value, dict):
        return str(value)
    return {
        "amount": value.get("amount") or value.get("value") or value.get("quantity"),
        "symbol": value.get("symbol") or value.get("currency") or value.get("token_symbol"),
        "token_address": value.get("token_address") or value.get("address") or value.get("contract_address"),
        "decimals": value.get("decimals"),
    }


def summarize_stage(stage):
    if not isinstance(stage, dict):
        return {"raw": stage}
    price = stage.get("price")
    if price is None:
        price = stage.get("mint_price") or stage.get("payment")
    return {
        "label": stage.get("label") or stage.get("name") or stage.get("stage_name"),
        "type": stage.get("type") or stage.get("stage_type") or stage.get("kind"),
        "start": stage.get("start_time") or stage.get("start") or stage.get("startTime"),
        "end": stage.get("end_time") or stage.get("end") or stage.get("endTime"),
        "price": summarize_asset(price),
        "max_per_wallet": stage.get("max_per_wallet") or stage.get("maxPerWallet") or stage.get("wallet_limit"),
        "allowlist_present": bool(stage.get("allowlist") or stage.get("merkle_root") or stage.get("merkleRoot")),
    }


def summarize_drop_detail(slug, body):
    if not isinstance(body, dict):
        return {"slug": slug, "raw_type": type(body).__name__}
    stages = list_from_body(body, "stages", "mint_stages", "phases")
    return {
        "slug": slug,
        "collection_name": body.get("collection_name") or body.get("name") or body.get("collection"),
        "chain": body.get("chain") or body.get("network"),
        "total_supply": body.get("total_supply") or body.get("totalSupply"),
        "max_supply": body.get("max_supply") or body.get("maxSupply") or body.get("supply"),
        "contract_address": body.get("contract_address") or body.get("contract"),
        "stage_count": len(stages),
        "stages": [summarize_stage(stage) for stage in stages],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chains", default="ethereum,base,robinhood")
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--detail-limit", type=int, default=10)
    parser.add_argument("--list-chains", action="store_true")
    args = parser.parse_args()

    api_key, key_source, key_meta = resolve_api_key()
    if not api_key:
        print(json.dumps({
            "ok": False,
            "error": "could not resolve OpenSea API key",
            "key_source": key_source,
            "key_meta": key_meta,
        }, ensure_ascii=False, indent=2))
        return 2

    chains_result = http_json("GET", "/chains", api_key)
    if not chains_result["ok"]:
        print(json.dumps({
            "ok": False,
            "stage": "list_chains",
            "key_source": key_source,
            "error": chains_result,
        }, ensure_ascii=False, indent=2))
        return 1

    chain_rows = list_from_body(chains_result.get("body"), "chains", "results")
    requested = [c.strip() for c in args.chains.split(",") if c.strip()]
    resolved, unresolved, identities = resolve_requested_chains(requested, chain_rows)

    if args.list_chains:
        print(json.dumps({
            "ok": True,
            "key_source": key_source,
            "key_meta": key_meta,
            "requested_chains": requested,
            "resolved_chains": resolved,
            "unresolved_chains": unresolved,
            "supported_chains": [{"key": c.get("key"), "name": c.get("name")} for c in identities],
        }, ensure_ascii=False, indent=2))
        return 0

    # If an alias is not resolved by /chains, still report it but never silently pretend it was supported.
    filter_chains = resolved
    params = {"type": "upcoming", "limit": max(1, min(args.limit, 100))}
    if filter_chains:
        params["chains"] = ",".join(filter_chains)
    drops_result = http_json("GET", "/drops?" + urllib.parse.urlencode(params), api_key)

    out = {
        "ok": drops_result["ok"],
        "key_source": key_source,
        "key_meta": key_meta,
        "chain_probe_latency_ms": chains_result.get("latency_ms"),
        "requested_chains": requested,
        "resolved_chains": resolved,
        "unresolved_chains": unresolved,
        "drop_query_chains": filter_chains,
        "drop_query_latency_ms": drops_result.get("latency_ms"),
    }

    if not drops_result["ok"]:
        out["status"] = drops_result.get("status")
        out["error"] = drops_result.get("error")
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 1

    body = drops_result.get("body")
    drops = list_from_body(body, "drops", "results")
    out["returned_count"] = len(drops)
    out["cursor_present"] = bool(body.get("next") or body.get("cursor")) if isinstance(body, dict) else False
    out["drop_summaries"] = []

    detail_limit = max(0, min(args.detail_limit, 20, len(drops)))
    detail_failures = []
    for drop in drops[:detail_limit]:
        slug = extract_slug(drop)
        if not slug:
            detail_failures.append({"slug": None, "error": "no collection slug in drop list item"})
            continue
        detail = http_json("GET", "/drops/" + urllib.parse.quote(slug, safe=""), api_key)
        if not detail["ok"]:
            detail_failures.append({
                "slug": slug,
                "status": detail.get("status"),
                "error": detail.get("error"),
            })
            continue
        summary = summarize_drop_detail(slug, detail.get("body"))
        summary["latency_ms"] = detail.get("latency_ms")
        out["drop_summaries"].append(summary)

    out["detail_requested"] = detail_limit
    out["detail_success_count"] = len(out["drop_summaries"])
    out["detail_failures"] = detail_failures
    out["multi_stage_count"] = sum(1 for d in out["drop_summaries"] if (d.get("stage_count") or 0) > 1)
    out["stage_total"] = sum(d.get("stage_count") or 0 for d in out["drop_summaries"])

    # PASS here means the provider path worked. Coverage adequacy is judged from the retained result, not guessed here.
    out["probe_pass"] = len(drops) > 0 and len(out["drop_summaries"]) > 0
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out["probe_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
