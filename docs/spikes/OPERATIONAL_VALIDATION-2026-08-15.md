# Operational Validation — 2026-08-15

## Scope
No production code was written. This pass used current first-party provider documentation, a disposable external-call attempt where possible, and repository capability checks.

## X
Status: `TECHNICALLY_FEASIBLE / BLOCKED_BY_CREDENTIAL_AND_CONSOLE_PRICE`

Confirmed:
- pay-per-use, prepaid credits
- current endpoint prices live in Developer Console
- Filtered Stream supports near-real-time delivery and up to 1,000 rules for pay-per-use
- stream/search are both valid architectural modes
- usage has a monthly post-read cap before Enterprise

Still required:
- real developer app/Bearer token
- current search/stream prices
- 10 representative rules
- observed latency, false-positive volume and projected monthly spend

## OpenSea
Status: `API_CONTRACT_PASS / LIVE_CALL_ENVIRONMENT_BLOCKED`

Confirmed:
- instant free-tier key can be created without signup
- free-tier documentation currently states 60 read requests/minute and 30-day key expiry
- upcoming drops support chain filtering
- drop details expose mint stages, price, start/end, per-wallet limit and supply data

Operational attempt:
- disposable request to the instant-key endpoint was attempted
- current execution container failed DNS resolution for `api.opensea.io`
- no key was obtained or stored

Interpretation:
- this is an execution-environment network failure, not a provider failure

Still required:
- live response from a network-capable environment
- 10+ Ethereum/Base drop mappings
- manual coverage comparison

## Galxe / PREMINT / Guild
Status: `ARCHITECTURE_RESOLVED / OPTIONAL_CREDENTIALS_REMAIN`

Galxe:
- official Quest API exposes quest status, times, counts and eligibility structures
- access token is required for normal API operation
- adapter can be optional without breaking core architecture

PREMINT:
- partner/API access is optional, never a Phase 1 hard dependency

Guild:
- public-reference/manual-deep-link mode remains initial fallback until a supported general read API is confirmed

Decision:
- campaign spike is sufficiently resolved for architecture; enabling each adapter requires provider-specific validation later

## Telegram
Status: `PROTOCOL_PASS / LIVE_DELIVERY_BLOCKED_BY_USER_BOT`

Confirmed:
- Bot API `sendMessage` accepts target chat id and returns sent Message on success
- private-chat delivery requires the user to contact/start the bot first
- local outbox/dedup remains required because transport itself is not treated as exactly-once

Still required:
- bot token
- user `/start`
- target chat id
- one dry-run alert and recorded provider message id

## Dune
Status: `PHASE_1_5_OPTIONAL / BLOCKED_BY_API_KEY_FOR_COST_MEASUREMENT`

Confirmed:
- latest saved-query results can be retrieved without triggering execution
- result retrieval still consumes credits based on result size
- fresh execution consumes compute credits and failed executions may also cost credits
- execution status itself can expose execution cost metadata

Decision:
- cached-first, bounded-refresh, budget-capped optional adapter
- not a Phase 1 blocker

## Discord
Status: `PHASE_3_SERVER_OPT_IN_ONLY`

Confirmed:
- `GUILD_MEMBERS` and `MESSAGE_CONTENT` are privileged intents
- message history/content also depends on server permission/access
- arbitrary third-party NFT Discord surveillance is not a valid product assumption

Decision:
- authorized server-installed bot only
- no user tokens, self-bots or automated chat
- not a Phase 1 blocker

## Runtime
Status: `HYBRID_TOPOLOGY_CLASS_RESOLVED / CONCRETE_PROVIDER_PENDING_X_MODE`

Confirmed:
- GitHub Actions scheduled workflows can be delayed and, at high load, queued jobs can be dropped
- therefore Actions cron-only is not suitable as sole low-latency/stream runtime

Decision:
- persistent/low-latency worker or suitable event-capable service for X/urgent feeds
- PostgreSQL durable state/outbox
- GitHub Actions only for non-critical batch/reconciliation/evals

## Repository secret visibility
Attempt to list Actions secrets via the connected GitHub integration returned `403 Resource not accessible by integration`.

Therefore this session cannot determine whether provider secrets already exist in the repository settings. Secret presence must never be guessed.

## Phase 1 blockers after this pass
Only these remain P0 operational blockers:
1. X real access + console pricing/latency/cost decision, or explicit decision to make X optional.
2. OpenSea live sample/coverage mapping from a network-capable runtime.
3. Telegram real one-message delivery.
4. Concrete low-latency hosting choice/cost, which depends mainly on final X mode.

Galxe live API validation is desirable before enabling that adapter but is no longer a core architecture blocker because source degradation is defined.

## Coding status
`PRODUCTION_CODING_BLOCKED`

The block is operational/provider evidence, not unresolved core design.
