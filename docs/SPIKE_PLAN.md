# Technical Spike Plan

## Purpose
Spikes answer provider/architecture uncertainties without allowing disposable experiments to become production code.

Rules:
- one bounded question per spike;
- no production feature code;
- no committed credentials;
- explicit success/failure/cost cap;
- result retained under `docs/spikes/`;
- provider failure must degrade behind an adapter, not break core architecture;
- paid calls require the smallest practical test budget and explicit user approval where new spend is required.

---

## SPIKE-MARKET-001 — OpenSea live coverage/mapping — Phase 1 BLOCKING
### Question
Does live OpenSea data provide useful structured discovery/stage evidence across **Ethereum + Base + Robinhood Chain**, while remaining incomplete enough that outside discovery is still necessary?

### Method
1. Use disposable probe with `OPENSEA_API_KEY`.
2. Fetch upcoming/listed drops across target chains where API supports filtering/enumeration.
3. Fetch details for >=10 representative drops.
4. Map to `Project -> MintCampaign -> MintStage -> Opportunity`.
5. Verify stage-specific allocation/time/max/price state.
6. Include multi-stage allowlist/public case; include ERC-20-priced case if present.
7. Compare against a small manual/off-OpenSea discovery sample.

### Success
- >=10 real samples map without source-specific core-schema hacks;
- multi-stage values remain stage-specific;
- FREE/KNOWN/UNKNOWN/VARIABLE price states map correctly;
- missing coverage is measurable and OpenSea is not treated as completeness authority.

### Failure
- live data cannot represent target opportunities without material domain redesign;
- target-chain support/fields are materially insufficient for useful P0 structured evidence.

### Artifact
`docs/spikes/SPIKE-MARKET-001-RESULT.md`

---

## SPIKE-TG-001 — Telegram delivery — Phase 1 BLOCKING
### Question
Can one action alert be delivered safely and observably to the user's Telegram with local dedup/outbox semantics?

### Method
1. user-created bot/token only via secret/runtime;
2. user starts bot; establish chat target;
3. send one dry-run Korean message with safe placeholder/CONSISTENT link state and correlation test id;
4. observe provider result;
5. exercise retry/dedup behavior without creating a notification storm.

### Success
- user sees one intended dry-run;
- secret not logged;
- response observable;
- retry/dedup behavior recorded.

### Artifact
`docs/spikes/SPIKE-TG-001-RESULT.md`

---

## SPIKE-X-001 — X discovery access/cost — Phase 1 BLOCKING unless X becomes optional
### Question
Can official-project/reactivation/WL signals be detected with acceptable latency/noise and bounded spend?

### Candidate modes
- STREAM_PRIMARY
- SEARCH_PRIMARY
- HYBRID
- X_OPTIONAL

### Method
1. record current Developer Console price/budget without exposing keys;
2. disposable API test only;
3. test representative official accounts + narrow keywords;
4. measure delivered volume, useful/noise ratio, observed latency/reconnect/catch-up;
5. project spend for realistic watchlist sizes;
6. compare stream vs 5/10/15m search polling if available.

### Success
- p95 official-target detection <=10m or clearly acceptable degraded mode;
- spend is predictably bounded under approved budget;
- no prohibited scraping;
- MVP watchlist capacity is adequate.

### Failure
- access/tier unavailable;
- spend materially exceeds budget;
- retrieval noise makes spend unpredictable;
- latency fails practical alert goal.

### Safety
X probe requires explicit acknowledgment before any potentially charged call.

### Artifact
`docs/spikes/SPIKE-X-001-RESULT.md`

---

# Non-blocking adapter spikes

## SPIKE-CAMPAIGN-001 — Galxe / PREMINT / Guild
Goal: select `API|OPTIONAL_API|PUBLIC_REFERENCE_ONLY|DISABLED` without protected scraping.

- Galxe structured path should be validated before production adapter enablement.
- PREMINT partner access is optional.
- Guild must have supported/public access or remain reference-only.

Artifact: `docs/spikes/SPIKE-CAMPAIGN-001-RESULT.md`.

## SPIKE-DUNE-001 — wallet cohort analytics — Phase 1.5
Measure cached/fresh result latency, credits/size, reproducibility and benchmark validity. Core radar must survive Dune unavailable.

Also validate AlphaWallet evaluation out-of-sample to reduce survivorship/look-ahead bias.

Artifact: `docs/spikes/SPIKE-DUNE-001-RESULT.md`.

## SPIKE-DISCORD-001 — permitted Discord intelligence — Phase 3
Use only explicitly authorized server/bot access. Test announcement read/member role data and required intents/permissions. No user token/self-bot/activity automation.

Artifact: `docs/spikes/SPIKE-DISCORD-001-RESULT.md`.

## SPIKE-RUNTIME-001 — runtime topology — RESOLVED
Prior spike/ADR selected hybrid topology with Railway worker + PostgreSQL and GitHub Actions only for non-critical batch/eval. Do not reopen absent new P0 evidence.

---

## Current execution order
Use the smallest actionable order based on current blockers/credentials:
1. `SPIKE-MARKET-001` — OpenSea
2. `SPIKE-TG-001` — Telegram
3. `SPIKE-X-001` — X

Campaign/Dune/Discord do not block Phase 1 unless a future ADR makes them mandatory.

## Phase 1 coding gate
Before production Phase 1 code:
- OpenSea live mapping resolved;
- Telegram delivery/config resolved;
- X resolved or explicitly optional by ADR;
- runtime already resolved;
- spike results reconciled into canonical design/status;
- no stale derived authority remains;
- no unresolved P0 provider feasibility ambiguity.
