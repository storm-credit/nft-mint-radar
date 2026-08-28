# Executable Harness Specification

## Purpose
Turn the policy rules in `CLAUDE.md` into an execution contract that can be followed and verified before production code is touched.

**Important:** names below are logical execution roles. They do **not** imply one autonomous agent per role. Implementation mechanism is chosen by `docs/MINIMUM_ACTION_ADOPTION.md` and ADR-009.

---

## H0 — Minimal Context Load

Start with only:
- `CLAUDE.md`
- `docs/PROJECT_STATUS.md`
- `docs/PRODUCTION_CODING_START_GATE.md`

Then load only the authority required by the current task:
- domain/schema -> `DEEP_DESIGN.md` + relevant ADR
- source -> `SOURCE_STRATEGY.md` + adapter contract/spike
- harness -> this file + `HARNESS_SCHEMAS.md`
- eval -> `EVAL_FIXTURES.md`
- minimum-agency decision -> `MINIMUM_ACTION_ADOPTION.md` + ADR-009

Do not preload every repository document into every role.

Output:
- current phase/gate
- allowed work type
- required authority refs
- current blockers

Fail if:
- authorities conflict without a governing ADR;
- a required derived artifact is marked/observed stale.

---

## H1 — Intent Contract
Output:
- goal
- primary user
- immediate task
- in-scope
- out-of-scope
- measurable success conditions
- stop conditions
- unfilled material gaps

Fail if success cannot be observed/tested.

---

## H2 — Blind-Spot Sweep
Check only material dimensions:
- source/data coverage
- timing/latency
- API/auth/cost
- security/safety
- ToS/automation boundaries
- false positives/negatives
- stale/duplicate data
- operational recovery
- maintenance/state drift
- derived-artifact staleness

Output P0/P1/P2 findings, mitigation, unresolved questions.

---

## H3 — Preflight Trap Check
Must check:
- wrong-problem risk
- simpler mechanism available
- unnecessary agent/tool/runtime
- local model action-space >5
- delegate that only launders choices
- God Agent / Tool Swamp / Agent Explosion / persona-only agent
- excess context or permissions
- source-of-truth conflict / Shadow Authority
- Stale Derived Artifact
- rate limit / paid dependency / cost explosion
- scraping fragility
- source identity spoofing / compromised official channel
- phishing URL
- stale wallet labels
- wash/sybil manipulation
- timezone/deadline conversion
- accidental social-account automation
- accidental wallet-signing path
- missing independent critique where stakes justify it

---

## H4 — Alternatives
Only when design space is genuinely open, compare four materially different options before implementation.

Each option:
- description
- strengths
- weaknesses
- cost/complexity
- failure modes
- reversibility

Output:
- selected option
- rejected alternatives
- ADR path

Do not fabricate four options for a mechanical patch.

---

## H5 — Design Contract

### Source adapter
- source role/tier
- auth model
- polling/stream model
- rate/cost assumptions
- raw event schema
- normalized output
- retry/backoff
- stale/delete/edit handling
- degradation behavior
- fixture examples
- local action-space impact if model-driven

### Scoring
- inputs
- deterministic formula/rules
- hard gates
- explainability
- calibration fixtures
- regression expectations

### Notification
- trigger
- severity
- fingerprint/dedup
- CTA/link safety
- payload fixture
- re-alert policy

### Model-driven node
Must additionally define:
- why deterministic/direct work is insufficient
- exact minimal context bundle
- tools/actions exposed
- local action-space count
- authority boundary
- success/stop conditions
- independent-review need

---

## H6 — Implementation Gate
Production implementation allowed only if:
- `PROJECT_STATUS.md` unblocks it;
- `PRODUCTION_CODING_START_GATE.md` passes for the task;
- relevant Deep Design is current, not stale;
- unresolved P0 ambiguity is zero;
- required spike evidence exists;
- tests/acceptance are specified;
- model-driven nodes comply with ADR-009 or have an explicit waiver.

Otherwise return `BLOCKED_BY_DESIGN`, `BLOCKED_BY_SPIKE`, or `STALE_DERIVED_ARTIFACT` and do not write production code.

---

## H7 — Execute with Minimum Necessary Agency

Default Phase 1 hot path is deterministic:

```text
Source adapters
 -> Normalization
 -> Evidence/Verification rules
 -> MintCampaign/MintStage state
 -> Scoring formula + hard gates
 -> Decision rules
 -> Transactional outbox
 -> Telegram renderer
```

Conditional model-driven roles:
- unstructured signal/claim extraction
- ambiguous entity resolution after deterministic rules fail
- Phase 2 Quest parsing

Independent critique is isolated from the builder path.

No central LLM chooses among all pipeline roles.

---

## H8 — Verification
Feature completion requires one or more suitable paths:
- unit test
- schema/contract test
- integration fixture
- dry-run event
- sandbox/live provider response where appropriate
- observable Telegram test

Required result:
- tests/checks run
- expected
- actual
- failures
- residual risks
- evidence refs

### Independent review input
When used, reviewer receives:
- artifact
- requirements
- constraints
- acceptance criteria
- verification evidence

Builder rationale/self-justification is not included by default.

---

## H9 — State / Deviation / Stale Propagation
After meaningful work:
- update canonical state, not conversation memory;
- record plan drift when execution differed;
- preserve old decisions/provenance;
- if an authority changed, update all affected derived artifacts or mark them `STALE` and block the dependent gate.

Plan drift record belongs in `docs/deviations/CHANGELOG_DECISIONS.md`.

---

# Logical Role Contracts

## Discovery Extraction
**Default mechanism:** adapter + deterministic filter; narrow LLM extraction only for unstructured content.

Goal: find candidate projects/opportunities early.

Must not:
- assert official mint/WL instructions from T3/T4 alone;
- recommend action without verification state.

Output minimum:
- project candidate
- source/tier
- discovered_at
- raw signal ref
- candidate type
- extracted claims/links
- confidence
- required verification

## Verification
**Default mechanism:** deterministic evidence/trust/link rules; narrow ambiguity fallback only.

Output minimum:
- claim
- supporting/conflicting evidence
- source tier
- official identity status
- CTA/link safety status
- confidence
- expiry/recheck

## Entity Resolution
**Default mechanism:** deterministic exact/official-link/contract relations first; model fallback only when unresolved.

Must never merge solely on similar names/logos, influencer claims, or wallet overlap.

## Campaign / Stage State
**Default mechanism:** deterministic state machine.

Goal: maintain `MintCampaign`, `MintStage`, and action-oriented `Opportunity` state without illegal transitions.

Must reject clock-only `MINT_OPEN` unless current evidence supports it.

## Scoring
**Default mechanism:** deterministic versioned formula.

Output minimum:
- quality
- alpha
- effort
- risk
- evidence confidence
- action score/grade
- hard gate
- component evidence/reasons

Must not raise Quality solely from influencer/famous-wallet involvement.

## Wallet Intelligence
**Default mechanism:** deterministic/query analytics (RPC/indexer/Dune etc.).

Output minimum:
- wallet/cohort identifiers
- identity confidence
- signal timing/type
- independence assessment
- wash/sybil/conflict flags
- strength

## Quest Parsing — Phase 2
**Default mechanism:** structured platform data first; narrow parser skill/model for unstructured requirements.

Output minimum:
- required/optional tasks
- stage/campaign relation
- deadline
- FCFS/raffle/guaranteed/holder semantics
- external platform
- wallet/social/Discord dependency
- manual-action requirement

Never execute social engagement or wallet action.

## User Progress — Phase 2+
**Default mechanism:** explicit user/provider state, deterministic.

Do not infer completion from recommendation or planned work.

## Decision
**Default mechanism:** deterministic thresholds/rules.

Output minimum:
- WATCH / APPLY_WL / PREPARE / MINT_RECHECK / AVOID / NO_ALERT
- urgency/severity
- reasons
- confidence
- next user action
- missing information
- safe CTA or null

## Telegram Renderer
**Default mechanism:** deterministic template.

Must include when known:
- project/campaign/stage
- grade/component scores
- current state
- KST deadline
- next action
- evidence confidence
- verified/consistent CTA only
- risk flags

Must not include an unverified/quarantined wallet-impacting CTA or routine no-change spam.

## Independent Critic
**Mechanism:** isolated reviewer when warranted.

Goal:
- test artifact against requirements/constraints/acceptance/evidence;
- identify undefined safety/governance terms and test weaker readings;
- avoid anchoring on builder rationale.

---

# Fixture Families
Minimum families before production trust:
1. official X allowlist
2. PREMINT social-task raffle
3. Galxe WL reward
4. Discord level requirement
5. phishing impersonation
6. edited mint date
7. conflicting official dates
8. famous wallet + weak project
9. 3 independent alpha wallets
10. wash-like cluster
11. snapshot already passed
12. free mint contract unlinked
13. multi-stage GTD/FCFS/Public mint
14. ERC-20-priced mint stage
15. explicit free stage
16. compromised official social account with hostile new domain
17. official disavowal/revocation

Canonical expected cases live in `EVAL_FIXTURES.md`; do not maintain divergent outcome copies here.

---

# Error Taxonomy
- `SOURCE_UNAVAILABLE`
- `AUTH_REQUIRED`
- `PERMISSION_REQUIRED`
- `RATE_LIMITED`
- `STALE_EVIDENCE`
- `STALE_DERIVED_ARTIFACT`
- `IDENTITY_UNCERTAIN`
- `CONFLICTING_OFFICIAL_SOURCES`
- `UNVERIFIED_LINK`
- `CTA_QUARANTINED`
- `PHISHING_SUSPECTED`
- `SCHEMA_PARSE_FAILED`
- `DUPLICATE_EVENT`
- `STATE_TRANSITION_REJECTED`
- `COST_BUDGET_EXCEEDED`
- `BLOCKED_BY_DESIGN`
- `BLOCKED_BY_SPIKE`
- `SAFETY_BOUNDARY`
- `TELEGRAM_DELIVERY_FAILED`
- `PROVIDER_DEGRADED`

---

# Harness Completion Criteria
Harness is executable-in-design only when:
- logical role contracts exist;
- each role has a chosen implementation mechanism (direct/rule/skill/agent/deterministic service);
- typed schemas are synchronized with current accepted domain ADRs;
- fixture/golden outcomes cover current hard-safety rules;
- failure/stop conditions exist;
- local action-space rules are satisfied or explicitly waived;
- phase gates are checklist/machine-checkable;
- validation output is standardized;
- at least one credential-free end-to-end dry run exists;
- stale derived artifacts relevant to the gate are zero.
