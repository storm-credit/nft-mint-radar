# Project Status

## Current verdict

**Deep Design v1.1 canonical sync complete / Minimum-Action governance adopted / Harness logical-role architecture synced / Harness schemas v1.1 synced / Eval fixtures synced / Local Action Space audit PASS / OpenSea operational spike CLOSED / P0 provider operational evidence 2건 미완료 / Production Coding BLOCKED**

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
- root `CLAUDE.md` is constitution/authority map rather than duplicate domain spec.
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
- `ARCHITECTURE.md` synchronized and overview-only.
- `SOURCE_STRATEGY.md` current.
- `SOURCE_ADAPTER_CONTRACTS.md` synchronized to Robinhood Chain / Campaign+Stage / asset-aware price / minimum-action scheduler model.
- `HARNESS_SPEC.md` synchronized to deterministic-first mechanism.
- `HARNESS_SCHEMAS.md` v1.1 synchronized.
- `PROMPT_CONTRACTS.md` limited to narrow model-driven nodes.
- `EVAL_FIXTURES.md` synchronized through F28.
- `SPIKE_PLAN.md` synchronized.
- `PRODUCTION_CODING_START_GATE.md` synchronized.

Current known P0 stale-derived-artifact blocker: **0**.

### OpenSea operational spike — CLOSED
See `docs/spikes/SPIKE-MARKET-001-RESULT.md`.

Observed live through GitHub Actions on 2026-08-28:
- instant free key issuance: PASS (`201`)
- provider chain keys resolved: `ethereum`, `base`, `robinhood`
- combined upcoming rows: 14
- Ethereum query: 200 / 8 rows
- Base query: 200 / 0 rows at observation time
- Robinhood query: 200 / 6 rows
- detail sample: 10/10 success
- multi-stage drops: 7/10
- total stages: 25
- real GTD / FCFS / holder / free-team / public structures observed
- Robinhood multi-stage mapping validated
- previous DNS failure reclassified as execution-environment-specific

Important coverage decision:
- Base returned zero `upcoming` rows while active Base mint surfaces existed;
- therefore OpenSea `upcoming` is useful but cannot be treated as mint-coverage authority;
- off-OpenSea official/campaign/on-chain discovery remains required.

Non-native payment-token canonicalization was not observed in the bounded detail sample. The domain already represents unknown payment assets safely, so this is retained as a future targeted adapter refinement, not a Phase 1 blocker.

---

## Remaining Phase 1 P0 operational evidence — 2

### 1. Telegram real delivery
User-side prerequisites have been reduced to:
- create Telegram bot;
- store `TELEGRAM_BOT_TOKEN` only in secret/runtime configuration;
- send `/start` to the bot.

`TELEGRAM_CHAT_ID` is optional for the spike; the disposable probe can resolve the latest private chat through `getUpdates` when no webhook is configured.

Need to observe:
- one Korean dry-run delivered once;
- safe no-CTA/CTA formatting behavior;
- delivery response and local retry/dedup semantics.

### 2. X real access/cost/mode
Need:
- Developer credential/access;
- current pricing/budget data;
- bounded recent-search/stream test;
- latency and useful/noise volume;
- spend projection;
- final mode = STREAM_PRIMARY / SEARCH_PRIMARY / HYBRID / X_OPTIONAL.

X calls remain guarded because reads may consume paid credits.

---

## Non-blocking later evidence
- Galxe live query before enabling adapter.
- Dune freshness/credits + out-of-sample AlphaWallet validation — Phase 1.5.
- Discord authorized server read — Phase 3.
- PREMINT/Guild only if supported access is enabled.
- Railway outbound/runtime activation before deployment.
- targeted non-native OpenSea payment-asset mapping sample when available.

---

## Coding policy

### Production feature code
**BLOCKED.**

### Disposable technical spikes
**UNBLOCKED.** They must not become production code accidentally.

### Harness/eval runner
Can be implemented only when the current Start Gate permits that slice; it must use current v1.1 contracts/fixtures and preserve minimum-action architecture.

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
- [x] OpenSea operational spike complete and reconciled.
- [ ] Telegram operational spike complete.
- [ ] X operational mode/cost resolved or explicitly optional.
- [ ] remaining provider spike results reconciled into canonical status/ADRs.
- [ ] no unresolved P0 provider feasibility ambiguity.

---

## Next action
Do not start production collectors yet.

Continue only the two remaining Phase 1 provider spikes as credentials/access permit:
1. Telegram real dry-run;
2. X bounded paid-access/cost trial.

Then reconcile through `docs/PRODUCTION_CODING_START_GATE.md` and, if all P0 evidence is closed, move to `FREEZE_PENDING` and finally `PHASE_1_CODING_READY`.
