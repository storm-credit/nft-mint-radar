# Disposable Technical Spike Runners

These files are **not production code**. They exist only to close the remaining operational evidence gates in `docs/PRODUCTION_CODING_START_GATE.md`.

Rules:
- never commit credentials;
- do not import these modules from production packages later;
- every run should produce measurements copied into the matching `docs/spikes/*-RESULT.md`;
- delete/replace spike code after the architecture decision is frozen if it becomes misleading;
- X calls may consume paid API credits and require explicit opt-in.

## OpenSea

```bash
export OPENSEA_API_KEY='...'
python spikes/opensea_probe.py
```

Optional chain list:

```bash
python spikes/opensea_probe.py --chains ethereum,base,robinhood
```

The script never prints the API key. If the exact Robinhood chain slug differs, first run `--list-chains` and use the returned supported identifier.

## Telegram

```bash
export TELEGRAM_BOT_TOKEN='...'
export TELEGRAM_CHAT_ID='...'
python spikes/telegram_probe.py --send
```

No message is sent unless `--send` is supplied. The token is never printed.

## X

```bash
export X_BEARER_TOKEN='...'
python spikes/x_probe.py --query 'from:SomeOfficialAccount (allowlist OR mint OR holders)' --execute-paid
```

The X script refuses to call the API without `--execute-paid` because Post reads may consume paid credits. Before running, record current Developer Console pricing and the maximum test spend in the spike result.

## Expected outputs
Each runner emits compact JSON containing only measurements/non-secret response data. Copy the results into the relevant retained spike result file; do not treat a successful HTTP status alone as a PASS.
