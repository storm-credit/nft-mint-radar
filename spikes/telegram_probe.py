#!/usr/bin/env python3
"""Disposable Telegram delivery probe. Not production code.

If TELEGRAM_CHAT_ID is absent, the probe resolves the latest private chat from getUpdates.
The user only needs to create the bot and send /start first.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

USER_AGENT = "nft-mint-radar-spike/1.1"


def telegram_json(token: str, method: str, payload: dict | None = None):
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = urllib.parse.urlencode(payload or {}).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method="POST" if data is not None else "GET", headers={"User-Agent": USER_AGENT})
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = json.load(resp)
            return {
                "ok": bool(body.get("ok")) if isinstance(body, dict) else False,
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


def resolve_chat_id(token: str):
    configured = os.getenv("TELEGRAM_CHAT_ID")
    if configured:
        return configured, "environment", None

    webhook = telegram_json(token, "getWebhookInfo")
    if webhook.get("ok"):
        info = webhook.get("body", {}).get("result", {})
        if info.get("url"):
            return None, "webhook-configured", {
                "error": "bot has a webhook configured; getUpdates cannot be used simultaneously",
                "webhook_url_present": True,
            }

    updates = telegram_json(token, "getUpdates")
    if not updates.get("ok"):
        return None, "getUpdates-failed", updates

    rows = updates.get("body", {}).get("result", [])
    for update in reversed(rows if isinstance(rows, list) else []):
        message = update.get("message") or update.get("edited_message") or {}
        chat = message.get("chat") or {}
        chat_id = chat.get("id")
        if chat_id is None:
            continue
        if chat.get("type") == "private":
            return str(chat_id), "getUpdates-private-chat", {
                "update_id": update.get("update_id"),
                "text_preview": (message.get("text") or "")[:40],
            }

    # Report the bot's public username so the operator knows which bot to open.
    # getMe returns public bot identity only; it never echoes the token.
    me = telegram_json(token, "getMe")
    bot_username = None
    if me.get("ok"):
        bot_username = (me.get("body", {}).get("result", {}) or {}).get("username")

    return None, "no-private-chat", {
        "error": "no private bot conversation found; send /start to the bot and rerun",
        "update_count": len(rows) if isinstance(rows, list) else None,
        "bot_username": bot_username,
        "open_this_bot": f"https://t.me/{bot_username}" if bot_username else None,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--send", action="store_true")
    args = parser.parse_args()

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print(json.dumps({"ok": False, "error": "TELEGRAM_BOT_TOKEN missing"}))
        return 2
    if not args.send:
        print(json.dumps({"ok": False, "error": "refusing to send without --send"}))
        return 2

    chat_id, chat_source, chat_meta = resolve_chat_id(token)
    if not chat_id:
        print(json.dumps({
            "ok": False,
            "error": "could not resolve Telegram private chat",
            "chat_source": chat_source,
            "chat_meta": chat_meta,
        }, ensure_ascii=False, indent=2))
        return 2

    correlation_id = os.getenv("SPIKE_RUN_ID") or f"tg-spike-{uuid.uuid4().hex[:10]}"
    text = (
        "🧪 NFT Mint Radar Telegram Spike\n"
        f"Correlation: {correlation_id}\n"
        "상태: 실제 전송 테스트\n"
        "CTA: 없음 — 지갑 연결/서명/민팅을 수행하지 않습니다."
    )

    sent = telegram_json(token, "sendMessage", {"chat_id": chat_id, "text": text})
    if not sent.get("ok"):
        print(json.dumps({
            "ok": False,
            "status": sent.get("status"),
            "latency_ms": sent.get("latency_ms"),
            "chat_source": chat_source,
            "error": sent.get("error") or sent.get("body"),
        }, ensure_ascii=False, indent=2))
        return 1

    body = sent.get("body") or {}
    result = body.get("result", {}) if isinstance(body, dict) else {}
    out = {
        "ok": True,
        "status": sent.get("status"),
        "latency_ms": sent.get("latency_ms"),
        "correlation_id": correlation_id,
        "message_id": result.get("message_id"),
        "chat_source": chat_source,
        "chat_resolution_meta": chat_meta,
        "chat_id_matches": str(result.get("chat", {}).get("id")) == str(chat_id),
        "korean_text_sent": True,
        "cta_present": False,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
