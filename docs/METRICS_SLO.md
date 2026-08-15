# Metrics and SLOs

## Purpose
A radar is only useful if it is early, accurate, quiet, and safe. These are initial Phase 1 operating targets, to be recalibrated after shadow runs.

## Safety SLOs — hard gates
- Verified-link safety: 100% of user-facing ACTION/URGENT CTAs must pass official-link verification.
- Phishing fixture protection: 100% pass.
- Prohibited automation: 0 automated wallet signatures/approvals/transactions/social engagement/Discord self-bot actions.
- Secret leakage: 0 secrets in logs, evidence, fixtures, notifications, commits.

Any failure here blocks release regardless of other metrics.

## Detection latency
For provider-originated events where the provider exposes data promptly:
- P0 stream/poll sources: p95 system detection <= 15 minutes.
- URGENT recheck near deadlines: target p95 <= 5 minutes where provider/runtime supports it.
- Batch analytics sources such as Dune: freshness SLO defined per query; they do not inherit real-time SLO automatically.

`system_detection_latency = observed_at - provider_published_at`

Provider publication delay is tracked separately when measurable.

## Alert precision / noise
Initial shadow-run targets after at least 30 candidate action alerts:
- ACTION/URGENT precision >= 90% by manual review: alert truly required a relevant user action and had adequate verification.
- S/A candidate usefulness >= 80% by manual user review (`useful / total reviewed`).
- duplicate-visible-alert rate < 1%.
- T3/T4-only actionable-alert rate = 0%.

## False negative sampling
At least weekly during early operation, manually sample known notable NFT WL/mint events and ask whether radar found them early enough.
Track:
- missed opportunity count
- source that would have found it
- miss reason: coverage / parser / verification / score threshold / runtime failure

Do not optimize precision by silently accepting high miss rates.

## Lead time
For each opportunity:
- `lead_to_registration_close`
- `lead_to_mint_open`
- `lead_vs_first_broad_marketplace_listing` when comparable
- `lead_vs_first_user-seen/manual-reference` where available

Source ROI uses median unique lead time, not raw event volume.

## Verification quality
Track:
- claims promoted to OFFICIAL/HIGH
- conflicts detected before alert
- stale/corrected claims
- CTA links revoked after publication
- identity-resolution manual reviews

Target: all source conflicts that are present in fixture/known evidence are surfaced rather than arbitrarily resolved.

## Source ROI
Per source monthly:
```text
unique_actionable_leads
median_unique_lead_minutes
false_positive_count
requests
cost
cost_per_unique_actionable_lead
provider_outage_minutes
```
Sources with no unique lead value across a meaningful evaluation window should be demoted or removed.

## Wallet signal quality
Do not judge wallet intelligence by number of alerts.
Track:
- single-wallet signals
- independent cohort signals
- later official-project corroboration rate
- wash/sybil downgrades
- median lead time before official/social visibility
- cohort false positive rate

## Scoring calibration
Version every scoring rule set.
For each version maintain:
- fixture pass rate
- grade distribution
- user-action rate by grade
- downgrade/cancellation rate by grade
- false positive rate by grade

Never tune a score solely to make past winners look obvious; preserve negative/missed examples.

## Notification usefulness
For single-user deployment, Telegram alerts may be marked manually:
- USEFUL
- TOO_LATE
- TOO_NOISY
- WRONG
- ALREADY_KNEW
- MISSED_CONTEXT

This feedback is optional but becomes calibration evidence.

## Runtime health
- source fetch success rate
- last successful fetch
- queue lag
- normalization failure rate
- verification failure/conflict rate
- notification outbox age
- Telegram delivery success rate
- rate-limit incidents
- cost budget utilization

## Cost guardrails
Before production, set explicit configurable monthly caps for every paid provider and a global cap.
Behavior at cap:
1. emit operator warning;
2. degrade optional source;
3. preserve core safety/official verification sources where possible;
4. never exceed cap automatically.

Exact monetary caps are configuration/user-budget decisions and must not be invented in source code.

## Release gates
Phase 1 release candidate requires:
- 100% hard-safety fixture pass;
- >=95% curated fixture event/state/action classification;
- no unresolved P0 source identity/link bug;
- source health and cost telemetry visible;
- at least one successful Telegram dry run;
- required source/runtime spikes resolved.
