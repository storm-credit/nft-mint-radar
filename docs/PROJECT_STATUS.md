# Project Status

## Current verdict

**설계 골격 완료 / Source·Blind-spot 1차 완료 / Deep Design v1 완료 / 정책형 Harness 완료 / Executable Harness 사양 완료 / Credential-free 설계 Dry-run 완료 / Provider Paper Validation 완료 / Operational Spikes 미완료 / Harness Runner·본 구현 미착수 / Production Coding BLOCKED**

This is the authoritative readiness statement until the required spike results are recorded.

## What is complete

### 1. Product/architecture skeleton — COMPLETE
- Phase 1–4 boundaries exist.
- Core entities are defined: Project, Source, Evidence, Opportunity, Quest, UserProgress, WalletEntity, InfluencerEntity, Notification.
- Discovery and verification are explicitly separated.
- Trust tiers T0–T4 exist.
- Dune/wallet cohort and influencer roles are separate from official verification.
- Telegram is the primary notification destination.

### 2. Source strategy / blind-spot sweep — FIRST PASS COMPLETE
- X, official sites, PREMINT, Galxe, Guild, OpenSea, on-chain, Dune, Discord, Telegram, Reddit and optional analytics sources are classified.
- Famous-wallet and influencer traps are documented.
- Discord/X automation safety boundaries are documented.
- Source ROI and time-to-alpha metrics are defined.

### 3. Deep Design v1 — COMPLETE IN DESIGN
Authoritative documents:
- `docs/DEEP_DESIGN.md`
- `docs/SOURCE_ADAPTER_CONTRACTS.md`
- `docs/WALLET_INTELLIGENCE_SPEC.md`
- `docs/METRICS_SLO.md`
- `docs/DEEP_DESIGN_CHECKLIST.md`

Decided:
- Phase 1 primary user/JTBD/non-goals
- initial chains: Ethereum + Base
- provider-neutral canonical schemas
- event normalization/dedup/edit handling
- evidence versioning and conflict policy
- project identity merge/split policy
- verification and CTA safety gates
- opportunity state machine
- scoring formula/thresholds/hard gates
- wallet cohort/AlphaWalletScore design
- WL/Quest/UserProgress future contracts
- Telegram severity/re-alert/fingerprint design
- PostgreSQL persistence semantics + notification outbox
- retries/rate limits/source degradation
- UTC storage/KST presentation
- secret/link safety/retention/observability

### 4. Harness design — COMPLETE
Authoritative documents:
- `CLAUDE.md`
- `docs/HARNESS_SPEC.md`
- `docs/HARNESS_SCHEMAS.md`
- `docs/PROMPT_CONTRACTS.md`
- `docs/EVAL_FIXTURES.md`
- `docs/HARNESS_DRY_RUN.md`

Defined:
- H0–H8 workflow gates
- per-agent typed logical I/O contracts
- confidence/error taxonomy
- prompt-injection boundary
- stop/fail conditions
- 20 fixture families with golden outcomes
- hard safety regression rules
- credential-free end-to-end design dry run

Important distinction:
**Harness specification is complete; an executable harness runner/test implementation does not exist yet.** This is intentional because the current work order forbids production coding before spike validation.

### 5. ADRs — ACTIVE
- ADR-001 Alpha Radar architecture
- ADR-002 Phase 1 scope and source degradation
- ADR-003 PostgreSQL persistence + transactional notification outbox
- ADR-004 explainable scoring + hard safety gates

### 6. Provider paper validation — COMPLETE
`docs/spikes/PAPER_VALIDATION-2026-08-15.md` records current first-party documentation findings.

Confirmed at design level:
- OpenSea exposes upcoming-drop/drop-detail APIs.
- Galxe exposes structured Quest/eligibility GraphQL APIs.
- PREMINT Connect is partner/access-gated and cannot be assumed mandatory.
- Guild requirement logic must preserve ALL/ANY/X-of-Y and negative conditions.
- X provides stream/search but cost must be measured in the real Developer Console.
- Dune supports latest-results + explicit executions with credit costs.
- Discord content/member reads depend on bot installation/privileged intents.
- Telegram `sendMessage` is suitable for MVP notifications.

## What is NOT complete

### Operational Spikes — REQUIRED
Contracts exist in `docs/SPIKE_PLAN.md`, results do not yet exist:
- [ ] `SPIKE-X-001` — X access/cost/latency
- [ ] `SPIKE-MARKET-001` — OpenSea coverage/mapping
- [ ] `SPIKE-CAMPAIGN-001` — Galxe/PREMINT/Guild operational access
- [ ] `SPIKE-TG-001` — actual Telegram bot delivery
- [ ] `SPIKE-DUNE-001` — Dune freshness/credit cost (Phase 1.5 optional)
- [ ] `SPIKE-RUNTIME-001` — Actions/serverless/worker/hybrid topology
- [ ] `SPIKE-DISCORD-001` — server-opt-in read feasibility (Phase 3 gate, not Phase 1 blocker)

### Executable harness/runtime code — NOT STARTED
Missing by design:
- concrete JSON Schema/Pydantic models
- fixture files under tests
- fixture/eval runner
- prompt runner
- provider adapters
- database migrations/repositories
- scheduler/workers
- Telegram outbox sender
- CI validation workflow

These are implementation artifacts and remain blocked until required Phase 1 spikes resolve.

## Coding policy

### Production feature code
**BLOCKED.**

### Executable harness implementation
Also **BLOCKED until required Phase 1 provider/runtime spikes resolve**, because source contracts/runtime topology could affect implementation packaging. The logical harness itself is fully specified.

### Technical spikes
**UNBLOCKED.**
Each spike must obey `docs/SPIKE_PLAN.md` and produce a result document. Disposable spike code/scripts must be isolated and must not become production architecture by accident.

## Phase 1 implementation exit gate
All required to switch status to `PHASE_1_CODING_READY`:
- [x] Deep Design v1 complete.
- [x] Harness contracts/schemas complete.
- [x] Fixture/eval/golden-output plan complete.
- [x] Security boundaries testable in design.
- [x] MVP domain/source scope fixed.
- [x] Runtime/API cost guardrail model documented.
- [x] Phase 1 success criteria measurable.
- [x] No unresolved P0 core domain/trust-model ambiguity.
- [ ] Required Phase 1 operational spikes completed and recorded.
- [ ] Runtime topology ADR accepted after spike.
- [ ] No unresolved P0 provider feasibility ambiguity.

## Next action
**Do not implement the production radar yet. Run the required operational spikes in order:**
1. X
2. OpenSea/marketplace
3. campaign platforms
4. Telegram
5. runtime topology

Dune can follow as Phase 1.5 if desired; Discord is a Phase 3 gate.

After those results, update ADRs/status to `PHASE_1_CODING_READY`, then implement the harness runner and Phase 1 smallest working slice under the already-defined contracts.
