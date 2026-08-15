# SPIKE-MARKET-001 Result — OpenSea drop coverage

## Status
**PAPER_VALIDATED / OPERATIONAL_BLOCKED_BY_EXECUTION_ENVIRONMENT**

No production code was written.

## Verified against current official OpenSea documentation
- `GET /api/v2/drops` supports `featured`, `upcoming`, and `recently_minted`.
- It supports chain filters including `ethereum` and `base`.
- Drop detail returns stages, price, start/end time, max per wallet and supply metadata.
- API key authentication is required for reads.
- OpenSea currently offers an instant free-tier API key endpoint with no signup; current docs state 60 read requests/minute and 30-day expiry for the instant key.

## Operational attempt
A credential-free POST to the documented instant-key endpoint was attempted from the current execution environment. The environment could not resolve `api.opensea.io`, so no provider response was obtained.

This is an **environment networking limitation**, not evidence that the OpenSea API failed.

## Result
Schema/API suitability for Phase 1: **PASS ON PAPER**.
Live response mapping and actual coverage: **NOT YET VERIFIED**.

## Decision
Keep OpenSea as the P0 structured marketplace/drop source for Ethereum + Base.
Do not add Magic Eden or another marketplace until a live sample proves material missing coverage.

## Required operational evidence
- obtain ephemeral/full OpenSea API key;
- fetch `type=upcoming&chains=ethereum,base`;
- map at least 10 representative drops to canonical Opportunity objects;
- compare with a manual sample of upcoming projects;
- measure unique discovery and missing coverage.

## Gate impact
Marketplace adapter remains operationally unverified, but no architecture change is indicated.
