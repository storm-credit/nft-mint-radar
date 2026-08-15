# Credential Readiness

## Purpose
List the minimum external credentials/configuration required to finish operational spike validation without committing secrets or starting production implementation.

## Required before PHASE_1_CODING_READY

### X
Needed:
- X developer app
- Bearer token
- current Developer Console endpoint pricing
- explicit monthly spend cap

Secret name proposal:
- `X_BEARER_TOKEN`

Do not commit screenshots or token values. Record only endpoint prices, test scope, observed latency and estimated monthly spend.

### Telegram
Needed:
- user-created bot token
- user sends `/start` to the bot
- target chat id resolved from bot update/runtime

Secret name proposal:
- `TELEGRAM_BOT_TOKEN`

Config (non-secret) proposal:
- `TELEGRAM_CHAT_ID`

Required evidence:
- one dry-run message delivered exactly once from the test path
- provider message id/result recorded without token exposure

### OpenSea
No user account is required for the documented instant free-tier key path, but live provider access must be tested from an environment that can resolve/reach `api.opensea.io`.

For longer testing/production, secret name proposal:
- `OPENSEA_API_KEY`

Required evidence:
- upcoming Ethereum/Base response
- at least 10 drop samples mapped to canonical Opportunity
- stage fields: allowlist/public, price, start/end, max per wallet, supply
- manual coverage comparison

## Optional Phase 1 adapters

### Galxe
Secret name proposal:
- `GALXE_ACCESS_TOKEN`

Galxe is not a hard blocker if the adapter remains optional and degrades to official/public references. A live token query should still be completed before enabling the Galxe adapter in production.

### PREMINT
Partner/API access is optional. Do not block Phase 1 on PREMINT Connect approval.

### Guild
Begin as public-reference/manual deep-link source until a supported read API contract is independently confirmed.

## Later-phase credentials

### Dune — Phase 1.5
- `DUNE_API_KEY`

### Discord — Phase 3 only
- `DISCORD_BOT_TOKEN`
- server installation and required permissions/intents

## GitHub integration limitation observed
The currently connected GitHub integration can read/write repository contents but cannot list repository Actions secrets (`403 Resource not accessible by integration`). Therefore secret presence cannot be verified from this agent session and must not be guessed.

## Safety rules
- never paste secrets into repository files, issues, PRs or logs
- never commit `.env`
- redact provider responses that echo credentials
- rotate any credential accidentally exposed
- spike artifacts store only metadata/results, never token values
