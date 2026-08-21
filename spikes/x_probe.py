#!/usr/bin/env python3
"""Disposable X recent-search probe. May consume paid API credits. Not production code."""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://api.x.com/2/tweets/search/recent"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--max-results", type=int, default=10)
    parser.add_argument("--execute-paid", action="store_true")
    args = parser.parse_args()

    if not args.execute_paid:
        print(json.dumps({
            "ok": False,
            "error": "refusing potential paid Post reads without --execute-paid",
            "query": args.query,
        }, ensure_ascii=False, indent=2))
        return 2

    token = os.getenv("X_BEARER_TOKEN")
    if not token:
        print(json.dumps({"ok": False, "error": "X_BEARER_TOKEN missing"}))
        return 2

    params = urllib.parse.urlencode({
        "query": args.query,
        "max_results": max(10, min(args.max_results, 100)),
        "tweet.fields": "created_at,author_id",
    })
    req = urllib.request.Request(
        BASE + "?" + params,
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": "nft-mint-radar-spike/1.0",
        },
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = json.load(resp)
            data = body.get("data", []) if isinstance(body, dict) else []
            meta = body.get("meta", {}) if isinstance(body, dict) else {}
            print(json.dumps({
                "ok": True,
                "status": resp.status,
                "latency_ms": round((time.perf_counter() - started) * 1000, 1),
                "returned_count": len(data),
                "newest_id": meta.get("newest_id"),
                "oldest_id": meta.get("oldest_id"),
                "result_count": meta.get("result_count"),
                "posts": [
                    {
                        "id": p.get("id"),
                        "author_id": p.get("author_id"),
                        "created_at": p.get("created_at"),
                        "text_preview": (p.get("text") or "")[:180],
                    }
                    for p in data
                ],
            }, ensure_ascii=False, indent=2))
            return 0
    except urllib.error.HTTPError as exc:
        print(json.dumps({
            "ok": False,
            "status": exc.code,
            "latency_ms": round((time.perf_counter() - started) * 1000, 1),
            "error": exc.read(1000).decode("utf-8", "replace"),
        }, ensure_ascii=False, indent=2))
        return 1
    except Exception as exc:
        print(json.dumps({
            "ok": False,
            "status": None,
            "latency_ms": round((time.perf_counter() - started) * 1000, 1),
            "error": f"{type(exc).__name__}: {exc}",
        }, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())
