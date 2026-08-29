# Blind Spot Sweep — 2026-08-29

## Scope
Run immediately after `PHASE_1_CODING_READY` was set, before any production code was written.

This is deliberately **not** a second Red Team. The cross-system Red Team walked a defined checklist
and closed every P0. Both sweeps here were told to read that record first, skip anything it covered,
and instead find the questions **nobody asked** — assumptions so embedded that no document states
them.

Two axes were swept independently: product/value, and operational/human reality. The orchestrator
contributed findings of its own and verified every cited line.

Both sweeps volunteered the same judgement unprompted: safety, CTA handling, source degradation,
stale artifacts and provider access/cost mechanics are genuinely well covered. Nothing below reopens
them.

## Result
- CRITICAL: 3
- MAJOR: 8
- No safety defect. No gate criterion was found unmet.
- The theme is not correctness. It is **whether a correct system will be worth running.**

---

## CRITICAL

### BS-1 — The product thesis rests on signal volume nobody has measured
**The unasked question:** what minimum volume of unique, early, actionable opportunities would make
this worth running for this one user?

Every document closes provider feasibility, safety and adapter shape, then defers source *value* to
production measurement. Nothing asks whether coding should begin before a minimum viable signal
thesis exists.

The measured evidence is uncomfortable and it is all ours:
- `ADR-010`: "Neither tested query shape produced a single actionable mint signal";
- `SPIKE-X-001-RESULT.md:218`: "Signal yield is not proven";
- `SPIKE-MARKET-001-RESULT.md:33`: the combined target query returned **14 drops**;
- today's re-probe: 11 upcoming rows across all three target chains.
- `METRICS_SLO.md:25`: precision review begins "after at least 30 candidate action alerts" — a
  threshold that may take a very long time to reach at this volume.

**What breaks:** the system is safe, quiet, technically correct, and produces almost nothing. The user
gets an expensive verifier attached to a sparse calendar, not an alpha radar.

**Response: MEASURE.** A 30-day manual opportunity inventory for this user — which mints mattered,
where each first appeared, on which chain, how much lead time existed — before committing to build
every adapter in the frozen order.

### BS-2 — "Early enough" is measured to Telegram and stops there
**The unasked question:** is an alert still useful after sleep, work, wallet setup, Discord/X task
time, gas decision and mint-site interaction are included?

`METRICS_SLO.md:20` defines `system_detection_latency = observed_at - provider_published_at`. Every
latency number in this project is provider-to-system. `DEEP_DESIGN.md:26` asks "Is it early enough to
act?" and no metric answers it.

**This directly indicts a decision made the same day.** `ADR-010` chose `STREAM_PRIMARY` partly on
measured ~4.8 s delivery versus polling "in minutes". But `METRICS_SLO.md:16` sets the product target
at **p95 detection ≤ 15 minutes**, and `ADR-005:27` speaks of a 10-minute alert SLO. Recent Search
polling at a few-minute interval already satisfies that comfortably. The stream's seconds-level
advantage is roughly two orders of magnitude finer than the product's own requirement, and it was
bought with real operational complexity: persistent connection, one-connection limit, rule lifecycle,
and the provisioning delay we actually hit during the spike.

The honest remaining argument for stream is **cost shape**, not latency — and that argument is not
the one written in `ADR-010`.

**Response: MEASURE, then revisit `ADR-010`.** Add `human_action_latency` and rebuild the mode
rationale on cost, or simplify to `SEARCH_PRIMARY`. Deciding now is far cheaper than after the
adapter exists.

### BS-3 — KST is a rendering rule, not a life schedule
**The unasked question:** what happens when the only operator is asleep or at work when the window
opens?

`DEEP_DESIGN.md:433` stores UTC and renders KST. `EVAL_FIXTURES.md:474` verifies the conversion. No
document models user availability, quiet hours, or which alert class is worth waking someone for.

**What breaks:** the product wakes the user for low-value noise, or stays politely quiet through the
one window that mattered. Both destroy trust faster than any provider latency ever will.

**Response: PATCH.** One user operating profile: timezone, sleep/work blackout, and the escalation
threshold that justifies breaking it.

---

## MAJOR

| ID | The unasked question | Response |
|---|---|---|
| BS-4 | What must be true about this human — time, accounts, risk tolerance, capital — for an alert to be worth sending? Quest actions span X, Discord, Galxe, Guild, on-chain and referral flows; nothing states which the user will actually do. | PATCH: user constraints as product inputs feeding Effort/actionability, not just copy |
| BS-5 | How many real opportunities die *because* we waited for corroboration? Fail-closed is reviewed as safety correctness; nobody measured whether safe delay destroys the lead time the product exists to provide. | MEASURE: replay known recent mints, record first weak signal vs first safe actionable signal vs window remaining |
| BS-6 | When there are no alerts, can the user tell "nothing happened" from "the worker is dead"? `SOURCE_STRATEGY.md:316` forbids "nothing found" spam and `DEEP_DESIGN.md:721` suppresses routine health noise. Silence is the dominant UX state of this product, and it is ambiguous. | PATCH: one low-frequency status surface — last successful fetch per source, candidates seen, alerts suppressed, degraded sources |
| BS-7 | Are Ethereum/Base/Robinhood where this user's opportunities actually appear, or where Phase 1 could integrate safely first? | MEASURE: build a user-opportunity map from owned collections, followed projects and past missed mints; test scope against it |
| BS-8 | In Phase 1, how does the user say "done", "skipped", "too late"? `HARNESS_SPEC.md:322` places User Progress in Phase 2+, yet `F27` sits inside the Phase 1 acceptance set (`EVAL_FIXTURES.md:466`) and assumes explicit user confirmation. The fixture set is not phase-tagged. | PATCH: either a crude Phase 1 reply path (`DONE`/`SKIP`/`TOO_LATE`/`WRONG`) or phase-tag the fixtures |
| BS-9 | If the worker, database, bot or provider account breaks unattended, who notices before the window is gone? X recovery has a hard 7-day cliff; a vacation or billing failure becomes permanent coverage loss. | PATCH: a one-person ops rule — what warns, where it warns when Telegram itself is broken, maximum tolerated unattended interval |
| BS-10 | When does the user first receive a real alert? The frozen order reaches the renderer at step 10 and the end-to-end dry run at step 14. | PATCH: make the first slice vertical — one source, one verified opportunity, one Telegram alert — then harden around it |
| BS-11 | For each provider, are we actually permitted to store, retain, replay and act on this data for months? The docs say "where permitted" without a source-by-source ledger. | MEASURE: permission ledger per source — store body, store hash, replay in fixtures, render in Telegram, retention TTL |

---

## What this does and does not change

It does **not** reopen `PHASE_1_CODING_READY`. Every gate criterion — safety, provider feasibility,
contract completeness, P0 = 0 — is genuinely met, and both sweeps confirmed it independently.

It does challenge **the first move after the gate**. The frozen order builds horizontally: all domain
primitives, then persistence, then adapters, reaching a user-visible alert at step 10 and end-to-end
at step 14. BS-1, BS-2, BS-6 and BS-10 all point the same direction: the cheapest way to answer every
open question is a **thin vertical slice** — one source through to one real Telegram alert — because
that single artifact simultaneously measures whether signal exists, how late the human actually sees
it, what silence feels like, and how long value takes to arrive.

That is a change to the frozen implementation order, so it belongs to the user as a decision, not to
the orchestrator as an edit.
