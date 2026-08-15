# Project Status

## Current verdict

**설계 골격 완료 / Deep Design v1 완료 / 정책형 Harness 완료 / Executable Harness 사양 완료 / Credential-free 설계 Dry-run 완료 / Provider Paper Validation 완료 / Operational Spike 2차 검증 완료(부분) / P0 실측 4건 미완료 / Harness Runner·본 구현 미착수 / Production Coding BLOCKED**

This is the authoritative readiness statement until the remaining P0 operational evidence is completed.

## Complete

### Product / Deep Design
- Phase 1–4 boundaries fixed.
- Ethereum + Base fixed as initial chains.
- Project, Source, Evidence, Opportunity, Quest, UserProgress, WalletEntity, InfluencerEntity and Notification contracts defined.
- Discovery vs verification and T0–T4 trust tiers defined.
- event normalization, identity merge/split, evidence versioning/conflict handling defined.
- opportunity state machine defined.
- explainable Quality/Alpha/Effort/Risk scoring and hard safety gates defined.
- wallet cohort/AlphaWalletScore design defined.
- PostgreSQL durable state + transactional notification outbox selected.
- UTC storage/KST presentation, retry/rate-limit/degradation/retention/observability rules defined.

### Harness design
- `CLAUDE.md` policy harness complete.
- H0–H8 execution gates defined.
- logical typed agent I/O contracts defined.
- prompt contracts and prompt-injection boundary defined.
- 20 golden fixture families defined.
- credential-free end-to-end design dry run complete.

Important: executable harness/test runner code does not exist yet by design.

### Source/provider decisions
- X: technically feasible; actual mode/cost unresolved.
- OpenSea: P0 structured marketplace/drop source retained.
- Galxe: supported API adapter, but optional/degradable.
- PREMINT: optional partner API, not a hard dependency.
- Guild: public-reference/manual fallback initially.
- Dune: optional Phase 1.5 cached-first wallet intelligence.
- Discord: Phase 3 server-opt-in/partial only.
- Telegram: primary notification destination.

### Runtime topology
ADR-005 accepts a hybrid topology class:
- urgent/stream ingestion -> persistent or event-capable low-latency runtime;
- durable state/outbox -> PostgreSQL;
- GitHub Actions -> non-critical batch/reconciliation/evals only.

Cron-only GitHub Actions is rejected for real-time ingestion because scheduled jobs can be delayed or dropped under load.

## Operational validation status
See:
- `docs/spikes/OPERATIONAL_VALIDATION-2026-08-15.md`
- individual `docs/spikes/SPIKE-*-RESULT.md`
- `docs/CREDENTIAL_READINESS.md`

### Resolved enough for architecture
- [x] Campaign-platform degradation model.
- [x] Dune optionality / cached-first policy.
- [x] Discord server-opt-in boundary.
- [x] Hybrid runtime topology class.
- [x] OpenSea API contract/schema suitability on first-party docs.
- [x] Telegram protocol suitability on first-party docs.

### Remaining P0 operational evidence
1. **X real access/cost**
   - Developer app/Bearer token
   - current Developer Console endpoint prices
   - small stream/search trial
   - observed latency/volume
   - projected spend
   - final mode: STREAM_PRIMARY / SEARCH_PRIMARY / HYBRID / X_OPTIONAL

2. **OpenSea live sample/coverage**
   - live `upcoming` Ethereum/Base response from a network-capable runtime
   - 10+ drop mappings
   - manual coverage comparison

   Current disposable attempt failed because this execution environment could not resolve `api.opensea.io`; this is `ENVIRONMENT_BLOCKED`, not provider failure.

3. **Telegram actual delivery**
   - user-created bot token
   - user sends `/start`
   - target chat id
   - exactly one dry-run message delivered and provider result recorded

4. **Concrete low-latency hosting choice/cost**
   - choose provider only after X final mode is known
   - verify monthly cost and always-on/stream support if required

### Non-P0 / later adapter evidence
- [ ] Galxe live access-token query before enabling Galxe adapter in production.
- [ ] Dune real query credit/freshness measurement — Phase 1.5.
- [ ] Discord authorized test-server read — Phase 3.

## Credential visibility limitation
The connected GitHub integration can modify repository contents but cannot list repository Actions secrets; the attempted secrets-list endpoint returned `403 Resource not accessible by integration`.

Therefore this project must not claim that any X/Telegram/OpenSea/Galxe/Dune/Discord secret is already configured unless verified outside this connector.

## Coding policy

### Production feature code
**BLOCKED.**

### Executable harness implementation
**BLOCKED** until remaining P0 operational evidence is resolved or explicitly waived by ADR.

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
- [x] Campaign adapters can degrade without changing architecture.
- [ ] X operational mode/cost resolved or explicitly downgraded to optional.
- [ ] OpenSea live sample/coverage completed.
- [ ] Telegram real delivery completed.
- [ ] Concrete low-latency hosting/cost selected.
- [ ] No unresolved P0 provider feasibility ambiguity.

## Next action
Do not implement the production radar yet. Finish the four remaining P0 operational validations. Galxe/Dune/Discord do not block Phase 1.
