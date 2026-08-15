# Executable Harness Specification

## Purpose
Turn the policy rules in `CLAUDE.md` into an execution contract that an AI agent can follow and verify before touching production code.

## Harness stages

### H0 — Context Load
Required inputs:
- `CLAUDE.md`
- `docs/PROJECT_STATUS.md`
- `docs/ARCHITECTURE.md`
- `docs/SOURCE_STRATEGY.md`
- `docs/BLIND_SPOT_SWEEP.md`
- relevant ADRs

Output:
- concise current-state summary
- current phase
- blocked/unblocked work types

Fail if:
- required authority files conflict without an ADR resolving the conflict.

### H1 — Intent Contract
Output fields:
- goal
- primary user
- immediate task
- in-scope
- out-of-scope
- measurable success conditions
- stop conditions

Fail if:
- success cannot be observed or tested.

### H2 — Blind-Spot Sweep
Required categories:
- data/source coverage
- timing/latency
- API/auth/cost
- safety/security
- ToS/automation boundaries
- false positives/false negatives
- duplicate/stale information
- operational failure modes

Output:
- P0/P1/P2 risks
- mitigations
- unresolved questions

### H3 — Trap Check
Must explicitly check:
- rate limits
- paid API dependency
- scraping fragility
- source identity spoofing
- phishing URLs
- stale wallet labels
- wash/sybil manipulation
- timezone/deadline conversion
- accidental social-account automation
- accidental wallet-signing path

### H4 — Four-Option Decision
For material architecture/product decisions produce four materially different options.
Each option must include:
- description
- strengths
- weaknesses
- cost/complexity
- failure modes
- reversibility

Output:
- chosen option
- rejected alternatives
- ADR path

### H5 — Design Contract
Before implementation, required artifacts depend on task type.

For a source adapter:
- source role/tier
- auth model
- polling/stream model
- rate/cost assumptions
- raw event schema
- normalized output schema
- retry/backoff
- stale/deletion handling
- fixture examples

For a scoring component:
- inputs
- formula/rules
- explainability output
- calibration fixtures
- regression expectations

For a notification component:
- trigger
- severity
- dedup fingerprint
- CTA/link safety rule
- payload fixture
- re-alert policy

### H6 — Implementation Gate
Production implementation is allowed only if:
- current task is unblocked by `PROJECT_STATUS.md`
- Deep Design exit criteria relevant to the task are satisfied
- unresolved P0 ambiguity is zero
- required spike results exist
- success tests are specified

Otherwise output `BLOCKED_BY_DESIGN` or `BLOCKED_BY_SPIKE` and do not write production code.

### H7 — Verification
A feature is complete only when at least one suitable verification path exists:
- unit test
- integration fixture
- contract/schema test
- dry-run event
- sandbox API response
- observable Telegram test

Required output:
- tests run
- expected result
- actual result
- failures
- residual risks

### H8 — Deviation Record
If implementation differs materially from plan:
- original plan
- actual change
- reason
- impact
- compatibility/migration impact
- follow-up

Record under `docs/deviations/CHANGELOG_DECISIONS.md`.

## Agent contracts

### Discovery Agent
Goal: find candidate projects/opportunities early.
Must not:
- assert official mint/WL instructions from T3/T4 alone
- recommend action without verification status

Output minimum:
- project candidate
- source
- source tier
- discovered_at
- raw signal reference
- candidate type
- confidence

### Verification Agent
Goal: corroborate actionable facts.
Output minimum:
- claim
- supporting evidence
- source tier
- official-link status
- confidence
- conflicting evidence
- expiry/recheck time

### Scoring Agent
Goal: produce explainable component scores.
Output minimum:
- quality_score
- alpha_score
- effort_score when applicable
- risk_score
- evidence_confidence
- component reasons
- no-guarantee disclaimer state

Must not:
- increase score solely because an influencer/famous wallet is involved
- hide unsupported assumptions

### Wallet Intelligence Agent
Goal: interpret public wallet/cohort behavior.
Output minimum:
- wallet/cohort identifiers
- identity confidence
- signal type
- entry timing
- independence assessment
- wash/sybil/conflict flags
- strength

### Quest Parser Agent (Phase 2)
Goal: convert WL instructions into structured user tasks.
Output minimum:
- required/optional tasks
- deadline
- FCFS/raffle/guaranteed type
- external platform
- wallet/social/Discord dependency
- manual-action requirement

Must never execute social engagement or wallet actions.

### Decision Agent
Goal: decide whether an alert is action-worthy.
Output minimum:
- action class: WATCH / APPLY_WL / PREPARE / MINT_RECHECK / AVOID / NO_ALERT
- reasons
- urgency
- confidence
- required next user action
- missing information

### Telegram Reporter
Goal: render concise actionable messages.
Must include when known:
- project
- grade/component scores
- current state
- deadline in KST
- next action
- evidence confidence
- verified official link
- risk flags

Must not:
- include an unverified mint link as CTA
- send routine no-change spam

## Fixture plan
Create fixture families before production prompt trust:
1. official X allowlist announcement
2. PREMINT raffle with social tasks
3. Galxe quest with WL reward
4. Discord-level requirement disclosed on official site
5. fake phishing reply impersonating official project
6. deleted/edited mint date
7. conflicting official X vs website date
8. famous wallet enters low-quality project
9. three independent alpha wallets enter before announcement
10. wash-like wallet cluster
11. holder snapshot already passed
12. free mint whose contract is not yet officially linked

Each fixture needs:
- raw inputs
- expected normalized event
- expected evidence status
- expected action class
- forbidden outputs

## Error taxonomy
- `SOURCE_UNAVAILABLE`
- `AUTH_REQUIRED`
- `RATE_LIMITED`
- `STALE_EVIDENCE`
- `IDENTITY_UNCERTAIN`
- `CONFLICTING_OFFICIAL_SOURCES`
- `UNVERIFIED_LINK`
- `SCHEMA_PARSE_FAILED`
- `DUPLICATE_EVENT`
- `COST_BUDGET_EXCEEDED`
- `BLOCKED_BY_DESIGN`
- `BLOCKED_BY_SPIKE`
- `SAFETY_BOUNDARY`

## Harness completion criteria
The harness is considered executable-in-design when:
- all agent contracts exist
- typed schemas are defined for their I/O
- fixture families and expected outputs exist
- failure/stop conditions exist
- phase gates are machine-checkable or checklist-checkable
- validation outputs are standardized
- at least one dry-run scenario can be executed end-to-end without production credentials

Until then, the project remains `policy harness complete / executable harness incomplete`.
