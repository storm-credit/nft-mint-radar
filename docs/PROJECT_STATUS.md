# Project Status

## Current verdict

**Deep Design v1.1 canonical sync complete / Minimum-Action governance adopted / Harness logical-role architecture synced / Harness schemas v1.1 synced / Eval fixtures synced / Local Action Space audit PASS / P0 provider operational evidence 3건 미완료 / Production Coding BLOCKED**

Current gate: **`SPIKE_REQUIRED / PRODUCTION CODING BLOCKED`**.

---

## Authoritative recovery order
1. `CLAUDE.md`
2. this file
3. `docs/PRODUCTION_CODING_START_GATE.md`
4. `docs/DEEP_DESIGN.md`
5. Accepted ADRs, especially ADR-007/008/009
6. `docs/MINIMUM_ACTION_ADOPTION.md`
7. `docs/HARNESS_SPEC.md`
8. `docs/HARNESS_SCHEMAS.md`
9. `docs/EVAL_FIXTURES.md`
10. `docs/LOCAL_ACTION_SPACE_AUDIT.md`
11. relevant spike results

Conversation history is not source of truth.

---

## Completed / accepted

### Domain / product
- Phase 1–4 boundaries accepted.
- Phase 1 EVM target: **Ethereum + Base + Robinhood Chain**.
- OpenSea = high-value structured source, not completeness authority.
- `AssetAmount`, explicit price state, `MintCampaign`, `MintStage`, action-oriented `Opportunity` canonicalized.
- legacy project reactivation / chain migration / holder-access events canonicalized.
- source/project identity trust separated from wallet-impacting CTA safety.
- append-only Evidence, correction/conflict/stale semantics accepted.
- stage/campaign/opportunity state rules accepted.
- Quality / Alpha / Effort / Risk scoring + deterministic hard gates accepted.
- wallet/influencer evidence regimes separated.
- PostgreSQL + transactional outbox accepted.
- Railway hybrid runtime target accepted; no production deployment yet.

### Minimum-Action adoption
- `MINIMUM_ACTION_ADOPTION.md` added.
- ADR-009 accepted.
- root `CLAUDE.md` is constitution/authority map rather than a duplicate domain spec.
- logical Harness roles do not imply separate autonomous agents.
- Phase 1 hot path is deterministic-first.
- model-driven nodes are narrow: unstructured extraction, ambiguous entity resolution, Phase 2 quest parsing, independent critique.
- scoring/state/dedup/budget/decision/Telegram are deterministic by default.
- minimum context bundles defined.
- independent critic is isolated from builder rationale by default.
- Shadow Authority / Stale Derived Artifact are explicit governance checks.

### Local action-space audit
`LOCAL_ACTION_SPACE_AUDIT.md`:
- UNSTRUCTURED_SIGNAL_EXTRACT: PASS
- AMBIGUOUS_ENTITY_RESOLVE: 4 conservative branches — PASS
- QUEST_PARSE: PASS
- INDEPENDENT_CRITIC: 4 verdict branches — PASS
- designed-node waivers: 0
- scope limits: 0

### Harness / derived-artifact synchronization
- `DEEP_DESIGN.md` synchronized to ADR-007/008/009.
- `ARCHITECTURE.md` synchronized and made overview-only.
- `SOURCE_STRATEGY.md` already current.
- `SOURCE_ADAPTER_CONTRACTS.md` synchronized to Robinhood Chain / Campaign+Stage / asset-aware price / minimum-action scheduler model.
- `HARNESS_SPEC.md` synchronized to deterministic-first mechanism.
- `HARNESS_SCHEMAS.md` v1.1 synchronized.
- `PROMPT_CONTRACTS.md` reduced to only narrow model-driven nodes.
- `EVAL_FIXTURES.md` expanded/synchronized through F28.
- `SPIKE_PLAN.md` synchronized to current blocking order/scope.
- `PRODUCTION_CODING_START_GATE.md` synchronized.

Current known P0 stale-derived-artifact blocker: **0**.

---

## Remaining Phase 1 P0 operational evidence — 3

### 1. OpenSea live API mapping / coverage
Need:
- live sample across Ethereum/Base/Robinhood as exposed by API;
- >=10 drops mapped through Project/MintCampaign/MintStage/Opportunity;
- real multi-stage allowlist/public case;
- asset-aware pricing and non-native token case if present;
- off-OpenSea comparison to quantify calendar/listing coverage gaps;
- provider degradation result.

Previous environment could not resolve `api.opensea.io`; that is environment-blocked evidence, not provider failure.

### 2. Telegram real delivery
Need:
- user-created bot/token via secret/runtime only;
- user sends `/start` and target chat established;
- one Korean dry-run delivered once;
- safe CTA formatting;
- retry/dedup result recorded.

### 3. X real access/cost/mode
Need:
- Developer credential/access;
- current price/budget data;
- bounded search/stream test;
- latency and useful/noise volume;
- spend projection;
- final mode = STREAM_PRIMARY / SEARCH_PRIMARY / HYBRID / X_OPTIONAL.

---

## Non-blocking later evidence
- Galxe live query before enabling adapter.
- Dune freshness/credits + out-of-sample AlphaWallet validation — Phase 1.5.
- Discord authorized server read — Phase 3.
- PREMINT/Guild only if supported access is enabled.
- Railway outbound/runtime activation before deployment.

---

## Coding policy

### Production feature code
**BLOCKED.**

### Disposable technical spikes
**UNBLOCKED.** They must not become production code accidentally.

### Harness/eval runner
Can be implemented only when current Start Gate permits the implementation slice; it must use current v1.1 contracts/fixtures and preserve minimum-action architecture.

---

## PHASE_1_CODING_READY
- [x] current domain/architecture design synchronized.
- [x] latest blind-spot decisions incorporated.
- [x] Minimum-Action governance adopted.
- [x] logical-role vs agent distinction fixed.
- [x] typed harness schemas current.
- [x] prompt contracts current.
- [x] eval fixtures current.
- [x] local action-space audit PASS.
- [x] no known P0 stale authority/derived artifact.
- [x] runtime topology/provider target selected.
- [ ] OpenSea operational spike complete.
- [ ] Telegram operational spike complete.
- [ ] X operational mode/cost resolved or explicitly optional.
- [ ] provider spike results reconciled into canonical status/ADRs.
- [ ] no unresolved P0 provider feasibility ambiguity.

---

## Next action
Run the three remaining provider spikes in the smallest actionable order as credentials/access permit:
1. OpenSea
2. Telegram
3. X

Then reconcile results through `PRODUCTION_CODING_START_GATE.md`. Do not start production collectors before the gate passes.
