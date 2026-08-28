# SPIKE-MARKET-001 Result — OpenSea drop coverage

## Status
**OPERATIONAL_VALIDATED / STRUCTURED_SOURCE_PASS / COVERAGE_AUTHORITY_REJECTED**

No production collector code was written. Only disposable spike runners and GitHub Actions smoke jobs were used.

## Operational evidence — 2026-08-28
Two credential-free GitHub Actions runs completed successfully against the live OpenSea API.

Retained runs:
- run `33171614678` — initial credential-free live smoke
- run `33171764870` — stricter per-chain/stratified validation

### Instant API key
Observed live response from `POST /api/v2/auth/keys`:
- HTTP `201`
- key kept only in process memory; never logged
- observed read limit: `600/h`
- observed expiry: approximately 7 days for the issued spike key

These are observations from the run, not a promise that OpenSea will keep identical limits forever.

### Chain identity
`GET /api/v2/chains` resolved all Phase 1 target keys exactly:
- `ethereum`
- `base`
- `robinhood`

`robinhood` is therefore the confirmed provider chain key for Robinhood Chain.

### Upcoming drop queries
Combined target query returned `14` drops at the observation time.

Per-chain live results:
- Ethereum: HTTP 200, `8` upcoming drops
- Base: HTTP 200, `0` upcoming drops
- Robinhood: HTTP 200, `6` upcoming drops

The Base result is important: a successful endpoint with zero `upcoming` rows is not proof that Base has no active NFT mints. Public OpenSea surfaces showed active Base minting at the same time. Therefore `upcoming` is a useful structured signal, not a complete mint inventory.

### Drop detail / MintStage validation
A bounded 10-drop detail sample was fetched successfully:
- detail success: `10/10`
- failures: `0`
- multi-stage drops: `7/10`
- total observed stages: `25`

Representative real structures:
- Ethereum `Mentographs`: Public + two presale stages
- Ethereum `Monster Crush`: Public + holder presale
- Ethereum `PIXONA: MUTAGEN`: Public + whales/team + holders/collabs + FCFS
- Robinhood `Project NINJANEX`: GTD -> FCFS -> Public
- Robinhood `Internet Monkes`: free team premint -> GTD -> FCFS -> Public
- Robinhood `Fabled Chronicles`: free treasury/honorary stages -> GTD whitelist -> Public

This directly validates ADR-008's `MintCampaign` + `MintStage` model. A single native-price Opportunity would lose real stage-specific timing, price and eligibility semantics.

### Pricing observation
The sampled OpenSea detail responses exposed mint-price values as raw integer strings for the observed stages. The spike did not observe a non-native-token payment object in the bounded 10-drop detail sample.

Decision:
- keep canonical `AssetAmount` and explicit `price_state` from ADR-008;
- never infer payment token from a UI dollar display or raw integer alone;
- if payment asset cannot be identified from provider/on-chain evidence, store payment asset as UNKNOWN and suppress asset-specific claims;
- a future non-native payment sample can refine the adapter mapping without changing the domain model.

This remaining token-canonicalization sample is **not a Phase 1 architecture blocker** because the model already fails closed for unknown payment assets.

## Coverage finding
OpenSea is operationally strong for structured listed-drop metadata but is not coverage-complete.

Evidence:
- live Base `upcoming` query returned zero while active Base mint surfaces existed;
- OpenSea's calendar/listing behavior therefore cannot be used as proof of absence;
- official X/sites, campaign platforms and on-chain discovery remain necessary parallel sources.

Decision from ADR-007 remains confirmed:
- OpenSea role = high-value structured `DISCOVERY` + `VERIFICATION` for listed drops;
- `COVERAGE_AUTHORITY = false`.

## Degradation finding
Earlier execution environments failed DNS resolution for `api.opensea.io`, while GitHub Actions successfully reached the same provider.

Therefore:
- prior failures were environment-specific, not OpenSea provider failure;
- source adapters must report `SOURCE_UNAVAILABLE/DEGRADED` without stopping unrelated sources;
- GitHub Actions/Railway outbound connectivity is a valid operational route.

## Verdict
- API reachability: **PASS**
- credential-free spike path: **PASS**
- target chain identifiers: **PASS**
- Ethereum structured mapping: **PASS**
- Robinhood structured mapping: **PASS**
- Base endpoint feasibility: **PASS**; zero current upcoming rows observed
- 10+ detail mappings: **PASS**
- multi-stage semantics: **PASS**
- provider degradation behavior: **PASS IN DESIGN / environment-specific failure observed**
- OpenSea completeness as sole discovery source: **REJECTED**
- non-native payment-token canonicalization sample: **NOT OBSERVED / NON-BLOCKING / FAIL-CLOSED UNKNOWN**

## Gate impact
`SPIKE-MARKET-001` is **CLOSED for Phase 1 provider feasibility**.

OpenSea no longer blocks `PHASE_1_CODING_READY`. Remaining blocking provider evidence is Telegram real delivery and X access/cost/mode.
