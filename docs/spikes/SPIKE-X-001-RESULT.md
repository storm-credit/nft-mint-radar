# SPIKE-X-001 Result — X discovery access/cost

## Status
**PAPER_VALIDATED / OPERATIONAL_BLOCKED_BY_CREDENTIAL_AND_CONSOLE_PRICING**

No production code was written.

## Verified against current official X documentation
- X API v2 is pay-per-use with prepaid credits and no monthly minimum.
- Current endpoint-specific rates are exposed in the Developer Console, not fully fixed in public docs.
- Filtered Stream supports near-real-time matching, up to 1,000 rules and one pay-per-use connection.
- Current docs describe approximately 6–7 second P99 stream latency.
- Recent Search allows up to 450 requests per 15 minutes per app, 100 posts max per request.
- Billing and rate limits are separate; successful returned posts consume usage, with daily deduplication of the same post.
- Pay-per-use has a 2 million post-read monthly cap before Enterprise.

## Result
Technical feasibility: **PASS**.
Cost feasibility: **UNRESOLVED** until the user's Developer Console exposes current prices and a spend budget is chosen.
Operational latency test: **BLOCKED** without an X developer app/Bearer token.

## Provisional decision
Keep both modes in the adapter contract:
1. `STREAM_PRIMARY` candidate for official accounts / high-priority keywords when price is acceptable.
2. `SEARCH_PRIMARY`/fallback for smaller or budget-constrained watchlists.

Do not select the final mode or runtime solely from documentation.

## Required operational evidence
- current Developer Console search/stream unit prices;
- Bearer token configured outside the repo;
- 10 representative project rules;
- measured delivered-post count, false positives and observed latency;
- estimated monthly spend at 100/500/1000 watched accounts.

## Gate impact
Phase 1 X source remains `BLOCKED_BY_CREDENTIAL` for operational validation. X may be made optional if cost/access is unacceptable.
