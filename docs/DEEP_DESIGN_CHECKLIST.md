# Deep Design Checklist

Deep Design v1 is complete when every design item below is decided, documented, and testable. Provider feasibility/cost validation remains a separate Spike gate.

## A. Product and scope
- [x] Primary user and primary job-to-be-done fixed. (`DEEP_DESIGN.md`)
- [x] Phase 1 target chains fixed: Ethereum + Base.
- [x] Phase 1 target marketplace/launchpad scope fixed: OpenSea structured source first; others evidence-driven after spike.
- [x] Phase 1 source list fixed and ranked P0/P1/P2. (`SOURCE_STRATEGY.md`, `SOURCE_ADAPTER_CONTRACTS.md`)
- [x] Explicit non-goals fixed.
- [x] Success metrics fixed: safety, precision, lead time, noise, false-positive/miss review. (`METRICS_SLO.md`)

## B. Data model
- [x] Canonical `Project` schema.
- [x] Canonical `Source` schema.
- [x] Canonical `Evidence` schema.
- [x] Canonical `Opportunity` schema.
- [x] Canonical `Quest` schema even if Phase 2 behavior is not implemented.
- [x] Canonical `WalletEntity` and `InfluencerEntity` schemas.
- [x] Entity identity merge/split rules.
- [x] Evidence immutability and versioning rules.

## C. Event normalization
- [x] Canonical raw event envelope.
- [x] Normalized event types.
- [x] Source timestamp vs observed timestamp semantics.
- [x] URL/entity identity normalization policy.
- [x] Deleted/edited post handling.
- [x] Duplicate and near-duplicate detection rules.

## D. Verification
- [x] Trust-tier transition rules.
- [x] Official-account/site linkage verification.
- [x] Contract-link verification.
- [x] Conflicting-source resolution.
- [x] Minimum evidence required per actionable claim.
- [x] Confidence taxonomy.
- [x] Stale evidence expiry/recheck rules.

## E. Opportunity state machine
- [x] Full state transition model.
- [x] Illegal transition handling.
- [x] Allowlist open/close/result states.
- [x] Holder snapshot semantics.
- [x] Mint scheduled/open/ended/cancelled states.
- [x] Change/correction handling.

## F. Scoring
- [x] Quality components and weights.
- [x] Alpha/earliness components and weights.
- [x] Effort components and weights.
- [x] Risk components and penalties.
- [x] Evidence confidence adjustment.
- [x] Cohort/wallet signal adjustment.
- [x] Influencer signal cap.
- [x] Action-score formula.
- [x] S/A/B/C/D thresholds.
- [x] Calibration fixture/regression policy. (`EVAL_FIXTURES.md`, `METRICS_SLO.md`)

## G. Wallet/Dune intelligence
- [x] Seed wallet policy.
- [x] Alpha Wallet Score v1 definition.
- [x] Cohort independence definition.
- [x] Early-entry percentile definition.
- [x] Successful-collection benchmark definition.
- [x] Wash/sybil penalties/features.
- [x] Dune query specs and provisional refresh strategy. (`WALLET_INTELLIGENCE_SPEC.md`)
- [x] Fallback behavior when Dune is unavailable.

Note: final Dune cadence/cost is validation-gated by `SPIKE-DUNE-001`, not a missing domain design item.

## H. WL / Quest future contract
- [x] Quest action taxonomy.
- [x] Deadline semantics.
- [x] Mandatory vs optional task distinction.
- [x] FCFS vs raffle vs guaranteed WL representation.
- [x] Discord role/level requirement representation.
- [x] Social-task representation without automated execution.
- [x] UserProgress state model.

## I. Notification design
- [x] Telegram payload schema.
- [x] Alert severity levels.
- [x] Actionability threshold.
- [x] Re-alert material-change threshold.
- [x] Deadline reminder/recheck policy.
- [x] Daily summary is optional and not required for Phase 1.
- [x] Dedup fingerprint.
- [x] Link safety presentation rules.

## J. Runtime and persistence
- [x] Storage choice and rationale: PostgreSQL semantics; SQLite allowed for local harness fixtures.
- [x] Idempotency strategy.
- [x] Logical scheduler/worker model.
- [x] Retry/backoff strategy.
- [x] Rate-limit handling.
- [x] Source degradation/fallback behavior.
- [x] UTC storage/KST presentation policy.
- [x] Retention and cleanup policy.

Note: deployment topology (Actions/serverless/worker/hybrid) is intentionally deferred to `SPIKE-RUNTIME-001` behind stable interfaces.

## K. Security
- [x] Secret inventory.
- [x] Least-privilege access plan.
- [x] No-private-key guarantee.
- [x] No-signature/approval/transaction guarantee.
- [x] No Discord self-bot guarantee.
- [x] No automated spam/referrals/social impersonation.
- [x] Phishing URL handling.
- [x] Official-link re-verification before CTA.

## L. Operations
- [x] Structured logging schema.
- [x] Error taxonomy.
- [x] Health indicators.
- [x] Per-source cost accounting.
- [x] Per-source lead-time accounting.
- [x] False-positive/miss tracking.
- [x] Manual override/disable mechanism.

## M. Technical spike contracts
For every uncertain dependency the contract defines:
- [x] question
- [x] hypothesis
- [x] method
- [x] success condition
- [x] failure condition
- [x] time/cost cap
- [x] artifact to keep
- [x] architectural decision unlocked by result

Defined in `SPIKE_PLAN.md` for X, campaign platforms, Telegram, Dune, Discord, marketplace coverage and runtime topology.

## Deep Design v1 exit verdict
**COMPLETE IN DESIGN.**

No unresolved P0 domain/data/safety decision remains that requires rewriting core entities or trust boundaries. Remaining uncertainty is provider feasibility, credentials, pricing, latency and deployment topology, all isolated behind adapter/runtime spike contracts.

This does **not** unlock production coding by itself. Required spikes and harness execution implementation gates remain in `PROJECT_STATUS.md`.
