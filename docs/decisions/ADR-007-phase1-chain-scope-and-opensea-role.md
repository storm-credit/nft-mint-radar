# ADR-007 — Phase 1 Chain Scope and OpenSea Role

## Status
Accepted — 2026-08-22

## Context
The original Phase 1 scope was Ethereum + Base to keep the first implementation EVM-only. A new blind-spot audit found that this excluded Robinhood Chain even though the user's target pattern includes The Saudis-style legacy NFT revival and Robinhood Chain is already hosting NFT mints/allowlists on OpenSea.

OpenSea's public Drop surface is also curated/filtered rather than a guaranteed complete inventory of all self-serve drops, so treating it as a coverage-complete discovery feed would overstate its role.

## Decision
### Phase 1 target chains
Use an EVM-first target set:
1. Ethereum
2. Base
3. Robinhood Chain

Persist normalized chain identity (`chain_key` plus EIP-155 chain id when available), not display strings only.

No Solana/Bitcoin/non-EVM expansion occurs in Phase 1 without a separate ADR.

### OpenSea role
OpenSea remains a P0 structured adapter because it provides high-value drop/stage/schedule/price data.

But it is explicitly **not** considered complete discovery coverage.

Roles:
- `DISCOVERY`: strong for OpenSea-listed drops, incomplete globally;
- `VERIFICATION`: strong structured stage/price/schedule evidence when project identity is corroborated;
- `COVERAGE_AUTHORITY`: false.

## Consequences
- `SPIKE-MARKET-001` must include Robinhood Chain samples.
- Coverage comparison must include projects discovered outside OpenSea.
- Missing OpenSea presence cannot be treated as evidence that a project/mint does not exist.
- Existing EVM domain architecture remains valid; no broad redesign required.

## Rejected alternatives
### Keep Ethereum + Base only
Rejected because it fails the user's demonstrated target use case.

### Add every OpenSea-supported chain now
Rejected as speculative over-expansion and contrary to minimum-action design.

### Make Robinhood a Phase 2 chain
Rejected because current target opportunities already exist there.

## Revalidation trigger
Revisit Phase 1 chain set if source ROI shows a target chain contributes negligible unique actionable alpha, or if another chain repeatedly contributes missed S/A-grade opportunities.
