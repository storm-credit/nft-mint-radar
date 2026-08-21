#!/usr/bin/env python3
"""Disposable OpenSea operational probe. Not production code."""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://api.opensea.io/api/v2"


def request_json(path: str, api_key: str):
    req = urllib.request.Request(
        BASE + path,
        headers={"X-API-KEY": api_key, "User-Agent": "nft-mint-radar-spike/1.0"},
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
            "error": exc.read(1000).decode("utf-8", "replace"),
        }
    except Exception as exc:
        return {
            "ok": False,
            "status": None,
            "latency_ms": round((time.perf_counter() - started) * 1000, 1),
            "error": f"{type(exc).__name__}: {exc}",
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chains", default="ethereum,base,robinhood")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--list-chains", action="store_true")
    args = parser.parse_args()

    api_key = os.getenv("OPENSEA_API_KEY")
    if not api_key:
        print(json.dumps({"ok": False, "error": "OPENSEA_API_KEY missing"}))
        return 2

    if args.list_chains:
        result = request_json("/chains", api_key)
        if result.get("body"):
            result["body"] = result["body"]
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["ok"] else 1

    params = urllib.parse.urlencode(
        {"type": "upcoming", "chains": args.chains, "limit": max(1, min(args.limit, 100))}
    )
    result = request_json("/drops?" + params, api_key)

    out = {
        "ok": result["ok"],
        "status": result["status"],
        "latency_ms": result["latency_ms"],
        "requested_chains": args.chains.split(","),
    }

    if result["ok"]:
        body = result["body"]
        drops = body.get("drops", body.get("results", [])) if isinstance(body, dict) else []
        out["returned_count"] = len(drops) if isinstance(drops, list) else None
        out["sample"] = drops[:10] if isinstance(drops, list) else body
        if isinstance(body, dict):
            out["cursor_present"] = bool(body.get("next") or body.get("cursor"))
    else:
        out["error"] = result.get("error")

    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
