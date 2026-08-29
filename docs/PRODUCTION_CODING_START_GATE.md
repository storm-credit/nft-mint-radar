# Production Coding Start Gate

## Purpose
Production implementation begins only after domain design, harness/safety rules, minimum-agency architecture, and architecture-changing provider uncertainties are sufficiently closed.

## Gate states
- `DESIGNING`
- `SPIKE_REQUIRED`
- `FREEZE_PENDING`
- `PHASE_1_CODING_READY`
- `CODING_BLOCKED`

---

## A. Recovery
Before evaluating:
- [ ] read `CLAUDE.md`;
- [ ] read `PROJECT_STATUS.md`;
- [ ] read this gate;
- [ ] read `DEEP_DESIGN.md` + relevant Accepted ADRs;
- [ ] read `MINIMUM_ACTION_ADOPTION.md` / ADR-009;
- [ ] read `HARNESS_SPEC.md`, `HARNESS_SCHEMAS.md`, `EVAL_FIXTURES.md`;
- [ ] read relevant spike results;
- [ ] confirm no completed design is being reopened without new P0 evidence.

---

## B. Deep Design
- [x] Phase boundaries defined.
- [x] Phase 1 chain scope = Ethereum + Base + Robinhood Chain.
- [x] OpenSea role defined as structured but incomplete discovery.
- [x] source trust != claim verification != CTA safety.
- [x] AssetAmount / FREE|KNOWN|UNKNOWN|VARIABLE defined.
- [x] MintCampaign / MintStage / Opportunity separation defined.
- [x] legacy reactivation/migration/holder-access events defined.
- [x] evidence version/conflict/stale semantics defined.
- [x] campaign/stage/opportunity state semantics defined.
- [x] Quality/Alpha/Effort/Risk + hard gates defined.
- [x] wallet/influencer evidence boundaries defined.
- [x] persistence/runtime/retry/rate-limit/cost/time/retention rules defined.
- [x] no-wallet-action/no-self-bot/no-fake-engagement safety boundaries defined.
- [x] `DEEP_DESIGN.md` canonical text synchronized to ADR-007/008/009.

---

## C. Minimum-Action / Harness Design
- [x] Minimum Necessary Agency adopted.
- [x] logical role != autonomous agent.
- [x] production hot path deterministic-first.
- [x] Agent creation requires real context/tool/permission/evidence/failure/independent-judgment boundary.
- [x] model-driven nodes use minimum context bundles.
- [x] local action-space audit recorded: designed-node waivers = 0, current planned nodes PASS.
- [x] independent critic input separated from builder rationale by default.
- [x] H0–H9 harness stages defined.
- [x] typed logical I/O v1.1 synchronized with current domain model.
- [x] prompt contracts reduced to narrow model-driven nodes.
- [x] golden fixtures include multi-stage/ERC20/FREE/compromised-official/manual-progress/critic cases.
- [x] failure/stop/error taxonomy defined.
- [x] credential-free design dry-run exists.

---

## D. Red Team
- [x] source coverage / OpenSea completeness limitation
- [x] Robinhood Chain target-pattern gap
- [x] official-account compromise / CTA substitution
- [x] ERC-20 vs native price
- [x] multi-stage GTD/FCFS/holder/community/public
- [x] factory/deployer attribution
- [x] famous-wallet / influencer / wash-sybil manipulation
- [x] AlphaWallet look-ahead/survivorship risk
- [x] Discord/self-bot/social automation
- [x] Telegram phishing/noise
- [x] stale/edit/delete announcement
- [x] provider outage/cost/rate limit
- [x] God Agent / Tool Swamp / Agent Explosion
- [x] Shadow Authority / Stale Derived Artifact
- [x] current P0 design findings closed by targeted PATCH.

---

## E. Phase 1 Blocking Operational Spikes

### OpenSea — CLOSED
- [x] instant credential path observed live;
- [x] Ethereum/Base/Robinhood provider chain keys observed;
- [x] >=10 real detail samples;
- [x] multi-stage GTD/FCFS/holder/free/public structures;
- [x] coverage incompleteness observed and documented;
- [x] provider/environment degradation distinction established.

OpenSea no longer blocks Phase 1.

### Telegram — CLOSED
Real delivery observed 2026-08-29 in run `33255435740`: HTTP 200, `message_id 4`,
467.8 ms, chat auto-resolved via `getUpdates`, `chat_id_matches true`, Korean text,
no CTA, one send producing one provider Message. Telegram no longer blocks Phase 1.

Readiness previously observed:
- [x] disposable probe/workflow ready;
- [x] missing-token path fails closed;
- [x] no network send occurs when token is absent;
- [x] chat id can be resolved from clean-bot `/start` through bounded `getUpdates`, or supplied explicitly.

Completed:
- [x] `TELEGRAM_BOT_TOKEN` configured through secret;
- [x] user sent `/start` to `@nftmr_bot`;
- [x] one Korean dry-run delivered;
- [x] provider response/message id/latency observed;
- [x] one send produced one provider Message; dedup remains a local outbox
      responsibility and is verified by notifier fixtures, not by this spike.

### X — CLOSED
Measured 2026-08-29 for `$0.055` of an approved `$0.10` ceiling. Free plan 403s on both
endpoints; Pay Per Use required. Recent Search 200 at 225.9 ms. Filtered Stream delivered
10 Posts in 16.9 s at 4.3-5.1 s lag with a clean rule create/delete cycle. A broad keyword
rule measured useful 0 / noise 10 at about $250/day, which is why `ADR-010` freezes the mode
as `STREAM_PRIMARY_WITH_SEARCH_RECOVERY` with author-scoped rules mandatory.

Prior paper contract, retained:
Current official public contract observed 2026-08-29:
- [x] Post read rate observed: `$0.005/resource`;
- [x] Pay-per-use Filtered Stream documented available;
- [x] Filtered Stream limits observed: 1,000 rules/project, 1 connection;
- [x] ~6–7 second P99 delivery documented;
- [x] 2,000,000 Post-read/month Pay-per-use cap documented;
- [x] Bearer Token documented for app-only public reads;
- [x] disposable probe compile PASS;
- [x] absent-token path observed with paid calls = 0;
- [x] paid test bounded to <= `$0.10` Post-read cost at observed public rate;
- [x] stream leg refuses pre-existing rules and removes its temporary rule.

Still required:
- [x] `X_BEARER_TOKEN` configured through secret;
- [x] App attached to a Pay Per Use project; the Free-plan 403 is recorded as a measured fact;
- [x] API credit sufficient — actual spend `$0.055`;
- [x] explicit paid-run confirmation supplied;
- [x] bounded Recent Search sample observed;
- [x] bounded Filtered Stream rule/connection lifecycle observed, including clean cleanup;
- [x] useful/noise sample classified — useful 0 / noise 10 on a broad rule, useful 0 / noise 1
      on the `from:opensea` search. Signal yield is explicitly **not** proven;
- [x] public Post-read rate rechecked at `$0.005/resource` immediately before each execution;
- [x] final mode frozen as `STREAM_PRIMARY_WITH_SEARCH_RECOVERY` in `ADR-010`.

---

## F. Non-blocking later evidence
- [ ] Dune freshness/credits + out-of-sample AlphaWallet validation — Phase 1.5.
- [ ] Galxe live query before production adapter enablement.
- [ ] PREMINT partner access if enabled.
- [ ] Guild supported integration if enabled.
- [ ] Discord authorized server read — Phase 3.
- [ ] Railway outbound/runtime activation check before actual deployment.
- [ ] targeted non-native OpenSea payment-asset sample when available.

---

## G. Freeze reconciliation
After Telegram/X pass or a named item is explicitly waived:
- [x] OpenSea spike result saved and reconciled;
- [x] X paper/access contract reconciled;
- [x] save Telegram real-delivery result;
- [x] save X credentialed result;
- [x] update final X source mode/budget assumptions (ADR-010);
- [ ] verify no derived schema/prompt/fixture/spike mapping is stale;
- [ ] freeze Phase 1 source/runtime configuration;
- [ ] confirm no unresolved P0 provider ambiguity.

---

## H. Coding authorization
Only after the remaining E + G items are complete (or explicit named ADR waiver) set:

`PHASE_1_CODING_READY`

Implementation order:
1. canonical domain primitives;
2. evidence/identity/CTA-safety core;
3. selected P0 source adapters;
4. normalization + campaign/stage/opportunity state;
5. deterministic scoring/decision gates;
6. transactional outbox;
7. Telegram renderer/notifier;
8. scheduler/worker integration;
9. fixture/eval runner;
10. controlled end-to-end dry run.

No central God Agent orchestration is introduced by default.

---

## I. Regression rule
If later evidence invalidates a frozen assumption:
1. mark only affected authority/derived artifacts STALE;
2. stop impacted path;
3. targeted Red Team/spike;
4. KEEP/PATCH/CUT first;
5. NEW DESIGN only for true structural hole;
6. re-enter only affected gate criteria.

## Current verdict

**`FREEZE_PENDING`**

All Phase 1 blocking operational spikes are closed: OpenSea, Telegram, X.
No user-owned credential is outstanding.

Production coding is still blocked on analysis, not evidence collection:
1. full cross-system Red Team with P0 = 0;
2. remaining section G reconciliation.
