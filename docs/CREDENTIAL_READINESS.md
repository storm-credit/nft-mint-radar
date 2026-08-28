# Credential Readiness

## Purpose
List the minimum external credentials/configuration still required to finish Phase 1 operational validation without committing secrets or starting production implementation.

## Current blocker count
Only **two** Phase 1 provider validations still need user-owned credentials/access:
1. Telegram
2. X

OpenSea provider feasibility is already operationally validated and no longer requires user setup.

---

## Telegram — required / lowest-friction next step

### User must do only this
1. Create a bot with `@BotFather`.
2. Store the token as GitHub Actions/runtime secret named `TELEGRAM_BOT_TOKEN`.
3. Open that bot in Telegram and send `/start` once.

That is enough for the disposable spike in the normal clean-bot case.

### `TELEGRAM_CHAT_ID`
Optional for the spike.

If absent, `spikes/telegram_probe.py` uses `getUpdates` to locate the latest private conversation after `/start`.

Exception:
- if the bot already has an active webhook, `getUpdates` cannot be used simultaneously; then configure `TELEGRAM_CHAT_ID` explicitly or use a clean test bot.

### Required evidence
- one Korean dry-run message arrives;
- provider response/message id observed;
- chat target matches;
- token never appears in logs;
- retry/dedup semantics recorded.

No wallet connection or CTA is needed for the first delivery spike.

---

## X — required after Telegram
Needed:
- X Developer app/project access;
- Bearer token as `X_BEARER_TOKEN`;
- current Developer Console endpoint pricing/credits;
- explicit acceptable test/monthly spend cap.

The manual workflow will not run X unless the user enters exactly:

`I_UNDERSTAND_X_MAY_COST`

The first trial is intentionally bounded to a small recent-search result set. Do not widen watchlists or use a persistent stream until first observed cost/noise/utility is recorded.

Required evidence:
- authenticated request succeeds;
- useful/noise ratio on bounded NFT signal query;
- latency;
- current spend projection;
- final operating mode: `STREAM_PRIMARY`, `SEARCH_PRIMARY`, `HYBRID`, or `X_OPTIONAL`.

Do not commit token values or screenshots containing credentials.

---

## OpenSea — CLOSED for Phase 1 feasibility
No user setup is required for the completed spike.

Observed live on GitHub Actions:
- instant free API key issuance succeeded;
- `ethereum`, `base`, `robinhood` provider keys resolved;
- per-chain API calls succeeded;
- 10/10 detail sample succeeded;
- multi-stage GTD/FCFS/holder/public/free structures observed;
- `upcoming` coverage was proven incomplete, so OpenSea remains a structured source, not completeness authority.

See `docs/spikes/SPIKE-MARKET-001-RESULT.md`.

A full `OPENSEA_API_KEY` may later be configured for longer-lived production use, but it is not a current user-action blocker.

---

## Optional/later credentials

### Galxe
- `GALXE_ACCESS_TOKEN`
- live query required only before enabling the adapter in production.

### PREMINT
Partner/API access optional; do not block Phase 1 on approval.

### Guild
Begin as supported public-reference/manual deep-link path until a read API is independently validated.

### Dune — Phase 1.5
- `DUNE_API_KEY`

### Discord — Phase 3
- `DISCORD_BOT_TOKEN`
- server installation + required permissions/intents

---

## GitHub integration limitation
The connected GitHub integration cannot safely enumerate repository Actions secrets. Secret presence must remain `UNKNOWN` until the corresponding workflow actually proves the credential path.

## Safety rules
- never paste secrets into repository files, issues, PRs or logs;
- never commit `.env`;
- redact provider responses that echo credentials;
- rotate any credential accidentally exposed;
- spike artifacts store only measurements/results, never token values.
