# ADR-011 — Vertical-First Implementation Order

## Status
Accepted — 2026-08-29

Supersedes the implementation order frozen in `docs/PHASE_1_FROZEN_CONFIG.md` on the same day. It
does **not** change any contract, schema, safety invariant, or gate criterion.

## Context
`PHASE_1_CODING_READY` was set after all three blocking spikes closed, a cross-system Red Team
reached P0 = 0, and freeze reconciliation completed. The frozen implementation order was horizontal:
all canonical domain primitives, then persistence, then verification, then adapters, reaching a
Telegram renderer at step 10 and an end-to-end dry run at step 14.

A blind-spot sweep run immediately afterwards (`docs/BLIND_SPOT_SWEEP_2026-08-29.md`) found no safety
defect and no unmet gate criterion, but raised three CRITICAL questions that the horizontal order
answers last:

1. **Signal volume is unproven.** Our own measurements: X produced zero actionable mint signals on
   both tested query shapes; OpenSea `upcoming` returned 14 drops in one probe and 11 in another
   across all three target chains. `METRICS_SLO.md` begins precision review only after 30 candidate
   alerts. Nothing states the minimum volume that makes this worth running.
2. **"Early enough" is measured to Telegram and stops there.** Every latency figure is
   provider-to-system. The product asks "is it early enough to act?" and no metric answers it,
   because the human's sleep, task time and wallet setup are not in any measurement.
3. **Silence is ambiguous.** Alert suppression is correct and deliberate, but in a low-volume product
   silence is the dominant state, and a dead worker looks exactly like a quiet market.

Under the horizontal order, the first real answer to any of these arrives at step 10 or later — after
most of the build effort is already spent.

## Options considered

### A. Keep the horizontal order
- Pros: cleanest dependency graph; primitives exist before anything uses them; least rework.
- Cons: spends the majority of the build before learning whether the product has signal at all. If
  BS-1 is true, that discovery arrives after nearly all the work.

### B. Measure first, code later
Run a 30-day manual opportunity inventory before writing production code.
- Pros: answers BS-1 with the least code.
- Cons: 30 days of the user's manual effort, and it still would not answer BS-2 or BS-3, which need a
  real alert reaching a real person.

### C. Vertical slice first — CHOSEN
Build the thinnest complete path — one source, one verified opportunity, one real Telegram alert —
then harden outward.
- Pros: one artifact measures all three CRITICAL questions at once. Signal volume becomes observable,
  `human_action_latency` becomes measurable because a real alert reaches a real person, and silence
  acquires meaning because there is something that could have spoken. Time-to-first-value collapses
  from step 14 to the first slice.
- Cons: some primitives get built narrowly and widened later. This is accepted rework, and it is
  small compared to discovering BS-1 at step 10.

### D. Cheap patches only, defer the order question
- Rejected as deferral. It leaves the CRITICAL questions unanswered while coding proceeds anyway.

## Decision

The Phase 1 implementation order becomes **vertical-first**.

### Slice 1 — thinnest end-to-end path
OpenSea is the source, because it is the only one already proven to return structured multi-stage
drop data without credentials.

```text
OpenSea upcoming/detail
  -> minimal Project / MintCampaign / MintStage / Opportunity
  -> Evidence with source_availability
  -> CTA safety gate producing an ActionLinkAssessment
  -> deterministic decision gate
  -> Telegram renderer + outbox
  -> one real alert to the user
```

### Non-negotiable inside the slice
The slice is thin in **coverage**, never in **safety**. All nine invariants in
`PHASE_1_FROZEN_CONFIG.md` apply from the first commit. Specifically:
- only an `ActionLinkAssessment` with `safety_state = CONSISTENT` may render as a CTA;
- `official_action_url` is never rendered;
- the outbox delivery state machine exists in slice 1; a null `sent_at` never authorizes a resend;
- fail-closed behavior is not deferred "until after the demo".

A thin slice that cuts safety is not this decision.

### Required alongside slice 1
Three blind-spot patches are in scope because the slice cannot measure what it was built to measure
without them:
1. **`human_action_latency`** — `user_seen_or_ack_at - notification_sent_at`, recorded from the first
   alert onward (BS-2).
2. **Liveness signal** — a low-frequency status line so silence is distinguishable from death
   (BS-6). Status, not alert spam.
3. **User operating profile** — timezone, sleep/work blackout, and the escalation threshold that
   justifies waking the user (BS-3).

### Order after slice 1
Widen outward from the working path, choosing the next step by what the slice's measurements show:
official website and on-chain adapters, then normalization and full state machines, then scoring,
then the X adapter, then scheduler, fixtures runner, and integration tests. The frozen 14-step list
stays as the coverage checklist; it is no longer the sequence.

## Consequences
- Time to first real alert drops from step 10 to slice 1.
- BS-1, BS-2, BS-3 and BS-6 become measurable questions instead of open ones.
- Some primitives are built narrowly and widened later; this rework is accepted deliberately.
- No contract, schema, fixture, safety invariant or gate criterion changes.
- `ADR-010`'s X mode is untouched, but the X adapter now arrives later, which is convenient: BS-2
  questions whether the stream's seconds-level latency serves a 15-minute p95 target, and the slice's
  `human_action_latency` data will inform that before the X adapter is written.

## Revisit triggers
- slice 1 shows signal volume so low that the product thesis fails — then scope, sources or the
  project itself are reconsidered before further building;
- `human_action_latency` shows the human is the dominant delay — then revisit `ADR-010`'s latency
  rationale and consider `SEARCH_PRIMARY`;
- the slice cannot be built without weakening a safety invariant — then stop; the invariant wins and
  this ADR is reconsidered.
