# SPIKE-DUNE-001 Result — Dune wallet/cohort analytics

## Status
**PAPER_VALIDATED / OPERATIONAL_BLOCKED_BY_API_KEY**

No production code was written.

## Verified against current official Dune documentation
- Saved queries can be executed programmatically with `POST /v1/query/{query_id}/execute`.
- Latest query results can be fetched without triggering a new execution.
- Latest-result retrieval still consumes credits based on result size.
- Query execution consumes credits based on actual compute resources; failed executions are also charged.
- Execution status inspection is free and includes execution cost metadata.
- API access requires an API key with `Read` scope.
- Current Dune docs state API access is available across plans, but programmatic execution consumes credits; free manual engine behavior is not equivalent to free automated execution.
- Current pricing docs expose per-execution/monthly budget controls and a free monthly credit allowance.

## Result
Technical fit for Alpha Wallet/cohort analytics: **PASS**.
Actual query freshness, result size and credit burn: **UNRESOLVED** until a real API key and representative queries are used.

## Decision
Dune remains optional Phase 1.5, never a hard dependency.
Adopt `CACHED_FIRST` policy:
1. prefer latest saved-query results for frequent reads;
2. trigger fresh execution only at a bounded cadence;
3. filter/project columns server-side where possible;
4. enforce a per-query and monthly credit budget;
5. degrade to stale/no wallet signal rather than blocking the core radar.

## Required operational evidence
- API key stored outside source control;
- two small queries: seed-wallet recent NFT interactions and early-minter overlap;
- record execution time, result size, credits and freshness;
- rerun with reduced columns/filters to quantify savings;
- confirm deterministic mapping into WalletSignal fixtures.

## Gate impact
Not required for Phase 1 coding readiness because Phase 1.5 is optional.
