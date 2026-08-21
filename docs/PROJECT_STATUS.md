# Project Status

## Current verdict

**설계 골격 완료 / Deep Design v1 완료 / 정책형 Harness 완료 / Executable Harness 사양 완료 / Credential-free 설계 Dry-run 완료 / Provider Paper Validation 완료 / Operational Spike 2차 검증 완료(부분) / Runtime Provider 결정 완료 / P0 실측 3건 미완료 / Harness Runner·본 구현 미착수 / Production Coding BLOCKED**

This is the authoritative readiness statement until the remaining three P0 operational validations are completed.

## Authority and start-gate rule
- `CLAUDE.md` defines the mandatory recovery/gate workflow.
- `docs/PRODUCTION_CODING_START_GATE.md` is the authoritative production-coding start gate.
- A new session must recover current state and continue from the first incomplete gate; completed Deep Design must not be restarted without new P0 evidence.
- Paper/provider-document validation must not be treated as observed operational validation.
- Spike code remains disposable/isolated and cannot silently become production code.
- After required spikes, results must be reconciled into design/ADRs/status before `PHASE_1_CODING_READY` is declared.

Current gate state: **`SPIKE_REQUIRED / PRODUCTION CODING BLOCKED`**.

## Complete

### Product / Deep Design
- Phase 1–4 boundaries fixed.
- Ethereum + Base fixed as initial chains.
- canonical Project/Source/Evidence/Opportunity/Quest/UserProgress/WalletEntity/InfluencerEntity/Notification contracts defined.
- discovery vs verification and T0–T4 trust tiers defined.
- event normalization, identity merge/split, evidence versioning/conflict handling defined.
- opportunity state machine defined.
- explainable Quality/Alpha/Effort/Risk scoring and hard safety gates defined.
- wallet cohort/AlphaWalletScore design defined.
- PostgreSQL durable state + transactional notification outbox selected.
- UTC/KST, retry/rate-limit/degradation/retention/observability rules defined.

### Harness design
- `CLAUDE.md` policy harness complete.
- H0–H8 execution gates defined.
- logical typed agent I/O contracts defined.
- prompt contracts/prompt-injection boundary defined.
- 20 golden fixture families defined.
- credential-free end-to-end design dry run complete.

Executable harness/test runner code does not exist yet by design.

### Source/provider decisions
- X: technically feasible; actual mode/cost unresolved.
- OpenSea: P0 structured marketplace/drop source retained.
- Galxe: supported API adapter, optional/degradable.
- PREMINT: optional partner API.
- Guild: public-reference/manual fallback initially.
- Dune: optional Phase 1.5 cached-first wallet intelligence.
- Discord: Phase 3 server-opt-in/partial only.
- Telegram: primary notification destination.

### Runtime provider — RESOLVED
ADR-005 defines hybrid topology.
ADR-006 selects **Railway** as the Phase 1 MVP runtime target.

Target:
- Railway `radar-worker` for persistent stream or polling;
- Railway PostgreSQL for canonical state + outbox;
- GitHub Actions only for non-critical batch/reconciliation/eval.

Current official Railway pricing model used for the decision:
- Hobby target: $5/month minimum applied toward resource usage;
- usage-based CPU/RAM/storage/egress;
- configure a compute hard limit before production traffic.

No Railway account activation, purchase or deployment has been performed during this no-coding validation phase.

## Operational validation artifacts
See:
- `docs/spikes/OPERATIONAL_VALIDATION-2026-08-15.md`
- `docs/CREDENTIAL_READINESS.md`
- individual `docs/spikes/SPIKE-*-RESULT.md`

## Remaining P0 operational evidence — ONLY THREE

### 1. X real access/cost
Needed:
- X Developer app/Bearer token;
- current Developer Console endpoint prices;
- small stream/search trial;
- observed latency and delivered volume;
- spend projection;
- final mode: `STREAM_PRIMARY`, `SEARCH_PRIMARY`, `HYBRID`, or `X_OPTIONAL`.

### 2. OpenSea live sample/coverage
Needed:
- live `upcoming` Ethereum/Base response;
- 10+ drop mappings to canonical Opportunity;
- manual coverage comparison.

Current disposable attempt failed because this execution environment could not resolve `api.opensea.io`. This is `ENVIRONMENT_BLOCKED`, not provider failure. Official docs confirm a no-signup instant free-tier API-key path.

### 3. Telegram actual delivery
Needed:
- user-created bot token;
- user sends `/start`;
- target chat id;
- one dry-run alert delivered once and provider result recorded.

## Non-P0 / later adapter evidence
- [ ] Galxe live access-token query before enabling Galxe adapter in production.
- [ ] Dune real query credit/freshness measurement — Phase 1.5.
- [ ] Discord authorized test-server read — Phase 3.
- [ ] Railway account/outbound-connectivity activation check before actual deployment.

## Credential visibility limitation
The connected GitHub integration cannot list repository Actions secrets; the attempted list endpoint returned `403 Resource not accessible by integration`.
Secret presence must not be guessed.

## Coding policy

### Production feature code
**BLOCKED.**

### Executable harness implementation
**BLOCKED** until the remaining P0 operational evidence is resolved or explicitly waived by ADR.

### Technical spikes
**UNBLOCKED.** No spike artifact may silently become production code.

## PHASE_1_CODING_READY gate
- [x] Deep Design v1 complete.
- [x] Harness contracts/schemas complete.
- [x] Fixture/eval/golden-output plan complete.
- [x] Security boundaries testable in design.
- [x] MVP scope fixed.
- [x] Runtime/API cost guardrail model documented.
- [x] Phase 1 success criteria measurable.
- [x] No unresolved P0 domain/trust-model ambiguity.
- [x] Runtime topology class selected.
- [x] Concrete MVP runtime provider target selected (Railway).
- [x] Campaign adapters can degrade without changing architecture.
- [ ] X operational mode/cost resolved or X explicitly downgraded to optional.
- [ ] OpenSea live sample/coverage completed.
- [ ] Telegram real delivery completed.
- [ ] Spike results reconciled into canonical design/ADRs/status.
- [ ] No unresolved P0 provider feasibility ambiguity.

## Next action
Do not implement the production radar yet. Finish the three remaining P0 operational validations: X, OpenSea live sample, Telegram dry-run. Then reconcile results through `docs/PRODUCTION_CODING_START_GATE.md`. Galxe/Dune/Discord do not block Phase 1.
