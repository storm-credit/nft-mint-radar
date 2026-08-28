# Project Status

## Current verdict

**Deep Design decisions accepted / Minimum-Action adoption complete in governance / Harness logical-role architecture patched / Harness typed schemas synced to ADR-008 / Eval fixtures synced / `DEEP_DESIGN.md` canonical text sync still required / P0 provider spikes 3건 미완료 / Production Coding BLOCKED**

Current gate: **`SPIKE_REQUIRED + STALE_DERIVED_ARTIFACT / PRODUCTION CODING BLOCKED`**.

---

## Authoritative recovery order
1. `CLAUDE.md`
2. this file
3. `docs/PRODUCTION_CODING_START_GATE.md`
4. `docs/DEEP_DESIGN.md`
5. Accepted ADRs, especially ADR-007/008/009
6. `docs/HARNESS_SPEC.md`
7. `docs/HARNESS_SCHEMAS.md`
8. `docs/EVAL_FIXTURES.md`
9. relevant spike results

Do not reconstruct truth from conversation history.

---

## Completed / accepted

### Product and architecture decisions
- Phase 1–4 boundaries accepted.
- Phase 1 EVM target set: **Ethereum + Base + Robinhood Chain** — ADR-007.
- OpenSea remains high-value structured source but not coverage authority — ADR-007.
- `AssetAmount`, `MintCampaign`, `MintStage`, explicit price state, legacy-reactivation signals, and independent CTA safety accepted — ADR-008.
- identity trust and wallet-impacting CTA safety are separate.
- Quality / Alpha / Effort / Risk scoring + hard gates accepted.
- PostgreSQL + transactional notification outbox accepted.
- Railway hybrid runtime target accepted; no production deployment yet.

### Minimum-Action governance
- `docs/MINIMUM_ACTION_ADOPTION.md` added.
- ADR-009 accepted.
- root `CLAUDE.md` reduced to constitution/authority pointers instead of duplicating domain truth.
- production hot path is deterministic-first; logical roles are not automatically separate agents.
- project-designed model-driven nodes target <=5 meaningful peer choices.
- Agent creation requires a real context/tool/permission/evidence/failure/independent-judgment boundary.
- minimal context bundles and independent critic isolation defined.
- Shadow Authority / Stale Derived Artifact are explicit Red Team checks.

### Harness synchronization completed
- `HARNESS_SPEC.md` now classifies logical roles by implementation mechanism.
- `HARNESS_SCHEMAS.md` v1.1 now includes campaign/stage refs, CTA safety state, user-confirmed progress, independent critic and local-action-space audit.
- `EVAL_FIXTURES.md` now includes multi-stage, ERC-20 price, FREE vs UNKNOWN, compromised official account, revocation, legacy reactivation, manual progress and weak-reading critic cases.

---

## Current stale artifact — P0 governance issue

### `docs/DEEP_DESIGN.md`
Accepted ADR-007/008 override portions of its older text, but the canonical file still contains stale statements including:
- Phase 1 chain list `Ethereum + Base` only;
- old single-`Opportunity` mint representation;
- `mint_price_native`;
- older event taxonomy without legacy-reactivation events;
- older CTA rule that can be read as trusting T1 identity too directly.

Therefore **do not call Deep Design text fully synchronized yet**.

Governance rule until sync:
- ADR-007/008 govern conflicts.
- `DEEP_DESIGN.md` is `STALE_PARTIAL` for the affected sections.
- Production Coding Start Gate remains blocked even if provider spikes later pass, until canonical sync is complete.

This is a targeted PATCH requirement, not a redesign.

---

## Remaining P0 provider evidence — 3

### X
Need real developer access/pricing + small trial:
- latency
- delivered/noise volume
- spend projection
- final mode: STREAM_PRIMARY / SEARCH_PRIMARY / HYBRID / X_OPTIONAL

### OpenSea
Need live API sample across Ethereum/Base/Robinhood:
- 10+ drops mapped to MintCampaign/MintStage
- allowlist/multi-stage example
- ERC-20 price case if present
- coverage comparison against outside discovery

### Telegram
Need one actual user-visible dry run:
- bot token through secret/runtime only
- chat target established
- Korean message
- safe CTA rendering
- dedup/outbox semantics observed

---

## Non-blocking later evidence
- Galxe live token/query before production adapter enablement.
- Dune freshness/credits — Phase 1.5.
- Discord authorized server read — Phase 3.
- Railway outbound/runtime activation check before deployment.

---

## Coding policy

### Production feature code
**BLOCKED.**

### Technical spikes
**UNBLOCKED** and must stay disposable/isolated.

### Harness runner
May be implemented only after:
1. `DEEP_DESIGN.md` stale sections are synchronized;
2. local-action-space audit is recorded for model-driven nodes;
3. runner acceptance uses current v1.1 schemas/fixtures.

---

## PHASE_1_CODING_READY checklist
- [x] Product/architecture decisions accepted.
- [x] Latest blind-spot P0 decisions accepted via ADR-007/008.
- [x] Minimum-Action governance adopted via ADR-009.
- [x] Harness logical roles no longer imply agent-per-role architecture.
- [x] Harness schemas synchronized to ADR-008.
- [x] Eval fixture set synchronized to current safety/stage model.
- [ ] `DEEP_DESIGN.md` canonical stale sections synchronized.
- [ ] model-driven local-action-space audit recorded.
- [ ] X operational mode/cost resolved or explicitly downgraded optional.
- [ ] OpenSea live multi-chain/multi-stage sample completed.
- [ ] Telegram real delivery completed.
- [ ] spike results reconciled into canonical docs/ADRs/status.
- [ ] no unresolved P0 provider or authority inconsistency.

---

## Next action

1. **Synchronize `DEEP_DESIGN.md` to ADR-007/008 without redesign.**
2. Run local-action-space audit for only the planned model-driven nodes.
3. Resume smallest provider spikes: OpenSea -> Telegram -> X as credentials/access permit.
4. Re-evaluate `PRODUCTION_CODING_START_GATE.md`.

Do not start production collectors before these gates close.
