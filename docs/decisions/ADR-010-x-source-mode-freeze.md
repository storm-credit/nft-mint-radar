# ADR-010 — X Source Mode Freeze

## Status
Accepted

## Context
`SPIKE-X-001` was the last Phase 1 blocking operational spike. Its purpose was to choose
between `STREAM_PRIMARY_WITH_SEARCH_RECOVERY`, `SEARCH_PRIMARY`, `HYBRID`, and `X_OPTIONAL`
using measured provider behavior rather than the assumption that "X matters for NFT alpha".

Measured 2026-08-29 on a Pay Per Use project, total actual spend `$0.055` against an
approved `$0.10` ceiling. Post-read rate rechecked at `$0.005/resource` immediately before
each execution.

### Access
- Free-plan project: **403 `client-not-enrolled`** on both Recent Search and Filtered Stream
  rules. Free tier cannot serve this product. Measured, not assumed.
- Pay Per Use project: both endpoints reachable.

### Recent Search — run `33255955730`
- HTTP 200, **225.9 ms**;
- `from:opensea (mint OR drop OR allowlist) -is:retweet` returned **1 Post in 7 days**;
- that Post was a retrospective about a 2022 mint. **Useful 0 / noise 1.**

### Filtered Stream — runs `33255955730`, `33256021263`
- first attempt: HTTP 503 `ProvisioningSubscription`, transient, minutes after the plan change;
- retry: **10 Posts in 16.9 s**;
- delivery lag per Post: 4.339, 4.539, 4.6, 4.706, 4.822, 4.839, 4.862, 5.032, 5.067, 5.128 s
  → observed range **4.3–5.1 s**, mean ≈ **4.8 s**, better than the ~6–7 s P99 the docs describe;
- temporary rule created and deleted, `cleanup_status: 200`, no rule left behind;
- rule `NFT lang:en -is:retweet` produced **useful 0 / noise 10**. Nine of ten were replies;
  the content was generic chatter, not mint or allowlist signal.

### The decisive cost arithmetic
Filtered Stream bills per **delivered** Post. The broad keyword rule delivered 10 Posts in
16.9 s ≈ 35 Posts/min ≈ 50,000 Posts/day ≈ **$250/day** at `$0.005`, for zero observed signal.

Broad keyword rules are therefore not a tuning preference. They are a cost-explosion
mechanism with measured zero yield.

## Options considered

### A. `SEARCH_PRIMARY`
Poll Recent Search on an interval.
- Pros: simplest; no persistent connection; naturally bounded per poll.
- Cons: discovery latency is the poll interval, not seconds. For a mint window this is the
  difference between acting and reading history.

### B. `STREAM_PRIMARY_WITH_SEARCH_RECOVERY` — CHOSEN
Author-scoped Filtered Stream rules for live signal; Recent Search for reconnect, backfill
and gap repair.
- Pros: measured ~4.8 s delivery; 1,000 rules/project is ample for a Phase 1 watchlist;
  cost scales with how often watched accounts actually post, which is low.
- Cons: requires connection lifecycle handling and a strict rule discipline.

### C. `HYBRID`
Run both continuously as co-primaries.
- Cons: pays twice for overlapping Posts and doubles operational surface with no measured
  benefit over B.

### D. `X_OPTIONAL`
Drop X from Phase 1.
- Cons: gives up the fastest observed announcement path. Kept as the degradation target
  rather than the starting point, because access, latency and rule lifecycle all passed.

## Decision

Phase 1 X mode is frozen as:

`STREAM_PRIMARY_WITH_SEARCH_RECOVERY`

subject to constraints that are part of this decision, not implementation detail:

1. **Stream rules must be author-scoped.** Production rules are built from `from:` clauses over
   verified official project accounts, with `-is:retweet -is:reply`. A rule whose match set is
   not bounded by author is forbidden.
2. **Broad keyword-only rules are forbidden in production**, including as a temporary
   convenience. The measurement above is the reason.
3. **Recent Search is recovery only** — reconnect, backfill, gap repair — advanced by `since_id`.
   It is not a polling discovery loop.
4. **A deterministic source budget gates every paid read.** Budget exhaustion sets the adapter
   `DEGRADED`; it never overspends silently. This is deterministic code, not a prompt.
5. **Signal ROI is unproven and must be measured in production.** Neither tested query shape
   produced a single actionable mint signal. If the measured useful/noise ratio of the
   author-scoped watchlist stays poor, the adapter degrades to `X_OPTIONAL` under ADR-002
   without an architecture change.

## What this ADR does not claim
- It does not claim X is a proven source of NFT alpha for this product. Access, latency, rule
  lifecycle and cost mechanics are proven. Signal yield is not.
- It does not claim the observed ~4.8 s lag is a guaranteed SLO. It is one 10-Post sample.

## Consequences
- The X adapter can be implemented against a frozen contract.
- Watchlist scale becomes the cost driver, and it is bounded by rule count and posting rate,
  both observable before spend.
- `SPIKE-X-001` closes. No Phase 1 blocking operational spike remains.

## Revisit triggers
- measured production useful/noise stays poor → degrade to `X_OPTIONAL`;
- Post-read rate changes materially from `$0.005/resource`;
- stream delivery lag degrades beyond the search-poll interval, removing B's advantage;
- rule or connection limits change on the Pay Per Use plan.
