# Project Status

## Current verdict

**설계 골격 완료 / Deep Design v1 완료 / 정책형 Harness 완료 / Executable Harness 사양 완료 / Credential-free 설계 Dry-run 완료 / Provider Paper Validation 완료 / Operational Spike 1차 검증 완료(부분) / Credential-dependent 실측 미완료 / Harness Runner·본 구현 미착수 / Production Coding BLOCKED**

This is the authoritative readiness statement until credential-dependent spike results are completed.

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
- primary user/JTBD/non-goals
- initial chains: Ethereum + Base
- canonical schemas/event normalization/evidence policy
- identity merge/split and conflict resolution
- opportunity state machine
- explainable scoring and hard safety gates
- wallet cohort/AlphaWalletScore design
- WL/Quest/UserProgress future contracts
- Telegram alert/dedup/re-alert design
- PostgreSQL durable state + transactional outbox
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
- per-agent logical typed I/O contracts
- confidence/error taxonomy
- prompt-injection boundary
- stop/fail conditions
- 20 golden fixture families
- hard safety regression rules
- credential-free end-to-end design dry run

Important distinction:
**Harness specification is complete; executable runner/test code does not exist yet.**

### 5. ADRs — ACTIVE
- ADR-001 Alpha Radar architecture
- ADR-002 Phase 1 scope and source degradation
- ADR-003 PostgreSQL persistence + transactional notification outbox
- ADR-004 explainable scoring + hard safety gates
- ADR-005 hybrid runtime topology class

### 6. Operational Spike first-pass validation — COMPLETE AS FAR AS CURRENT CREDENTIALS/ENVIRONMENT ALLOW
Result artifacts under `docs/spikes/` now exist.

- `SPIKE-X-001`: **PAPER_VALIDATED / OPERATIONAL_BLOCKED_BY_CREDENTIAL_AND_CONSOLE_PRICING**
  - stream/search technically feasible;
  - actual spend/latency still needs X developer credentials and console pricing.
- `SPIKE-MARKET-001`: **PAPER_VALIDATED / OPERATIONAL_BLOCKED_BY_EXECUTION_ENVIRONMENT**
  - OpenSea upcoming-drop API/stage mapping is suitable on paper;
  - current execution environment could not resolve the API host for a live call.
- `SPIKE-CAMPAIGN-001`: **PAPER_VALIDATED / MIXED_OPERATIONAL_ACCESS**
  - Galxe has supported GraphQL API but needs token;
  - PREMINT Connect is optional partner-key access;
  - Guild begins as public-reference/manual fallback until a supported read API is confirmed.
- `SPIKE-TG-001`: **PAPER_VALIDATED / OPERATIONAL_BLOCKED_BY_USER_CREDENTIALS**
  - Bot API contract is suitable;
  - actual one-message delivery still needs a user-created bot token/chat id.
- `SPIKE-DUNE-001`: **PAPER_VALIDATED / OPERATIONAL_BLOCKED_BY_API_KEY**
  - Dune is suitable for optional Phase 1.5 with cached-first/budget-capped policy.
- `SPIKE-RUNTIME-001`: **PAPER_VALIDATED / TOPOLOGY CLASS RESOLVED**
  - GitHub Actions cron-only rejected for real-time ingestion;
  - hybrid topology accepted in ADR-005;
  - concrete hosting provider depends on final X mode/budget.
- `SPIKE-DISCORD-001`: **PAPER_VALIDATED / SERVER_OPT_IN_REQUIRED**
  - Phase 3 is server-opt-in/partial only; no self-bots or arbitrary third-party server reads.

## What is NOT complete

### Credential-dependent operational evidence — REQUIRED FOR PHASE 1 GATE
- [ ] X Developer Console pricing + real stream/search trial.
- [ ] Live OpenSea upcoming-drop response/coverage sample from an environment with outbound network access.
- [ ] Galxe token live query (PREMINT/Guild remain optional fallbacks).
- [ ] Telegram bot dry-run delivered to the user's chat.
- [ ] Concrete low-latency hosting provider/cost selected after X mode is known.

### Optional later-phase evidence
- [ ] Dune real query credit/freshness measurement (Phase 1.5).
- [ ] Discord authorized test-server read trial (Phase 3).

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

These remain implementation artifacts.

## Coding policy

### Production feature code
**BLOCKED.**

### Executable harness implementation
**BLOCKED** until the required Phase 1 credential-dependent operational evidence above resolves provider/runtime packaging assumptions.

### Technical spikes
**UNBLOCKED.**
No production code is allowed to leak out of spike work.

## Phase 1 implementation exit gate
- [x] Deep Design v1 complete.
- [x] Harness contracts/schemas complete.
- [x] Fixture/eval/golden-output plan complete.
- [x] Security boundaries testable in design.
- [x] MVP domain/source scope fixed.
- [x] Runtime/API cost guardrail model documented.
- [x] Phase 1 success criteria measurable.
- [x] No unresolved P0 core domain/trust-model ambiguity.
- [x] Runtime topology class selected (hybrid; ADR-005).
- [ ] X operational mode/cost resolved or X explicitly downgraded to optional.
- [ ] OpenSea live mapping/coverage sample completed.
- [ ] Galxe live API path confirmed or explicitly downgraded to optional.
- [ ] Telegram real delivery completed.
- [ ] Concrete low-latency runtime/provider cost selected.
- [ ] No unresolved P0 provider feasibility ambiguity.

## Next action
**Do not implement the production radar yet.**
The next work is credential/configuration-assisted validation only: X, OpenSea, Galxe, Telegram, then final runtime provider selection. Dune and Discord do not block Phase 1.
