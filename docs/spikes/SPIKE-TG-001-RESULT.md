# SPIKE-TG-001 Result — Telegram delivery

## Status
**PAPER_VALIDATED / OPERATIONAL_BLOCKED_BY_USER_CREDENTIALS**

No production code was written.

## Verified against current official Telegram Bot API
- `sendMessage` sends text to a `chat_id` and returns the sent Message on success.
- Message text supports 1–4096 characters after entity parsing.
- Incoming bot updates can be consumed by either `getUpdates` long polling or webhooks, not both simultaneously.
- `update_id` supports ordered/deduplicated processing semantics for incoming updates.

## Result
Delivery protocol suitability: **PASS**.
Actual end-to-end delivery: **BLOCKED** because a bot token and target chat id are intentionally not available in the repository or current runtime.

## Required operational evidence
- user-created Telegram bot;
- token stored only as runtime/GitHub secret;
- user sends `/start` to establish a chat;
- resolve target chat id without logging the token;
- send one dry-run alert with a correlation id;
- confirm exactly-once user-visible delivery and record provider response.

## Decision
Telegram remains the primary notification destination. The notifier must use outbox state and correlation/fingerprint metadata for local deduplication; Telegram itself is not treated as an exactly-once transport.

## Gate impact
`BLOCKED_BY_CREDENTIAL` until one manual dry-run is completed.
