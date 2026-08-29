# SPIKE-X-001 Result — X discovery access/cost

## Status
**PAPER_VALIDATED_CURRENT / OPERATIONAL_BLOCKED_BY_CREDENTIAL**

No production code was written.

## Current official X facts revalidated — 2026-08-29
Official X documentation now exposes enough public pricing/access detail to close the old paper-cost ambiguity:

- X API uses pay-per-usage credits with no subscription/minimum-spend requirement stated in the public docs.
- public Post reads cost **$0.005 per returned resource** at the observed documentation revision;
- pay-per-usage is capped at **2,000,000 Post reads/month** before Enterprise;
- prices can change, so the Developer Console remains the execution-time authority;
- Filtered Stream is available to Pay-per-use;
- Filtered Stream supports **1,000 rules/project**, **1 connection**, and core operators;
- official docs describe approximately **6–7 second P99** Filtered Stream delivery;
- Recent Search accepts up to **100 Posts/response** and a start time within the last **7 days**;
- app-only public-data reads use a Bearer Token.

Primary references retained for human recheck:
- `https://docs.x.com/x-api/getting-started/pricing`
- `https://docs.x.com/x-api/posts/filtered-stream/introduction`
- `https://docs.x.com/x-api/posts/search-recent-posts`
- `https://docs.x.com/x-api/getting-started/getting-access`

## Cost model
For this product, X Post-read spend is driven by returned/delivered resources, not watched-account count by itself.

```text
estimated_monthly_post_read_cost = matched_unique_post_reads * current_post_read_unit_cost
```

At the observed public rate:
- 1,000 billable Post reads -> $5
- 4,000 billable Post reads -> $20
- 10,000 billable Post reads -> $50

These are arithmetic examples, not a prediction of our production volume.

## Bounded operational experiment
`spikes/x_probe.py` now hard-bounds the initial paid validation:

### Recent Search leg
- maximum 10 returned Posts;
- current Post-read cost ceiling: **$0.05**.

### Filtered Stream leg
- maximum 10 delivered Posts;
- current Post-read cost ceiling: **$0.05**;
- temporary rule is removed after the experiment;
- stream leg refuses to run when pre-existing project stream rules exist, because unrelated rules could deliver additional billable Posts.

### Combined mode
Current Post-read ceiling: **$0.10**.

The workflow still requires the exact manual confirmation string `I_UNDERSTAND_X_MAY_COST` before any paid call.

## Current decision
Technical suitability: **PASS ON CURRENT OFFICIAL DOCUMENTATION**.

Provisional production shape if operational validation succeeds:

`FILTERED_STREAM_PRIMARY + RECENT_SEARCH_RECOVERY`

Rationale:
- Filtered Stream matches the product's low-latency official-account/WL signal requirement;
- Recent Search is useful for reconnect/catch-up and bounded backfill;
- both remain behind source budgets and can degrade to X_OPTIONAL if real signal ROI is poor.

This is not frozen until the bounded credentialed run succeeds.

## Operational evidence still required
- `X_BEARER_TOKEN` configured through GitHub Secret/runtime only;
- sufficient X API credit for a <= $0.10 Post-read spike;
- bounded search result observed;
- Filtered Stream connection/rule lifecycle observed, or a recorded access-specific failure;
- useful/noise classification of the bounded sample;
- execution-time Developer Console rate checked against the documented $0.005 assumption;
- final mode frozen as `STREAM_PRIMARY_WITH_SEARCH_RECOVERY`, `SEARCH_PRIMARY`, or `X_OPTIONAL`.

## Re-observation — 2026-08-29
`X Spike No-Cost Smoke` rerun on the current `main`:
- run id: `33252938234`
- `spikes/x_probe.py` compile: **PASS**
- `X_BEARER_TOKEN`: **ABSENT**
- paid API call attempted: **false**
- retained artifact status: `BLOCKED_BY_CREDENTIAL`

Repository secret enumeration on the same date returned zero configured Actions secrets and zero environments.

## Gate impact
The old **pricing-definition ambiguity is closed**.

Remaining Phase 1 X blocker is now only **credentialed operational evidence + final mode freeze**.
