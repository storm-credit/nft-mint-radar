#!/usr/bin/env python3
"""Disposable Telegram delivery probe. Not production code."""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--send", action="store_true")
    args = parser.parse_args()

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print(json.dumps({"ok": False, "error": "TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID missing"}))
        return 2
    if not args.send:
        print(json.dumps({"ok": False, "error": "refusing to send without --send"}))
        return 2

    correlation_id = f"tg-spike-{uuid.uuid4().hex[:10]}"
    text = (
        "🧪 NFT Mint Radar Telegram Spike\n"
        f"Correlation: {correlation_id}\n"
        "상태: 실제 전송 테스트\n"
        "CTA: 없음 — 지갑 연결/서명/민팅을 수행하지 않습니다."
    )

    payload = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode()
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    req = urllib.request.Request(url, data=payload, method="POST", headers={"User-Agent": "nft-mint-radar-spike/1.0"})
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = json.load(resp)
            result = body.get("result", {}) if isinstance(body, dict) else {}
            out = {
                "ok": bool(body.get("ok")) if isinstance(body, dict) else False,
                "status": resp.status,
                "latency_ms": round((time.perf_counter() - started) * 1000, 1),
                "correlation_id": correlation_id,
                "message_id": result.get("message_id"),
                "chat_id_matches": str(result.get("chat", {}).get("id")) == str(chat_id),
            }
            print(json.dumps(out, ensure_ascii=False, indent=2))
            return 0 if out["ok"] else 1
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
