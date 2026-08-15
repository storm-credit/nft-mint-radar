# Project Status

## Current verdict

**설계 골격 완료 / Source·Blind-spot 1차 완료 / Deep Design 미완료 / 정책형 Harness 1차 완료 / 실행형 Harness 미완료 / 본 구현 금지 / 기술 Spike 전 단계**

This is the authoritative readiness statement until the exit criteria below are met.

## What is complete

### 1. Product/architecture skeleton — COMPLETE
- Phase 1–4 boundaries exist.
- Core entities are identified: Project, Source, Evidence, Opportunity, Quest, UserProgress, WalletEntity, InfluencerEntity, Notification.
- Discovery and verification are explicitly separated.
- Trust tiers T0–T4 exist.
- Dune/wallet cohort and influencer roles are separated from official verification.
- Telegram is defined as the primary notification destination.

### 2. Source strategy / blind-spot sweep — FIRST PASS COMPLETE
- X, official sites, PREMINT, Galxe, Guild, marketplaces, on-chain, Dune, Discord, Telegram, Reddit and optional analytics sources are classified.
- Famous-wallet and influencer traps are documented.
- Discord/X automation safety boundaries are documented.
- Source ROI and time-to-alpha metrics are identified.

### 3. Policy harness — FIRST PASS COMPLETE
`CLAUDE.md` defines:
- intent check
- blind-spot sweep
- trap check
- four-option design
- ADR requirement
- smallest-slice implementation
- validation-before-completion
- deviation logging
- phase boundaries
- security boundaries
- meta-prompting workflow

## What is NOT complete

### Deep Design — INCOMPLETE
The following are still required before production implementation:
- canonical event schema
- source adapter contract
- evidence schema and evidence conflict resolution
- project identity/entity resolution rules
- opportunity state-machine transitions
- quest schema and parser contract
- scoring formulas and calibration policy
- notification severity/urgency thresholds
- deduplication/fingerprint rules
- recheck scheduling policy
- stale evidence/expiry policy
- persistence/storage decision
- API/runtime cost budget
- retry/backoff/rate-limit policy
- source failure/degradation behavior
- chain/marketplace scope for MVP
- timezone/deadline semantics
- secret/config contract
- observability/logging requirements
- data retention policy
- safety gate before actionable mint links

### Executable Harness — INCOMPLETE
Policies exist, but the harness is not yet executable. Missing:
- per-agent role contracts
- typed input/output schemas
- fixtures representing real NFT announcements and WL quests
- golden expected outputs
- prompt/eval suite
- confidence/error taxonomy
- stop/fail/escalation conditions
- source verification test cases
- phishing/link-rewrite test cases
- duplicate-alert tests
- state-transition tests
- scoring regression tests
- dry-run Telegram payload tests
- cost/latency budget assertions
- phase-gate checklist usable by an agent before coding

## Coding policy

### Production feature code
**BLOCKED** until Deep Design and Executable Harness design reach their exit criteria.

### Technical spikes
Allowed only after the spike contract is documented. A spike must:
1. answer one uncertain technical question;
2. have a clear success/failure condition;
3. be disposable or isolated;
4. not become production architecture by accident;
5. produce a written decision/evidence record.

Likely spikes after design completion:
- X access/cost/rate-limit feasibility
- PREMINT/Galxe/Guild accessible-data feasibility
- Telegram Bot delivery end-to-end
- Dune query/API latency and credit-cost feasibility
- Discord permitted-read integration feasibility
- marketplace/API coverage for selected chains

## Exit gate to start Phase 1 implementation
All must be true:
- [ ] Deep Design checklist complete or explicitly waived in an ADR.
- [ ] Harness contracts/schemas complete.
- [ ] Fixture/eval plan complete.
- [ ] Security boundaries testable.
- [ ] MVP source scope fixed.
- [ ] Runtime/API cost assumptions documented.
- [ ] Required technical spikes completed and recorded.
- [ ] Phase 1 success criteria measurable.
- [ ] No unresolved P0 architecture ambiguity.

## Next action
Do not build collectors yet. Complete `DEEP_DESIGN_CHECKLIST.md` and `HARNESS_SPEC.md`, then run only the narrow technical spikes required to remove unresolved architecture uncertainty.
