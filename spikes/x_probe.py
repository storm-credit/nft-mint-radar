#!/usr/bin/env python3
"""Disposable X operational probe. May consume paid API credits. Not production code.

The probe is intentionally bounded:
- recent search returns at most 10 Posts;
- filtered stream receives at most 10 Posts;
- at the current public X Post-read rate ($0.005/resource), the Post-read upper
  bound for --mode both is $0.10;
- stream mode refuses to run when the project already has stream rules, because
  those rules could deliver unrelated billable Posts into the same connection.

Pricing can change. The retained spike result must record the console/public rate
observed at execution time before promoting an architecture decision.
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
import uuid

API = "https://api.x.com/2"
POST_READ_USD = 0.005
MAX_SEARCH_POSTS = 10
MAX_STREAM_POSTS = 10
USER_AGENT = "nft-mint-radar-x-spike/1.1"


def headers(token: str, *, json_body: bool = False):
    h = {
        "Authorization": f"Bearer {token}",
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }
    if json_body:
        h["Content-Type"] = "application/json"
    return h


def request_json(method: str, path: str, token: str, payload=None, timeout=20):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API + path,
        data=data,
        method=method,
        headers=headers(token, json_body=payload is not None),
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
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


def recent_search(token: str, query: str):
    params = urllib.parse.urlencode({
        "query": query,
        "max_results": MAX_SEARCH_POSTS,
        "tweet.fields": "created_at,author_id,entities",
    })
    result = request_json("GET", "/tweets/search/recent?" + params, token)
    out = {
        "ok": result["ok"],
        "status": result.get("status"),
        "latency_ms": result.get("latency_ms"),
        "query": query,
        "max_posts": MAX_SEARCH_POSTS,
    }
    if not result["ok"]:
        out["error"] = result.get("error")
        return out

    body = result.get("body") if isinstance(result.get("body"), dict) else {}
    posts = body.get("data") if isinstance(body.get("data"), list) else []
    out["returned_count"] = len(posts)
    out["estimated_post_read_cost_usd"] = round(len(posts) * POST_READ_USD, 4)
    out["posts"] = [
        {
            "id": p.get("id"),
            "author_id": p.get("author_id"),
            "created_at": p.get("created_at"),
            "text_preview": (p.get("text") or "")[:180],
        }
        for p in posts
    ]
    out["meta"] = body.get("meta", {})
    return out


def list_stream_rules(token: str):
    result = request_json("GET", "/tweets/search/stream/rules", token)
    if not result["ok"]:
        return result
    body = result.get("body") if isinstance(result.get("body"), dict) else {}
    rules = body.get("data") if isinstance(body.get("data"), list) else []
    return {"ok": True, "status": result.get("status"), "rules": rules}


def add_stream_rule(token: str, value: str, tag: str):
    return request_json(
        "POST",
        "/tweets/search/stream/rules",
        token,
        {"add": [{"value": value, "tag": tag}]},
    )


def delete_stream_rule(token: str, rule_id: str):
    return request_json(
        "POST",
        "/tweets/search/stream/rules",
        token,
        {"delete": {"ids": [rule_id]}},
    )


def parse_utc(value):
    if not value:
        return None
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def filtered_stream(token: str, query: str, duration_seconds: int):
    existing = list_stream_rules(token)
    if not existing.get("ok"):
        return {
            "ok": False,
            "stage": "list_rules",
            "status": existing.get("status"),
            "error": existing.get("error"),
        }

    rules = existing.get("rules", [])
    if rules:
        return {
            "ok": False,
            "status": "BLOCKED_EXISTING_RULES",
            "existing_rule_count": len(rules),
            "reason": "refusing stream spike because existing rules could add unrelated billable Posts",
        }

    tag = "nft-mint-radar-spike-" + uuid.uuid4().hex[:8]
    add = add_stream_rule(token, query, tag)
    if not add.get("ok"):
        return {
            "ok": False,
            "stage": "add_rule",
            "status": add.get("status"),
            "error": add.get("error"),
        }

    add_body = add.get("body") if isinstance(add.get("body"), dict) else {}
    added = add_body.get("data") if isinstance(add_body.get("data"), list) else []
    rule_id = added[0].get("id") if added and isinstance(added[0], dict) else None
    if not rule_id:
        return {
            "ok": False,
            "stage": "add_rule",
            "status": "MALFORMED_RULE_RESPONSE",
            "response_keys": sorted(add_body.keys()),
        }

    posts = []
    keepalives = 0
    started_wall = dt.datetime.now(dt.timezone.utc)
    started = time.monotonic()
    stream_error = None
    cleanup = None

    try:
        params = urllib.parse.urlencode({"tweet.fields": "created_at,author_id"})
        req = urllib.request.Request(
            API + "/tweets/search/stream?" + params,
            headers=headers(token),
        )
        # X sends keep-alives about every 20s. Read timeout slightly above the
        # bounded experiment duration so a quiet stream can still terminate.
        with urllib.request.urlopen(req, timeout=max(25, duration_seconds + 10)) as resp:
            while len(posts) < MAX_STREAM_POSTS and time.monotonic() - started < duration_seconds:
                raw = resp.readline()
                if not raw:
                    break
                line = raw.strip()
                if not line:
                    keepalives += 1
                    continue
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError:
                    continue
                post = payload.get("data") if isinstance(payload, dict) else None
                if not isinstance(post, dict) or not post.get("id"):
                    continue
                now = dt.datetime.now(dt.timezone.utc)
                created = parse_utc(post.get("created_at"))
                lag = None
                if created:
                    lag = round((now - created).total_seconds(), 3)
                posts.append({
                    "id": post.get("id"),
                    "author_id": post.get("author_id"),
                    "created_at": post.get("created_at"),
                    "delivery_lag_seconds": lag,
                    "text_preview": (post.get("text") or "")[:180],
                })
    except urllib.error.HTTPError as exc:
        stream_error = {"status": exc.code, "error": exc.read(2000).decode("utf-8", "replace")}
    except Exception as exc:
        stream_error = {"status": None, "error": f"{type(exc).__name__}: {exc}"}
    finally:
        cleanup = delete_stream_rule(token, rule_id)

    elapsed = round((dt.datetime.now(dt.timezone.utc) - started_wall).total_seconds(), 3)
    lags = [p["delivery_lag_seconds"] for p in posts if p.get("delivery_lag_seconds") is not None]
    return {
        "ok": stream_error is None and bool(cleanup and cleanup.get("ok")),
        "query": query,
        "duration_seconds_requested": duration_seconds,
        "duration_seconds_observed": elapsed,
        "max_posts": MAX_STREAM_POSTS,
        "returned_count": len(posts),
        "estimated_post_read_cost_usd": round(len(posts) * POST_READ_USD, 4),
        "keepalive_count": keepalives,
        "delivery_lag_seconds": lags,
        "posts": posts,
        "stream_error": stream_error,
        "temporary_rule_deleted": bool(cleanup and cleanup.get("ok")),
        "cleanup_status": cleanup.get("status") if cleanup else None,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["search", "stream", "both"], default="search")
    parser.add_argument("--query", default="from:opensea (mint OR drop OR allowlist) -is:retweet")
    parser.add_argument("--stream-query", default="NFT lang:en -is:retweet")
    parser.add_argument("--stream-seconds", type=int, default=45)
    parser.add_argument("--execute-paid", action="store_true")
    args = parser.parse_args()

    if not args.execute_paid:
        print(json.dumps({
            "ok": False,
            "status": "PAID_OPT_IN_REQUIRED",
            "max_post_read_cost_usd": 0.10 if args.mode == "both" else 0.05,
        }, ensure_ascii=False, indent=2))
        return 2

    token = os.getenv("X_BEARER_TOKEN")
    if not token:
        print(json.dumps({"ok": False, "status": "BLOCKED_BY_CREDENTIAL", "secret": "X_BEARER_TOKEN"}))
        return 2

    duration = max(20, min(args.stream_seconds, 90))
    out = {
        "ok": True,
        "mode": args.mode,
        "pricing_basis": {
            "post_read_usd_per_resource": POST_READ_USD,
            "source": "X public pricing documentation; recheck Developer Console at execution time",
        },
        "hard_post_read_cost_ceiling_usd": 0.10 if args.mode == "both" else 0.05,
    }

    if args.mode in ("search", "both"):
        out["search"] = recent_search(token, args.query)
        out["ok"] = out["ok"] and bool(out["search"].get("ok"))

    if args.mode in ("stream", "both"):
        out["stream"] = filtered_stream(token, args.stream_query, duration)
        out["ok"] = out["ok"] and bool(out["stream"].get("ok"))

    actual_estimate = 0.0
    for key in ("search", "stream"):
        if isinstance(out.get(key), dict):
            actual_estimate += float(out[key].get("estimated_post_read_cost_usd") or 0)
    out["estimated_post_read_cost_usd"] = round(actual_estimate, 4)

    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
