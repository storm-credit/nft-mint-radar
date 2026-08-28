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
- [x] current golden fixture families include multi-stage/ERC20/FREE/compromised-official/manual-progress/critic cases.
- [x] failure/stop/error taxonomy defined.
- [x] credential-free design dry-run exists.

Production harness runner code is not required before this design gate; production feature coding still waits for provider evidence below.

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
- [x] current P0 design findings closed by targeted PATCH, not redesign.

---

## E. Phase 1 Blocking Operational Spikes

### OpenSea
- [ ] live upcoming/listed sample succeeds across target chains as available through provider API;
- [ ] >=10 real drops map to Project/MintCampaign/MintStage/Opportunity;
- [ ] real multi-stage allowlist/public mapping verified;
- [ ] asset-aware price mapping verified, including non-native token if present;
- [ ] coverage gap vs off-OpenSea discovery documented;
- [ ] failure/degradation behavior confirmed.

### Telegram
- [ ] bot token only through secret/runtime;
- [ ] chat target established after user starts bot;
- [ ] one real Korean dry-run arrives once under local dedup semantics;
- [ ] safe CTA rendering checked;
- [ ] failure/retry result recorded.

### X
- [ ] real credential access succeeds;
- [ ] bounded search/stream trial completed;
- [ ] latency measured;
- [ ] delivered/useful/noise volume measured;
- [ ] cost projection measured from current pricing/console;
- [ ] final mode frozen: STREAM_PRIMARY / SEARCH_PRIMARY / HYBRID / X_OPTIONAL.

---

## F. Non-blocking later evidence
- [ ] Dune freshness/credits + out-of-sample AlphaWallet validation — Phase 1.5.
- [ ] Galxe live query before production adapter enablement.
- [ ] PREMINT partner access if enabled.
- [ ] Guild supported integration if enabled.
- [ ] Discord authorized server read — Phase 3.
- [ ] Railway outbound/runtime activation check before actual deployment.

---

## G. Freeze reconciliation
After E passes or named items are explicitly waived:
- [ ] save spike results;
- [ ] reconcile observed provider evidence into canonical design/ADR/status;
- [ ] update source modes/cost assumptions;
- [ ] verify no derived schema/prompt/fixture/spike mapping is stale;
- [ ] freeze Phase 1 source/runtime configuration;
- [ ] confirm no unresolved P0 provider ambiguity.

---

## H. Coding authorization
Only after E + G are complete (or explicit named ADR waiver) set:

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
If later evidence invalidates frozen assumption:
1. mark only affected authority/derived artifacts STALE;
2. stop impacted path;
3. targeted Red Team/spike;
4. KEEP/PATCH/CUT first;
5. NEW DESIGN only for true structural hole;
6. re-enter only affected gate criteria.

## Current verdict

**`SPIKE_REQUIRED / PRODUCTION CODING BLOCKED`**

Only Phase 1 blocking evidence remaining:
1. OpenSea live multi-chain/multi-stage mapping/coverage;
2. Telegram real delivery;
3. X operational access/cost/mode.
