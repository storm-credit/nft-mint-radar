# SPIKE-TG-001 Result — Telegram delivery

## Status
**PAPER_VALIDATED / CREDENTIAL_PATH_PROBED / BLOCKED_BY_MISSING_TELEGRAM_BOT_TOKEN**

No production code was written. No Telegram network send was attempted without a configured bot token.

## Protocol suitability
Telegram remains suitable as the Phase 1 notification destination:
- `sendMessage` returns an observable Message result on success;
- incoming updates can establish a private chat target;
- local outbox/fingerprint state remains responsible for deduplication because Telegram is not treated as exactly-once transport.

## Disposable spike improvements
`spikes/telegram_probe.py` now minimizes user setup:
- required secret: `TELEGRAM_BOT_TOKEN` only;
- `TELEGRAM_CHAT_ID` is optional for a clean test bot;
- if chat id is absent, the probe checks webhook state and then resolves the latest private chat via `getUpdates` after the user sends `/start`;
- if a webhook is already active, the probe fails closed rather than silently changing webhook configuration;
- no message is sent unless `--send` is explicitly supplied.

## Operational smoke — 2026-08-28
GitHub Actions run:
- run id: `33172110528`
- job id: `98851528892`
- workflow conclusion: success as a guarded readiness check

Observed credential state:
- `TELEGRAM_BOT_TOKEN`: **ABSENT** in the workflow secret context at this run
- delivery step: **SKIPPED**
- network send attempted: **false**
- blocker artifact: `BLOCKED_BY_CREDENTIAL`

The token value was never printed because no value existed in the secret context.

## Re-observation — 2026-08-29
Guarded `Telegram Spike Smoke` rerun on the current `main`:
- run id: `33252936929`
- workflow conclusion: success as a guarded readiness check

Observed credential state:
- `TELEGRAM_BOT_TOKEN`: **ABSENT** in the workflow secret context at this run
- delivery step: **SKIPPED**
- network send attempted: **false**
- retained artifact status: `BLOCKED_BY_CREDENTIAL`

Repository secret enumeration on the same date returned zero configured Actions secrets and zero environments, so the absence is a repository-configuration fact, not a workflow-context artifact.

## Exact user action required
1. Create a bot with `@BotFather`.
2. Add the token to repository Actions secrets as `TELEGRAM_BOT_TOKEN`.
3. Open the bot in Telegram and send `/start` once.

No chat-id lookup is normally required from the user anymore.

## Remaining operational evidence
After the token exists and `/start` has been sent:
- rerun the guarded Telegram spike;
- resolve private chat automatically or from optional explicit `TELEGRAM_CHAT_ID`;
- send one Korean dry-run alert;
- record provider message id, latency and target match;
- confirm user-visible single delivery;
- retain retry/dedup behavior as the notifier contract.

## Gate impact
Telegram remains a Phase 1 blocker, but the blocker is now precisely **one missing user-owned credential plus `/start`** rather than an unresolved integration design.
