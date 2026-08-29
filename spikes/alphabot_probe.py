#!/usr/bin/env python3
"""Disposable Alphabot allowlist-flow probe. Not production code.

This answers one bounded question for ADR/WL discovery: does site-wide
GET /raffles contain a meaningful flow of Robinhood Chain raffles?

The probe intentionally does not call Team-only endpoints. It reads only
User-available /raffles, then filters blockchain == "RH" client-side.
"""

import argparse
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from typing import Any

BASE_URL = "https://api.alphabot.app/v1"
USER_AGENT = "nft-mint-radar-alphabot-spike/0.1"
SECRET_ENV = "ALPHABOT_API_KEY"
MAX_RAFFLES_REQUESTS_PER_HOUR = 30
DEFAULT_MAX_REQUESTS = 6
HARD_MAX_REQUESTS = 20
PAGE_SIZE = 50
ROBINHOOD_BLOCKCHAIN = "RH"


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def parse_timestamp(value: Any) -> dt.datetime | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        number = float(value)
        if number > 10_000_000_000:
            number = number / 1000
        try:
            return dt.datetime.fromtimestamp(number, tz=dt.timezone.utc)
        except (OverflowError, OSError, ValueError):
            return None
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    if text.isdigit():
        return parse_timestamp(int(text))
    try:
        parsed = dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def iso_or_none(value: Any) -> str | None:
    parsed = parse_timestamp(value)
    return parsed.isoformat().replace("+00:00", "Z") if parsed else None


def first_present(row: dict[str, Any], keys: tuple[str, ...]) -> Any:
    for key in keys:
        if key in row and row[key] not in (None, ""):
            return row[key]
    return None


def nested_get(row: dict[str, Any], container_key: str, keys: tuple[str, ...]) -> Any:
    value = row.get(container_key)
    if not isinstance(value, dict):
        return None
    return first_present(value, keys)


def extract_rows(body: Any) -> list[Any]:
    if isinstance(body, list):
        return body
    if not isinstance(body, dict):
        return []
    for key in ("raffles", "data", "results", "items"):
        value = body.get(key)
        if isinstance(value, list):
            return value
    return []


def body_has_more(body: Any, row_count: int) -> bool | None:
    if not isinstance(body, dict):
        return None
    for key in ("hasMore", "has_more", "hasNextPage", "has_next_page"):
        value = body.get(key)
        if isinstance(value, bool):
            return value
    next_value = first_present(body, ("next", "nextPage", "next_page", "nextCursor", "next_cursor"))
    if next_value not in (None, "", False):
        return True
    meta = body.get("meta") or body.get("pagination")
    if isinstance(meta, dict):
        for key in ("hasMore", "has_more", "hasNextPage", "has_next_page"):
            value = meta.get(key)
            if isinstance(value, bool):
                return value
        next_value = first_present(meta, ("next", "nextPage", "next_page", "nextCursor", "next_cursor"))
        if next_value not in (None, "", False):
            return True
        total = meta.get("total") or meta.get("totalCount") or meta.get("total_count")
        offset = meta.get("offset")
        limit = meta.get("limit") or meta.get("pageSize") or meta.get("page_size")
        page = meta.get("page") or meta.get("currentPage") or meta.get("current_page")
        try:
            if total is not None and limit is not None:
                consumed = int(offset) + row_count if offset is not None else int(page) * int(limit)
                return consumed < int(total)
        except (TypeError, ValueError):
            return None
    return None


def next_cursor(body: Any) -> str | None:
    if not isinstance(body, dict):
        return None
    value = first_present(body, ("nextCursor", "next_cursor", "cursor"))
    if value not in (None, "", False):
        return str(value)
    meta = body.get("meta") or body.get("pagination")
    if isinstance(meta, dict):
        value = first_present(meta, ("nextCursor", "next_cursor", "cursor"))
        if value not in (None, "", False):
            return str(value)
    return None


def request_json(token: str, params: dict[str, Any]) -> dict[str, Any]:
    query = urllib.parse.urlencode(params)
    req = urllib.request.Request(
        f"{BASE_URL}/raffles?{query}",
        method="GET",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "User-Agent": USER_AGENT,
        },
    )
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


def extract_blockchain(row: Any) -> str:
    if not isinstance(row, dict):
        return "UNKNOWN"
    value = first_present(row, ("blockchain", "chain", "network"))
    if isinstance(value, dict):
        value = first_present(value, ("symbol", "id", "slug", "name"))
    return str(value or "UNKNOWN")


def extract_project_name(row: dict[str, Any]) -> str | None:
    direct = first_present(row, ("projectName", "project_name", "name", "title"))
    nested = nested_get(row, "project", ("name", "title", "slug", "id"))
    return str(direct or nested) if direct or nested else None


def extract_status(row: dict[str, Any]) -> str | None:
    value = first_present(row, ("status", "state", "raffleStatus", "raffle_status"))
    return str(value) if value not in (None, "") else None


def extract_start(row: dict[str, Any]) -> Any:
    return first_present(row, ("startTime", "start_time", "startsAt", "starts_at", "startDate", "start_date", "start"))


def extract_end(row: dict[str, Any]) -> Any:
    return first_present(row, ("endTime", "end_time", "endsAt", "ends_at", "endDate", "end_date", "end"))


def extract_any_times(row: dict[str, Any]) -> list[dt.datetime]:
    candidates = [
        "createdAt",
        "created_at",
        "updatedAt",
        "updated_at",
        "startTime",
        "start_time",
        "startsAt",
        "starts_at",
        "startDate",
        "start_date",
        "start",
        "endTime",
        "end_time",
        "endsAt",
        "ends_at",
        "endDate",
        "end_date",
        "end",
    ]
    parsed = []
    for key in candidates:
        value = row.get(key)
        ts = parse_timestamp(value)
        if ts:
            parsed.append(ts)
    return parsed


def entry_looks_open(row: dict[str, Any], now: dt.datetime) -> bool | None:
    status = (extract_status(row) or "").lower()
    start = parse_timestamp(extract_start(row))
    end = parse_timestamp(extract_end(row))
    if start and now < start:
        return False
    if end and now > end:
        return False

    closed_words = ("closed", "ended", "complete", "completed", "cancelled", "canceled", "paused")
    open_words = ("open", "active", "live", "started", "running")
    if any(word in status for word in closed_words):
        return False
    if any(word in status for word in open_words):
        return True
    if start or end:
        return True
    return None


def summarize_rh(row: dict[str, Any], now: dt.datetime) -> dict[str, Any]:
    return {
        "project_name": extract_project_name(row),
        "status": extract_status(row),
        "start": iso_or_none(extract_start(row)),
        "end": iso_or_none(extract_end(row)),
        "entry_looks_open": entry_looks_open(row, now),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--max-requests",
        type=int,
        default=DEFAULT_MAX_REQUESTS,
        help=f"Hard request budget for /raffles. Clamped to {HARD_MAX_REQUESTS}, below the 30/hour limit.",
    )
    args = parser.parse_args()

    max_requests = max(1, min(args.max_requests, HARD_MAX_REQUESTS))
    token = os.getenv(SECRET_ENV)
    if not token:
        print(json.dumps({
            "ok": False,
            "status": "BLOCKED_BY_CREDENTIAL",
            "secret": SECRET_ENV,
            "network_call_made": False,
        }, ensure_ascii=False))
        return 2

    now = utc_now()
    requests_made = 0
    page = 1
    cursor = None
    raffles: list[dict[str, Any]] = []
    page_errors: list[dict[str, Any]] = []
    data_exhausted = False
    stop_reason = None

    while requests_made < max_requests:
        params: dict[str, Any] = {"limit": PAGE_SIZE, "page": page}
        if cursor:
            params = {"limit": PAGE_SIZE, "cursor": cursor}

        requests_made += 1
        result = request_json(token, params)
        if not result.get("ok"):
            page_errors.append({
                "page": page,
                "status": result.get("status"),
                "latency_ms": result.get("latency_ms"),
                "error": result.get("error"),
            })
            page += 1
            continue

        rows = extract_rows(result.get("body"))
        normalized_rows = [row for row in rows if isinstance(row, dict)]
        raffles.extend(normalized_rows)

        if len(rows) == 0:
            data_exhausted = True
            stop_reason = "empty_page"
            break

        has_more = body_has_more(result.get("body"), len(rows))
        cursor = next_cursor(result.get("body"))
        if has_more is False or (has_more is None and len(rows) < PAGE_SIZE):
            data_exhausted = True
            stop_reason = "end_of_data"
            break

        page += 1

    if stop_reason is None:
        stop_reason = "request_budget_exhausted" if requests_made >= max_requests else "stopped"

    blockchain_counts = Counter(extract_blockchain(row) for row in raffles)
    breakdown = [
        {"blockchain": chain, "count": count}
        for chain, count in sorted(blockchain_counts.items(), key=lambda item: (-item[1], item[0]))
    ]

    window_times = []
    all_times = []
    for row in raffles:
        for value in (extract_start(row), extract_end(row)):
            ts = parse_timestamp(value)
            if ts:
                window_times.append(ts)
        all_times.extend(extract_any_times(row))
    span_basis = "min/max across parsed raffle start/end timestamps returned by /raffles"
    span_times = window_times
    if not span_times:
        span_basis = "min/max across parsed created/updated/start/end raffle timestamps returned by /raffles"
        span_times = all_times
    span_start = min(span_times) if span_times else None
    span_end = max(span_times) if span_times else None
    days_covered = None
    if span_start and span_end:
        days_covered = round(max(0.0, (span_end - span_start).total_seconds() / 86400), 3)

    rh_rows = [row for row in raffles if extract_blockchain(row).upper() == ROBINHOOD_BLOCKCHAIN]
    rh_share = round(len(rh_rows) / len(raffles), 6) if raffles else 0.0
    sample_truncated_by_budget = requests_made >= max_requests and not data_exhausted

    out = {
        "ok": not page_errors or bool(raffles),
        "status": "OK_PARTIAL" if page_errors else "OK",
        "base_url": BASE_URL,
        "endpoint": "GET /raffles",
        "total_raffles_seen": len(raffles),
        "blockchain_breakdown": breakdown,
        "time_span_covered": {
            "start": span_start.isoformat().replace("+00:00", "Z") if span_start else None,
            "end": span_end.isoformat().replace("+00:00", "Z") if span_end else None,
            "days": days_covered,
            "basis": span_basis,
        },
        "rh": {
            "blockchain": ROBINHOOD_BLOCKCHAIN,
            "count": len(rh_rows),
            "share_of_total": rh_share,
            "raffles": [summarize_rh(row, now) for row in rh_rows],
        },
        "verdict_input": {
            "rh_raffle_count": len(rh_rows),
            "rh_share_of_total": rh_share,
            "days_covered": days_covered,
        },
        "subscription_scope_used": "User",
        "requests_made": requests_made,
        "max_requests": max_requests,
        "hard_max_requests": HARD_MAX_REQUESTS,
        "provider_rate_limit_per_hour": MAX_RAFFLES_REQUESTS_PER_HOUR,
        "page_size": PAGE_SIZE,
        "data_exhausted": data_exhausted,
        "budget_exhausted_before_data_ran_out": sample_truncated_by_budget,
        "stop_reason": stop_reason,
        "page_errors": page_errors,
        "caveats": [
            "This measures raffles listed on Alphabot, which is not the same as all mints on that chain.",
            "A chain being supported in Alphabot's enum is not evidence that mints there actually use the platform.",
            "Robinhood filtering is client-side because /raffles has no blockchain filter; a truncated sample can under-count RH raffles.",
        ],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
