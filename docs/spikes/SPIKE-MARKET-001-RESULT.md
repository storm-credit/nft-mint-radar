# SPIKE-MARKET-001 Result — OpenSea drop coverage

## Status
**PAPER_VALIDATED / SCHEMA_MAPPING_VALIDATED / API_OPERATIONAL_BLOCKED_BY_EXECUTION_ENVIRONMENT**

No production code was written.

## Verified against current official OpenSea documentation
- `GET /api/v2/drops` supports `featured`, `upcoming`, and `recently_minted`.
- It supports chain filters from OpenSea's supported-chain set.
- Drop detail returns stages, price, start/end time, max per wallet and supply metadata.
- API key authentication is required for reads.
- OpenSea offers an instant/free-tier API-key path according to current docs.
- OpenSea's public Drops calendar is curated/filtered; self-serve drop creation does not guarantee calendar placement.

## Chain-scope update
ADR-007 expands Phase 1 from Ethereum + Base to:
- Ethereum
- Base
- Robinhood Chain

Reason: current public OpenSea surfaces demonstrate active Robinhood Chain NFT mints/allowlists, matching the user's target pattern.

## Operational attempts
### Attempt 1
Earlier disposable access attempt could not resolve `api.opensea.io`.

### Attempt 2 — 2026-08-22
The current execution environment again failed DNS resolution for:
- `https://api.opensea.io`
- `https://api.opensea.io/api/v2/chains`

Result: environment networking limitation remains reproducible. This is **not provider failure**.

## Manual surface mapping
`SPIKE-MARKET-001-MANUAL-MAPPING-2026-08-22.md` maps 10+ real public OpenSea mint surfaces across Ethereum/Base/Robinhood Chain.

Observed structures validate the need for ADR-008:
- multiple GTD/FCFS/community/holder/public stages;
- explicit Free vs paid stages;
- Robinhood Chain ecosystem with non-native/stable-asset display contexts;
- one campaign cannot safely be collapsed into one native-price Opportunity.

Schema/model suitability after ADR-008: **PASS**.

## Important data-quality finding
Public page `$` display values are not sufficient to infer canonical payment token. Structured API/on-chain evidence must identify the payment asset; USD display is derived evidence only.

## Result
- OpenSea structured source suitability: **PASS ON PAPER**.
- Patched schema mapping against real surfaces: **PASS**.
- Robinhood Chain inclusion: **REQUIRED**.
- OpenSea as complete discovery authority: **REJECTED**.
- Live API response mapping/rate/error/coverage: **NOT YET VERIFIED**.

## Required operational evidence remaining
- obtain/configure OpenSea API key outside repo;
- fetch upcoming drops across Ethereum/Base/Robinhood Chain supported identifiers;
- fetch details for at least 10 drops;
- confirm exact chain key returned for Robinhood Chain;
- map canonical payment token fields into AssetAmount;
- compare against off-OpenSea manual discovery sample;
- record latency/rate/error behavior.

## Gate impact
Marketplace adapter remains operationally unverified because the environment cannot reach the API host. No architecture redesign is indicated; Phase 1 coding remains blocked until this is observed or explicitly waived.
