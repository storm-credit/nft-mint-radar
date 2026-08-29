# SPIKE-X-001 Result — X discovery access/cost

## Status
**SPIKE_VALIDATED — access, latency, rule lifecycle and cost measured 2026-08-29; mode frozen in ADR-010**

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

### Bound enforcement observed in the runner — 2026-08-29
A cross-artifact consistency audit found that the documented Recent Search `<=10` cap
existed only as the `max_results` request parameter; the runner did not detect an
over-cap response. The runner was patched so that:
- estimated cost is always computed over every Post the provider actually returned,
  never over a locally truncated view, because truncating would understate real spend;
- an over-cap response sets `post_cap_exceeded` and fails the leg (`POST_CAP_EXCEEDED`)
  rather than reporting a bounded PASS;
- a combined estimate above the declared ceiling sets `post_read_cost_ceiling_exceeded`
  and fails the run;
- the Filtered Stream figure is recorded as a close lower bound, because X may bill a
  small number of Posts already delivered into the socket buffer when the bounded loop stops.

Offline verification with a stubbed provider response of 13 Posts: leg failed with
`POST_CAP_EXCEEDED` and reported the true `$0.065`, not a truncated `$0.05`.
A 10-Post response still passes at `$0.05`. No network call was made.

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

## Credentialed bounded run attempt — 2026-08-29
Manual Operational Spikes run `33255336140`, mode `both`, with the exact opt-in
`I_UNDERSTAND_X_MAY_COST`. Public Post-read rate rechecked immediately before execution
at `https://docs.x.com/x-api/getting-started/pricing`: still `$0.005/resource`, so the
`$0.10` ceiling was unchanged. (Same page now states a 3,000,000 Post-read monthly
pay-per-use cap; the earlier recorded figure of 2,000,000 is superseded.)

Observed:
- Recent Search leg: **HTTP 403**, `reason: client-not-enrolled`, latency 86.4 ms;
- Filtered Stream leg: **HTTP 403** at the `list_rules` stage;
- provider detail text: "you must use keys and tokens from a developer App that is
  attached to a Project", `required_enrollment: "Appropriate Level of API Access"`;
- Posts returned: **0**;
- actual estimated Post-read cost: **$0.00**;
- `post_read_cost_ceiling_exceeded`: false;
- no temporary stream rule was created, because the run failed before rule creation,
  so no cleanup was pending.

### Corrected root cause — 2026-08-29
The first reading of this 403 was that the App was not attached to any Project. Developer
portal state observed afterwards shows that reading was **wrong**: the App (client id
`30418932`) *is* attached to `Default project`, and that project's plan is **Free**.
A second project, `NFT Mint Radar`, exists on the **Pay Per Use** plan with **0 apps attached**.

So the accurate cause is **plan entitlement, not project attachment**. The provider's
message names project attachment, but the operative field is
`required_enrollment: "Appropriate Level of API Access"`. A Free-plan project does not carry
Post-read entitlement for either endpoint tested.

This is the first directly measured fact about Free-tier read access in this project, and it
outranks the pricing documentation, which does not state Free-tier endpoint entitlements at all:

**Free plan cannot call `GET /2/tweets/search/recent` and cannot call
`GET /2/tweets/search/stream/rules`.** Both returned 403 from the same Free-plan App.

The bounded-spend design behaved exactly as intended: a rejected run cost `$0.00`.

### Options this opens
1. Attach an App to the existing `NFT Mint Radar` Pay Per Use project, reissue its Bearer
   Token, update the secret, and rerun the bounded `<= $0.10` test.
2. Freeze X as `X_OPTIONAL` and run Phase 1 without it. ADR-002 already permits this: official
   X is "P0 when access/budget permits but degrades cleanly", so no architecture change is
   required to drop it. Cost is coverage, not correctness.

## Pay-Per-Use bounded run — 2026-08-29
After the App was moved to the `NFT Mint Radar` Pay Per Use project, run `33255955730`
executed mode `both` with the opt-in supplied. Post-read rate rechecked immediately before
execution: still `$0.005/resource`.

### Recent Search leg — PASS
- HTTP **200**, latency **225.9 ms**;
- query: `from:opensea (mint OR drop OR allowlist) -is:retweet`;
- returned Posts: **1** (`result_count: 1`, 7-day window);
- `post_cap_exceeded`: false;
- actual Post-read cost: **$0.005**.

Access is therefore confirmed: Pay Per Use entitles Recent Search, and the earlier 403 was
purely the Free-plan entitlement.

**Signal quality of that single Post: noise, not alpha.** It is an OpenSea retrospective about
Pixelmon's 2022 Generation 1 mint, not a current or upcoming mint announcement. Useful 0 / noise 1.

This says more about the query than about X. `from:opensea` alone is a marketing account, not a
drop feed, and it produced one Post in seven days. It is not a usable Phase 1 discovery query and
must not be carried into production as one. A real useful/noise ratio still needs a sample from a
query shaped like the actual watchlist: specific project accounts plus mint/allowlist operators.

### Filtered Stream leg — rule lifecycle PASS, connection deferred
- rule creation: **succeeded**;
- stream connect: **HTTP 503**, `connection_issue: ProvisioningSubscription`,
  "Your subscription change is currently being provisioned, please try again in a minute";
- Posts delivered: **0**; cost **$0.00**;
- temporary rule deleted: **true**, `cleanup_status: 200`.

This is a transient consequence of moving the App onto Pay Per Use minutes earlier, not an
entitlement refusal. The important durable evidence here is that the **rule create/delete
lifecycle works and cleanup succeeded even on a failed connection** — the probe left no rule behind.

### Spend
- run total actual Post-read cost: **$0.005**;
- `post_read_cost_ceiling_exceeded`: false;
- remaining budget inside the approved `$0.10` ceiling: **$0.095**.

### Filtered Stream leg retry — PASS, run `33256021263`
Rerun stream-only after provisioning settled:
- **10 Posts delivered in 16.9 s**; `post_cap_exceeded`: false;
- per-Post delivery lag: 4.339, 4.539, 4.6, 4.706, 4.822, 4.839, 4.862, 5.032, 5.067, 5.128 s
  → **4.3–5.1 s observed, mean ≈ 4.8 s**, better than the ~6–7 s P99 the docs describe;
- temporary rule created and deleted, `cleanup_status: 200`, no rule left behind;
- cost **$0.05**; `post_read_cost_ceiling_exceeded`: false.

**Signal quality: useful 0 / noise 10.** Nine of ten were replies; content was generic chatter
("heart broker", "Nice update dear", "Congrats to all"). The closest to relevant was a reply
discussing a Dutch-auction mechanism, which is commentary, not an actionable mint signal.

### The measurement that decided the mode
Filtered Stream bills per **delivered** Post. This broad keyword rule delivered ~35 Posts/min
≈ 50,000 Posts/day ≈ **$250/day** at `$0.005`, for zero observed signal. Broad keyword rules are
not a tuning preference; they are a cost-explosion mechanism with measured zero yield.
Production rules must be author-scoped. See `ADR-010`.

### Total spend for SPIKE-X-001
`$0.005` search + `$0.05` stream = **$0.055** against the approved `$0.10` ceiling. No breach.

## Final mode — FROZEN
`STREAM_PRIMARY_WITH_SEARCH_RECOVERY`, with author-scoped rules mandatory, broad keyword rules
forbidden, Recent Search restricted to recovery, a deterministic source budget, and degradation
to `X_OPTIONAL` if production signal ROI stays poor. Recorded in `ADR-010`.

Honest limit of this spike: access, latency, rule lifecycle and cost mechanics are proven.
**Signal yield is not proven** — neither tested query shape produced a single actionable mint
signal, which is why the degradation path is part of the frozen decision rather than a footnote.

## Gate impact
`SPIKE-X-001` is **CLOSED**. No Phase 1 blocking operational spike remains.
