# Disposable Technical Spike Runners

These files are **not production code**. They exist only to close the remaining operational evidence gates in `docs/PRODUCTION_CODING_START_GATE.md`.

Rules:
- never commit credentials;
- do not import these modules from production packages later;
- every run should produce measurements copied into the matching `docs/spikes/*-RESULT.md`;
- delete/replace spike code after the architecture decision is frozen if it becomes misleading;
- X calls may consume paid API credits and require explicit opt-in;
- workflow-dispatch inputs are passed through environment variables, not interpolated directly into shell commands.

## Preferred path: GitHub Actions

Open:
`Actions -> Manual Operational Spikes -> Run workflow`

Choose one probe at a time.

### OpenSea
No user-created API key is required for the spike.

The runner uses `OPENSEA_API_KEY` if configured. Otherwise it requests an instant free-tier key from OpenSea's unauthenticated `/api/v2/auth/keys` endpoint, keeps it in process memory, and never prints the key.

Default targets:
- ethereum
- base
- robinhood alias

The probe first calls `/chains` and resolves requested aliases to provider chain identifiers before querying upcoming drops. It then fetches up to 10 drop-detail records and emits bounded stage/price summaries.

Optional local run:

```bash
python spikes/opensea_probe.py --chains ethereum,base,robinhood --limit 30 --detail-limit 10
```

A full `OPENSEA_API_KEY` may still be supplied through the environment when desired.

### Telegram
Required user preparation:
1. Create a bot with BotFather.
2. Store only `TELEGRAM_BOT_TOKEN` in repository/runtime secret configuration.
3. Open the bot in Telegram and send `/start` once.

`TELEGRAM_CHAT_ID` is optional for the spike. If absent, the runner calls `getUpdates` and resolves the latest private chat. This fallback does not work when the bot already has an active webhook; in that case configure the chat id explicitly or use a clean test bot.

Local run:

```bash
export TELEGRAM_BOT_TOKEN='...'
python spikes/telegram_probe.py --send
```

No message is sent unless `--send` is supplied. The token is never printed.

### X
Required:
- `X_BEARER_TOKEN` in secret configuration;
- current Developer Console pricing/budget review;
- explicit acknowledgement that the test may consume paid Post reads.

GitHub Actions refuses the X job unless the workflow input is exactly:

`I_UNDERSTAND_X_MAY_COST`

Local run:

```bash
export X_BEARER_TOKEN='...'
python spikes/x_probe.py --mode search --query 'from:SomeOfficialAccount (allowlist OR mint OR holders)' --execute-paid
```

The bound is in the runner itself: `MAX_SEARCH_POSTS = 10` and `MAX_STREAM_POSTS = 10` in `spikes/x_probe.py`, not in a workflow default. If the provider returns more Posts than the cap, or the estimated Post-read cost exceeds the declared ceiling, the probe reports the real count/cost and fails the run rather than reporting a bounded PASS. Do not widen the caps until the first spend/utility result is recorded.

## Expected outputs
Each runner emits compact JSON containing only measurements/non-secret response data.

Record results in the matching retained spike result file. A successful HTTP status alone is **not** a provider PASS: judge coverage, mapping quality, latency, noise, spend, and failure behavior against the spike contract.
