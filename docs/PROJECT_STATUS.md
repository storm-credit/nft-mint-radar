# Project Status

## Current verdict

**설계 골격 완료 / Deep Design v1.1 PATCH 완료 / Blind-Spot 재검증 완료 / 정책형 Harness 완료 / Executable Harness 사양 완료 / Credential-free 설계 Dry-run 완료 / Provider Paper Validation 완료 / Runtime Provider 결정 완료 / P0 실측 3건 미완료 / Harness Runner·본 구현 미착수 / Production Coding BLOCKED**

This is the authoritative readiness statement after the 2026-08-22 blind-spot re-audit.

## Authority and start-gate rule
- `CLAUDE.md` defines mandatory recovery/gate workflow.
- `docs/PRODUCTION_CODING_START_GATE.md` is the authoritative production-coding start gate.
- `docs/BLIND_SPOT_SWEEP_2026-08-22.md` is the latest targeted Red Team audit.
- ADR-007 and ADR-008 override older chain/price/stage/CTA assumptions where they conflict.
- A new session continues from the first incomplete gate; completed design is not restarted without new P0 evidence.
- Paper validation never counts as operational validation.
- Spike artifacts remain disposable/isolated and cannot silently become production code.

Current gate state: **`SPIKE_REQUIRED / PRODUCTION CODING BLOCKED`**.

## Complete

### Product / Deep Design v1.1
- Phase 1–4 boundaries fixed.
- Phase 1 EVM target set fixed to **Ethereum + Base + Robinhood Chain** by ADR-007.
- canonical Project/Source/Evidence/Opportunity/Quest/UserProgress/WalletEntity/InfluencerEntity/Notification contracts defined.
- ADR-008 adds canonical `AssetAmount`, `MintCampaign`, `MintStage`, explicit `price_state`, and independent CTA safety state.
- legacy-reactivation signals are explicitly modeled: `PROJECT_REACTIVATED`, `CHAIN_MIGRATION_ANNOUNCED`, `LEGACY_HOLDER_ACCESS_ANNOUNCED`.
- discovery vs verification and T0–T4 trust tiers defined.
- source identity trust is now explicitly separated from wallet-impacting CTA link safety.
- event normalization, identity merge/split, evidence versioning/conflict handling defined.
- opportunity/state semantics and stage-specific mint representation defined.
- explainable Quality/Alpha/Effort/Risk scoring and hard safety gates defined.
- wallet cohort/AlphaWalletScore design defined.
- PostgreSQL durable state + transactional notification outbox selected.
- UTC/KST, retry/rate-limit/degradation/retention/observability rules defined.

### Latest Blind-Spot Red Team
`docs/BLIND_SPOT_SWEEP_2026-08-22.md` found four P0 issues and patched them without architecture reset:
1. Robinhood Chain missing from Phase 1 scope.
2. Official social identity was too easily conflated with CTA safety.
3. Native-only mint-price model could not represent ERC-20-priced mints.
4. Single-stage Opportunity model was insufficient for GTD/FCFS/community/public mint stages.

P1 findings recorded:
- OpenSea calendar is useful but not coverage-complete alpha discovery;
- factory deployer attribution can mislead wallet intelligence;
- future AlphaWallet scoring must avoid survivorship/look-ahead bias;
- Phase 2 requires first-class manual/user-confirmed progress states.

Architecture verdict remains **KEEP + targeted PATCH**, not NEW DESIGN.

### Harness design
- `CLAUDE.md` policy harness complete.
- H0–H8 execution gates defined.
- logical typed agent I/O contracts defined.
- prompt contracts/prompt-injection boundary defined.
- existing golden fixture families defined; ADR-008 requires additional multi-stage/ERC20/compromised-official-channel fixtures before runner freeze.
- credential-free end-to-end design dry run complete.

Executable harness/test runner code does not exist yet by design.

### Source/provider decisions
- X: technically feasible; actual mode/cost unresolved.
- OpenSea: P0 structured drop/stage source retained, but **not treated as coverage-complete discovery**.
- Galxe: supported API adapter, optional/degradable.
- PREMINT: optional partner API.
- Guild: public-reference/manual fallback initially.
- Dune: optional Phase 1.5 cached-first wallet intelligence.
- Discord: Phase 3 server-opt-in/partial only.
- Telegram: primary notification destination.

### Runtime provider — RESOLVED
ADR-005 defines hybrid topology.
ADR-006 selects **Railway** as Phase 1 MVP runtime target.

Target:
- Railway `radar-worker` for persistent stream or polling;
- Railway PostgreSQL for canonical state + outbox;
- GitHub Actions only for non-critical batch/reconciliation/eval.

No Railway account activation, purchase or deployment has been performed during the no-production-coding validation phase.

## Operational validation artifacts
See:
- `docs/spikes/OPERATIONAL_VALIDATION-2026-08-15.md`
- `docs/CREDENTIAL_READINESS.md`
- individual `docs/spikes/SPIKE-*-RESULT.md`

## Remaining P0 operational evidence — THREE

### 1. X real access/cost
Needed:
- X Developer app/Bearer token;
- current Developer Console endpoint prices;
- small stream/search trial;
- observed latency and delivered/noise volume;
- spend projection;
- final mode: `STREAM_PRIMARY`, `SEARCH_PRIMARY`, `HYBRID`, or `X_OPTIONAL`.

### 2. OpenSea live sample/coverage
Needed:
- live `upcoming` sample across **Ethereum + Base + Robinhood Chain**;
- 10+ real drops mapped through `MintCampaign`/`MintStage` and asset-aware pricing;
- at least one allowlist-stage case and, if present, ERC-20-priced case;
- manual comparison against opportunities discovered outside OpenSea to quantify calendar coverage gaps.

Previous API attempt was environment-blocked, not provider-failed. Public OpenSea pages currently demonstrate Robinhood Chain NFT mint/allowlist activity, so the chain-scope patch is evidence-driven.

### 3. Telegram actual delivery
Needed:
- user-created bot token;
- user sends `/start`;
- target chat id;
- one dry-run alert delivered exactly once from our local/outbox semantics;
- Korean text and safe verified-link rendering checked.

## Non-P0 / later adapter evidence
- [ ] Galxe live access-token query before enabling Galxe adapter in production.
- [ ] Dune real query credit/freshness measurement — Phase 1.5.
- [ ] Discord authorized test-server read — Phase 3.
- [ ] Railway account/outbound-connectivity activation check before actual deployment.

## Credential visibility limitation
The connected GitHub integration cannot safely establish whether repository/runtime secrets are already configured. Secret presence must not be guessed.

## Coding policy

### Production feature code
**BLOCKED.**

### Executable harness implementation
**BLOCKED** until remaining P0 operational evidence is resolved or explicitly waived by ADR, and ADR-008 fixture additions are included in runner acceptance criteria.

### Technical spikes
**UNBLOCKED.** No spike artifact may silently become production code.

## PHASE_1_CODING_READY gate
- [x] Deep Design v1.1 complete after latest P0 patch.
- [x] Harness contracts/schemas complete in design.
- [x] Fixture/eval/golden-output plan exists.
- [x] Security boundaries testable in design.
- [x] MVP scope fixed to Ethereum/Base/Robinhood Chain.
- [x] Runtime/API cost guardrail model documented.
- [x] Phase 1 success criteria measurable.
- [x] No unresolved P0 domain/trust-model ambiguity after ADR-007/ADR-008.
- [x] Runtime topology/provider selected (Railway).
- [x] Campaign adapters can degrade without changing architecture.
- [ ] X operational mode/cost resolved or X explicitly downgraded to optional.
- [ ] OpenSea live multi-chain/multi-stage sample completed.
- [ ] Telegram real delivery completed.
- [ ] Spike results reconciled into canonical design/ADRs/status.
- [ ] No unresolved P0 provider feasibility ambiguity.

## Next action
Do not implement the production radar yet. Continue operational spikes in the smallest actionable order:
1. OpenSea live sample when API credential/runtime access is available;
2. Telegram real dry-run when bot configuration is available;
3. X access/cost trial when Developer credentials/pricing are available.

If credentials are not yet available, prepare only disposable spike runners/contracts; do not start production collectors.
