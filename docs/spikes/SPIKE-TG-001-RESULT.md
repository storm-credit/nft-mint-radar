# SPIKE-TG-001 Result — Telegram delivery

## Status
**SPIKE_VALIDATED — real Korean dry-run delivered 2026-08-29**

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

## Operational delivery observed — 2026-08-29
`Telegram Spike Smoke` run `33255435740`, after the bot token was configured and the
user sent `/start` to `@nftmr_bot`.

Observed:
- provider HTTP status: **200**;
- `ok`: **true**;
- provider `message_id`: **4**;
- end-to-end send latency: **467.8 ms**;
- chat target resolution: `getUpdates-private-chat` — resolved automatically, no
  `TELEGRAM_CHAT_ID` was configured;
- `chat_id_matches`: **true** — the chat the provider echoed back is the chat the probe
  targeted, so the message went to the intended private conversation;
- `korean_text_sent`: **true**;
- `cta_present`: **false** — the dry-run carries no wallet-impacting call to action;
- one `sendMessage` call produced exactly one provider Message result.

Prior fail-closed behavior on the same bot remains observed and is part of this evidence:
runs `33254983732` and `33255307246` returned `update_count: 0` and refused to send
because no private chat existed yet. The probe never guessed a target.

### Contract conclusions
- Telegram is confirmed usable as the Phase 1 notification destination.
- Automatic chat resolution from a clean bot works; the user never had to look up a chat id.
- Delivery is observable (status + message id + latency), which is what the outbox/retry
  contract needs to decide success.
- Telegram is still not treated as exactly-once transport: local outbox fingerprint state
  remains responsible for deduplication. This spike delivered one message and does not
  by itself prove repeat-suppression; that belongs to the notifier implementation and its
  fixtures, not to provider behavior.

## Superseded — exact user action required
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
**Telegram no longer blocks Phase 1.** `SPIKE-TG-001 = PASS`.

The remaining Phase 1 operational blocker is X alone.
