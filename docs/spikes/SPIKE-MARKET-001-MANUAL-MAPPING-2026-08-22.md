# SPIKE-MARKET-001 — Manual Surface Mapping Addendum (2026-08-22)

## Status
**SCHEMA_MAPPING_PASS / API_OPERATIONAL_VALIDATION_STILL_BLOCKED_BY_ENVIRONMENT**

This addendum does not replace the required live OpenSea API spike. It validates that the patched domain model can represent real public OpenSea mint surfaces across the Phase 1 chain set.

## Why this addendum exists
The execution environment still cannot resolve `api.opensea.io`, so an API-key flow cannot be completed here. Public OpenSea collection/drop surfaces remain reachable through external web retrieval and provide enough current examples to test the model semantics without pretending the API itself was operationally validated.

## Sample mapping set

### 1. The School of NFTs — Genesis
- chain: Ethereum
- stages observed: Family allowlist (Free), WL GTD (paid), Public (paid)
- validates: multiple allowlist/public stages, explicit FREE vs KNOWN price

### 2. Kinsman
- chain: Ethereum
- stages observed: Treasury & Team (Free), Guaranteed, FCFS, Public
- validates: four-stage campaign, guaranteed + FCFS distinction

### 3. Offchain Ballers
- chain: Ethereum
- stages observed: GTD allowlist, Public
- validates: small two-stage campaign

### 4. ErasedEth
- chain: Ethereum
- stages observed: GTD, FCFS, Public with differing prices
- validates: stage-specific price cannot live safely on campaign-level Opportunity only

### 5. Beast Battle
- chain: Ethereum
- stages observed: holder allowlist variants + Public
- validates: holder-gated stage semantics and multiple holder requirement classes

### 6. Collectr
- chain: Base
- stage observed: monthly public edition
- validates: long/open-edition-style campaign and nullable/variable supply semantics

### 7. Base Fishing
- chain: Base
- stage observed: Public
- validates: simple Base public mint

### 8. Byte Solks
- chain: Base
- stages observed: Team, GTD, FCFS, Public with different limits/prices
- validates: full multi-stage mapping on Base

### 9. NUMBERS
- chain: Robinhood Chain
- stages observed: Team (Free), GTD (Free), Robinhood Frens/Communities (Free), Public (paid)
- validates: Robinhood Chain must be Phase 1 target; community-stage semantics

### 10. CatBroker
- chain: Robinhood Chain
- collection surface denominated in USDG
- stages observed: Early supporters (Free), FCFS community list (Free), Public (paid)
- validates: non-native asset ecosystem + free/paid multi-stage structure

### Additional corroborating Robinhood samples
- Ghost Kid in Robinhood: Team + community allowlist + Public
- Party Cats: Team + community allowlist + Public
- Grok Bot: TEAM + WL + PUBLIC
- HypeRobinHood: explicit FREE MINT public stage
- ChibiverseHood: Team + partner-collection WL + Public

## Model verdict
### `MintCampaign`
PASS. One collection/drop can own multiple stage records without colliding times/prices/limits.

### `MintStage`
PASS. Required observed variants are representable:
- TEAM
- ALLOWLIST/GTD
- FCFS
- HOLDER/COMMUNITY
- PUBLIC
- FREE and paid states

### `AssetAmount` + `price_state`
PASS in design. Public surfaces demonstrate that display/payment ecosystems are not safely representable as `mint_price_native` only. The API spike must confirm canonical token/address/currency fields for machine mapping.

### `Opportunity`
PASS if Opportunity references a specific campaign/stage rather than collapsing all stages into one row.

## New data-quality warning discovered
Public-facing OpenSea pages often render USD-converted values even when the underlying payment token semantics are not fully exposed in search/page text. Therefore:
- display `$x.xx` must not be assumed to mean USD stablecoin payment;
- canonical payment asset must come from structured API/on-chain/contract evidence;
- `usd_estimate` is derived evidence, never the canonical price asset.

This strengthens ADR-008.

## Coverage verdict
OpenSea is useful but must not be treated as exhaustive alpha discovery. Its own documentation states self-serve drop creation does not guarantee calendar placement. Therefore `SPIKE-MARKET-001` still requires comparison against X/official-site/campaign/on-chain discoveries after API access is available.

## Remaining API operational evidence
Still required:
1. obtain/configure OpenSea API key outside repo;
2. call `/api/v2/drops?type=upcoming` for Ethereum/Base/Robinhood Chain supported identifiers;
3. fetch detail for 10+ drops;
4. map structured stage/payment fields;
5. confirm exact Robinhood chain key returned by `/api/v2/chains`;
6. compare API results against off-OpenSea discovery sample;
7. record latency/rate/error behavior.

## Verdict
- Domain/schema patch: **PASS**
- Robinhood inclusion: **PASS / REQUIRED**
- OpenSea as P0 structured source: **KEEP**
- OpenSea as complete discovery authority: **REJECTED**
- Live API operational gate: **STILL OPEN**
