# Project Status

## Current verdict

**Deep Design v1.1 canonical sync complete / Minimum-Action governance adopted / Harness logical-role architecture synced / Harness schemas v1.1 synced / Eval fixtures synced / Local Action Space audit PASS / OpenSea operational spike CLOSED / Telegram credential path probed / X paper-cost contract resolved + no-cost preflight PASS / P0 credentialed operational evidence 2건 미완료 / Production Coding BLOCKED**

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
- Quality / Alpha / Effort / Risk scoring + deterministic hard gates accepted.
- wallet/influencer evidence regimes separated.
- PostgreSQL + transactional outbox accepted.
- Railway hybrid runtime target accepted; no production deployment yet.

### Minimum-Action adoption
- root `CLAUDE.md` is constitution/authority map rather than duplicate domain spec.
- logical Harness roles do not imply separate autonomous agents.
- Phase 1 hot path is deterministic-first.
- model-driven nodes are narrow: unstructured extraction, ambiguous entity resolution, Phase 2 quest parsing, independent critique.
- scoring/state/dedup/budget/decision/Telegram are deterministic by default.
- minimum context bundles defined.
- Shadow Authority / Stale Derived Artifact governance active.

### Local action-space audit
- UNSTRUCTURED_SIGNAL_EXTRACT: PASS
- AMBIGUOUS_ENTITY_RESOLVE: PASS
- QUEST_PARSE: PASS
- INDEPENDENT_CRITIC: PASS
- designed-node waivers: 0
- scope limits: 0

### Derived-artifact synchronization
Current known P0 stale-derived-artifact blocker: **0**.

`DEEP_DESIGN`, `ARCHITECTURE`, `SOURCE_STRATEGY`, `SOURCE_ADAPTER_CONTRACTS`, `HARNESS_SPEC`, `HARNESS_SCHEMAS`, `PROMPT_CONTRACTS`, `EVAL_FIXTURES`, `SPIKE_PLAN`, and the Production Coding Start Gate are synchronized to the current design.

---

## OpenSea operational spike — CLOSED
See `docs/spikes/SPIKE-MARKET-001-RESULT.md`.

Observed live through GitHub Actions on 2026-08-28:
- instant free key issuance PASS;
- chain keys: `ethereum`, `base`, `robinhood`;
- combined upcoming rows: 14;
- Ethereum: 8;
- Base: 0 at observation time;
- Robinhood: 6;
- detail sample: 10/10;
- multi-stage: 7/10;
- total stages: 25;
- GTD / FCFS / holder / free-team / public structures observed.

Coverage conclusion:
- Base endpoint itself succeeded while `upcoming` returned zero during a period with active Base mint surfaces;
- therefore OpenSea is structurally useful but incomplete;
- outside official/campaign/on-chain/X discovery remains required.

---

## Telegram operational spike — credential path ready, delivery still blocked
See `docs/spikes/SPIKE-TG-001-RESULT.md`.

Guarded Actions smoke observed (2026-08-28 run `33172110528`, reobserved 2026-08-29 run `33252936929`):
- workflow/probe path ready;
- `TELEGRAM_BOT_TOKEN`: **ABSENT** at both observed runs;
- delivery step skipped;
- network send attempted: false;
- repository Actions-secret enumeration on 2026-08-29: zero secrets, zero environments.

User-side prerequisite is now minimal:
1. create bot with `@BotFather`;
2. add Actions secret `TELEGRAM_BOT_TOKEN`;
3. send `/start` once.

`TELEGRAM_CHAT_ID` is normally unnecessary for the clean-bot spike.

Remaining evidence:
- one Korean dry-run arrives;
- provider message id/latency observed;
- single-delivery/dedup contract retained.

---

## X operational spike — paper/cost ambiguity closed, credentialed run still blocked
See `docs/spikes/SPIKE-X-001-RESULT.md`.

Current official documentation observed 2026-08-29 establishes:
- Post read: **$0.005/resource** at observed revision;
- Pay-per-use Filtered Stream available;
- 1,000 rules/project;
- 1 stream connection;
- ~6–7 second P99 stream delivery described by X;
- 2,000,000 Post-read/month Pay-per-use cap;
- Bearer Token for app-only public-data reads.

Provisional mode:

`FILTERED_STREAM_PRIMARY + RECENT_SEARCH_RECOVERY`

No-cost Actions preflight runs `33245992097` and `33252938234` (2026-08-29) observed:
- `spikes/x_probe.py` compile: PASS;
- `X_BEARER_TOKEN`: **ABSENT**;
- paid API calls attempted: 0;
- repository Actions-secret enumeration on 2026-08-29: zero secrets, zero environments.

Bounded credentialed test is ready:
- Recent Search <=10 Posts -> current ceiling `$0.05`;
- Filtered Stream <=10 Posts -> current ceiling `$0.05`;
- combined Post-read ceiling: **`$0.10`** at current public rate;
- existing stream rules => stream leg refuses to run;
- paid call requires exact manual opt-in `I_UNDERSTAND_X_MAY_COST`.

Remaining evidence:
- Bearer-token API access;
- bounded useful/noise sample;
- stream rule/connection lifecycle or precise access failure;
- execution-time rate recheck;
- final X mode freeze.

---

## Remaining Phase 1 P0 blockers — exactly 2

### 1. Telegram
External user-owned prerequisite:
- `TELEGRAM_BOT_TOKEN` + `/start`.

### 2. X
External user-owned prerequisite:
- developer Project/App;
- enough API credit for bounded test;
- `X_BEARER_TOKEN`.

No additional P0 design/code uncertainty is known before those credentials exist.

---

## Non-blocking later evidence
- Galxe live query before enabling adapter.
- Dune freshness/credits + out-of-sample AlphaWallet validation — Phase 1.5.
- Discord authorized server read — Phase 3.
- PREMINT/Guild only if supported access is enabled.
- Railway outbound/runtime activation before deployment.
- targeted non-native OpenSea payment-asset sample when available.

---

## Coding policy

### Production feature code
**BLOCKED.**

### Disposable technical spikes
**UNBLOCKED.** They must not become production code accidentally.

---

## PHASE_1_CODING_READY
- [x] domain/architecture synchronized.
- [x] latest blind-spot decisions incorporated.
- [x] Minimum-Action governance adopted.
- [x] typed harness schemas current.
- [x] prompt contracts current.
- [x] eval fixtures current.
- [x] local action-space audit PASS.
- [x] no known P0 stale authority/derived artifact.
- [x] runtime topology/provider target selected.
- [x] OpenSea operational spike complete and reconciled.
- [x] X public pricing/access contract revalidated and bounded probe ready.
- [ ] Telegram real delivery complete.
- [ ] X credentialed bounded run complete and final mode frozen.
- [ ] remaining results reconciled into canonical status/ADR if required.
- [ ] no unresolved P0 provider feasibility ambiguity.

---

## Next action
No production collectors yet.

As soon as credentials exist:
1. Telegram dry-run;
2. X bounded <=$0.10 trial;
3. reconcile results;
4. move to `FREEZE_PENDING`;
5. if no P0 remains, set `PHASE_1_CODING_READY` and begin production implementation in the frozen order.
