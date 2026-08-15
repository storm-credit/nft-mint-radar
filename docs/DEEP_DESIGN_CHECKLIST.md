# Deep Design Checklist

Deep Design is complete only when every P0 item below is decided, documented, and testable.

## A. Product and scope
- [ ] Primary user and primary job-to-be-done fixed.
- [ ] Phase 1 target chains fixed.
- [ ] Phase 1 target marketplaces/launchpads fixed.
- [ ] Phase 1 source list fixed and ranked P0/P1/P2.
- [ ] Explicit non-goals fixed.
- [ ] Success metrics fixed: precision, lead time, alert usefulness, false-positive rate.

## B. Data model
- [ ] Canonical `Project` schema.
- [ ] Canonical `Source` schema.
- [ ] Canonical `Evidence` schema.
- [ ] Canonical `Opportunity` schema.
- [ ] Canonical `Quest` schema even if Phase 2 behavior is not implemented.
- [ ] Canonical `WalletEntity` and `InfluencerEntity` schemas.
- [ ] Entity identity merge/split rules.
- [ ] Evidence immutability and versioning rules.

## C. Event normalization
- [ ] Canonical raw event envelope.
- [ ] Normalized event types.
- [ ] Source timestamp vs observed timestamp semantics.
- [ ] URL/entity identity normalization.
- [ ] Deleted/edited post handling.
- [ ] Duplicate and near-duplicate detection rules.

## D. Verification
- [ ] Trust-tier transition rules.
- [ ] Official-account/site linkage verification.
- [ ] Contract-link verification.
- [ ] Conflicting-source resolution.
- [ ] Minimum evidence required per actionable claim.
- [ ] Confidence taxonomy.
- [ ] Stale evidence expiry/recheck rules.

## E. Opportunity state machine
- [ ] Full state transition table.
- [ ] Illegal transition handling.
- [ ] Allowlist open/close/result states.
- [ ] Holder snapshot states.
- [ ] Mint scheduled/open/ended/cancelled states.
- [ ] Change/correction handling.

## F. Scoring
- [ ] Quality components and weights.
- [ ] Alpha/earliness components and weights.
- [ ] Effort components and weights.
- [ ] Risk components and penalties.
- [ ] Evidence confidence adjustment.
- [ ] Cohort/wallet signal adjustment.
- [ ] Influencer signal cap.
- [ ] Action-score formula.
- [ ] S/A/B/C thresholds.
- [ ] Calibration dataset and review policy.

## G. Wallet/Dune intelligence
- [ ] Seed wallet policy.
- [ ] Alpha Wallet Score definition.
- [ ] Cohort independence definition.
- [ ] Early-entry percentile definition.
- [ ] Successful-collection benchmark definition.
- [ ] Wash/sybil penalties.
- [ ] Dune query specs and refresh cadence.
- [ ] Fallback behavior when Dune is unavailable.

## H. WL / Quest future contract
- [ ] Quest action taxonomy.
- [ ] Deadline semantics.
- [ ] Mandatory vs optional task distinction.
- [ ] FCFS vs raffle vs guaranteed WL representation.
- [ ] Discord role/level requirement representation.
- [ ] Social-task representation without automated execution.
- [ ] UserProgress state model.

## I. Notification design
- [ ] Telegram payload schema.
- [ ] Alert severity levels.
- [ ] Actionability threshold.
- [ ] Re-alert material-change threshold.
- [ ] Deadline reminder policy.
- [ ] Daily summary policy, if any.
- [ ] Dedup fingerprint.
- [ ] Link safety presentation rules.

## J. Runtime and persistence
- [ ] Storage choice and rationale.
- [ ] Idempotency strategy.
- [ ] Scheduler/worker model.
- [ ] Retry/backoff strategy.
- [ ] Rate-limit handling.
- [ ] Source degradation/fallback behavior.
- [ ] UTC storage/KST presentation policy.
- [ ] Retention and cleanup policy.

## K. Security
- [ ] Secret inventory.
- [ ] Least-privilege access plan.
- [ ] No-private-key guarantee.
- [ ] No-signature/approval/transaction guarantee.
- [ ] No Discord self-bot guarantee.
- [ ] No automated spam/referrals/social impersonation.
- [ ] Phishing URL handling.
- [ ] Official-link re-verification before CTA.

## L. Operations
- [ ] Structured logging schema.
- [ ] Error taxonomy.
- [ ] Health indicators.
- [ ] Per-source cost accounting.
- [ ] Per-source lead-time accounting.
- [ ] False-positive tracking.
- [ ] Manual override/disable mechanism.

## M. Technical spike contracts
For every uncertain dependency define:
- question
- hypothesis
- method
- success condition
- failure condition
- time/cost cap
- artifact to keep
- architectural decision unlocked by result

## Deep Design exit condition
No unresolved P0 item remains that could materially change the Phase 1 architecture, data contracts, safety model, or operating cost.
