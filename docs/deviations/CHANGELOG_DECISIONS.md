# Plan Deviations / Decision Change Log

Use this file only when implementation/spike work materially differs from the accepted plan or ADR.

## Entry template

### YYYY-MM-DD — <short title>
- Original plan:
- Actual change:
- Why:
- Evidence:
- Impact:
- Compatibility/migration impact:
- Follow-up:
- ADR required: YES/NO

---

## Current entries

### 2026-08-28 — OpenSea spike no longer requires user API-key setup
- Original plan: obtain/configure `OPENSEA_API_KEY` before the live marketplace spike.
- Actual change: the disposable probe first checks for a configured key, then uses OpenSea's instant free-tier key issuance when absent. The key stays only in process memory and is never printed.
- Why: provider capability allowed a smaller user-action/credential surface and removed an unnecessary blocker.
- Evidence: GitHub Actions runs `33171614678` and `33171764870`; instant-key HTTP 201; live chain/drop/detail calls succeeded.
- Impact: `SPIKE-MARKET-001` was completed without user-owned OpenSea credentials. A long-lived production key remains a later deployment concern, not a Phase 1 design/spike blocker.
- Compatibility/migration impact: none to domain contracts; disposable runner and credential-readiness docs changed.
- Follow-up: keep OpenSea smoke manual-only for targeted revalidation; production auth method is selected at deployment time within the existing adapter contract.
- ADR required: NO — existing adapter/ADR boundaries already permit auth-mode refinement.

### 2026-08-28 — Telegram spike reduces user setup to token + /start
- Original plan: user provides both `TELEGRAM_BOT_TOKEN` and a resolved `TELEGRAM_CHAT_ID` before the delivery spike.
- Actual change: `TELEGRAM_CHAT_ID` became optional. A clean test bot can resolve the latest private chat through `getUpdates` after the user sends `/start`; webhook-configured bots fail closed instead of being modified.
- Why: reduce unnecessary manual configuration while preserving permission/safety boundaries.
- Evidence: updated disposable probe and guarded GitHub Actions smoke `33172110528`; the readiness check proved the current blocker is specifically an absent `TELEGRAM_BOT_TOKEN`, and no network send occurred.
- Impact: exact user prerequisite is now only bot creation, one GitHub secret, and `/start`.
- Compatibility/migration impact: none; explicit `TELEGRAM_CHAT_ID` remains supported.
- Follow-up: after the token is configured and `/start` sent, rerun the manual Telegram spike and record provider delivery evidence.
- ADR required: NO — notifier architecture is unchanged.

### 2026-08-29 — X spike narrows from open-ended pricing study to bounded credentialed validation
- Original plan: rely on Developer Console pricing discovery first, then compare stream/search with an unspecified small paid trial and watchlist-size spend projection.
- Actual change: current official X documentation now publicly exposes Post-read pricing and Pay-per-use Filtered Stream limits. The operational spike is hard-bounded to <=10 Recent Search Posts plus <=10 Stream Posts, currently <=$0.10 in Post-read charges at the documented $0.005/resource rate.
- Why: the old paper-pricing ambiguity no longer exists, and Minimum-Action calls for removing resolved questions rather than keeping them in the runtime experiment.
- Evidence: official X pricing/Filtered Stream/getting-access documentation revalidated 2026-08-29; no-cost GitHub Actions smoke run `33245992097` compiled the probe and confirmed `X_BEARER_TOKEN` is absent without making a paid call.
- Impact: the remaining X P0 question is only credentialed access + real NFT useful/noise observation + final mode freeze. Provisional shape is `FILTERED_STREAM_PRIMARY + RECENT_SEARCH_RECOVERY`.
- Compatibility/migration impact: no domain-schema change; X adapter contract, spike plan, runner, and readiness docs were synchronized.
- Follow-up: after a Bearer Token and API credit are configured, run the explicit paid `both` spike with the manual confirmation string and reconcile the result.
- ADR required: NO unless the observed run forces a different source architecture or makes X optional.

### 2026-08-29 — X bounded-spend claim strengthened from request bound to detected breach
- Original plan: the disposable X probe "hard-caps" the bounded paid test at <=10 Recent Search Posts and <=10 Filtered Stream Posts, total <=$0.10 Post-read cost.
- Actual change: the Recent Search cap existed only as the outbound `max_results` parameter, so a larger provider response would have been costed and reported as a bounded PASS. The runner now fails the leg on an over-cap response, fails the run when the combined estimate exceeds the declared ceiling, always estimates cost over the actual returned count instead of a truncated view, and records the Filtered Stream figure as a lower bound because in-flight delivered Posts may still be billed.
- Why: the gate depends on never promoting a lower validation state through a false PASS. Truncating the sample to fit the cap would have hidden real spend, which is the failure mode the ceiling exists to prevent.
- Evidence: cross-artifact consistency audit executed by Codex under a read-only scope; both cited contradictions verified by hand against `spikes/x_probe.py`, `spikes/README.md`, and `docs/SPIKE_PLAN.md`. Offline stubbed-provider check: 13-Post response -> `POST_CAP_EXCEEDED` at true `$0.065`; 10-Post response -> PASS at `$0.05`. `python -m py_compile spikes/x_probe.py` PASS. No network or paid call.
- Impact: the <=$0.10 ceiling is now an enforced and observable property of the runner rather than a documentation claim. No architecture, schema, or ADR change.
- Compatibility/migration impact: none; probe output gains `post_cap_exceeded`, `post_read_cost_ceiling_exceeded`, and `post_read_accounting_bound` fields.
- Follow-up: the credentialed bounded run must record the execution-time Developer Console rate and confirm the breach flags stayed false before the X mode is frozen.
- ADR required: NO — the bounded-spike contract is unchanged; only its enforcement was made real.

### 2026-08-29 - X mode frozen on measured evidence, not on the provisional shape
- Original plan: provisionally `FILTERED_STREAM_PRIMARY + RECENT_SEARCH_RECOVERY`, to be confirmed by a bounded credentialed run.
- Actual change: the mode is frozen as `STREAM_PRIMARY_WITH_SEARCH_RECOVERY` in `ADR-010`, but with constraints that did not exist in the provisional shape: production stream rules must be author-scoped `from:` clauses over verified official accounts with `-is:retweet -is:reply`, broad keyword-only rules are forbidden outright, Recent Search is recovery-only advanced by `since_id`, and a deterministic source budget gates every paid read.
- Why: the measurement forced it. A broad keyword rule delivered 10 Posts in 16.9 s - about 35 Posts/min, about 50,000 Posts/day, about $250/day at $0.005 - with useful 0 / noise 10. Nine of ten were replies. Without the author-scoping constraint the frozen mode would have been a cost-explosion mechanism with measured zero yield.
- Evidence: runs `33255336140` (Free-plan 403 on both endpoints), `33255955730` (Recent Search 200 at 225.9 ms, 1 Post, $0.005; stream 503 ProvisioningSubscription, rule cleanup 200), `33256021263` (stream 10 Posts in 16.9 s, delivery lag 4.3-5.1 s, cleanup 200, $0.05). Rate rechecked at $0.005/resource before each execution. Total actual spend $0.055 of an approved $0.10 ceiling; no ceiling breach.
- Impact: `SPIKE-X-001` closes and no Phase 1 blocking operational spike remains. Gate moves from `SPIKE_REQUIRED` to `FREEZE_PENDING`. Production coding stays blocked pending the cross-system Red Team.
- Compatibility/migration impact: no domain-schema change. `SOURCE_STRATEGY`, `SOURCE_ADAPTER_CONTRACTS`, `PROJECT_STATUS`, and the start gate were synchronized in the same change.
- Follow-up: X signal yield is deliberately recorded as **unproven** - neither tested query shape produced an actionable mint signal. Production must measure the author-scoped watchlist's useful/noise ratio, and degrade to `X_OPTIONAL` under ADR-002 if it stays poor. The Red Team must challenge any design that silently assumes X surfaces mints early.
- ADR required: YES - recorded as `ADR-010`.

### 2026-08-29 - Free-tier X read access ruled out by measurement
- Original plan: treat X access as a credential/budget question.
- Actual change: recorded as a hard fact that the Free plan cannot serve this product at all. A Free-plan App returned 403 `client-not-enrolled` on both `GET /2/tweets/search/recent` and `GET /2/tweets/search/stream/rules`.
- Why: the pricing documentation does not state Free-tier endpoint entitlements, so this could only be settled by observation. An earlier reading of the same 403 blamed project attachment; the developer portal showed the App *was* attached, to a Free-plan project. The operative field was `required_enrollment`.
- Evidence: run `33255336140` from a Free-plan project, then run `33255955730` from a Pay Per Use project with the same App and token succeeding at HTTP 200.
- Impact: any future "can we do this for free" question about X reads is answered. Cost $0.00 to establish, because a rejected call returns no Posts.
- Compatibility/migration impact: none.
- Follow-up: none.
- ADR required: NO - captured inside ADR-010's context.

### 2026-08-29 - Implementation order changed from horizontal to vertical-first
- Original plan: the frozen 14-step order built all canonical domain primitives, then persistence, then verification, then adapters, reaching a Telegram renderer at step 10 and an end-to-end dry run at step 14.
- Actual change: `ADR-011` makes the order vertical-first. Slice 1 is the thinnest complete path - OpenSea to one real Telegram alert - and the 14-step list becomes a coverage checklist rather than a sequence.
- Why: a blind-spot sweep run immediately after the gate opened found no safety defect and no unmet gate criterion, but three CRITICAL questions the horizontal order answers last. Signal volume is unproven by our own measurements: X produced zero actionable mint signals on both tested query shapes, and OpenSea upcoming returned 14 and then 11 rows across all three target chains. "Early enough to act" is measured only provider-to-system, never to the human. And in a low-volume product, silence is the dominant state and a dead worker looks exactly like a quiet market. One vertical slice measures all three at once; the horizontal order measures them after most of the build is spent.
- Evidence: `docs/BLIND_SPOT_SWEEP_2026-08-29.md`; `ADR-010` "Neither tested query shape produced a single actionable mint signal"; `SPIKE-MARKET-001-RESULT.md:33`; OpenSea probe run `33257068301`; `METRICS_SLO.md:16,20,25`.
- Impact: time to first real alert drops from step 10 to slice 1. Three blind-spot patches are pulled into slice 1 scope because the slice cannot measure what it exists to measure without them: `human_action_latency`, a liveness signal, and a user operating profile.
- Compatibility/migration impact: none. No contract, schema, fixture, safety invariant or gate criterion changes. Some primitives are built narrowly and widened later; that rework is accepted deliberately.
- Follow-up: if the slice shows the human is the dominant delay, revisit ADR-010's latency rationale - it justified STREAM_PRIMARY on ~4.8s delivery against a product target of p95 15 minutes, which is roughly two orders of magnitude finer than required. The remaining honest argument for stream is cost shape, and that is not what ADR-010 records.
- ADR required: YES - recorded as `ADR-011`.

