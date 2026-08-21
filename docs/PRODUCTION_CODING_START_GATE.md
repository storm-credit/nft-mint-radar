# Production Coding Start Gate

## Purpose
This gate is the NFT Radar equivalent of a manuscript-start gate: production implementation begins only after the system design, harness, safety model, and architecture-changing provider uncertainties are sufficiently closed.

The objective is not paperwork. The objective is to prevent unresolved provider, cost, safety, timing, or data-contract questions from being decided accidentally inside production code.

## Gate states
- `DESIGNING` — P0 design decisions remain unresolved.
- `SPIKE_REQUIRED` — design is coherent, but real provider evidence is still needed.
- `FREEZE_PENDING` — required spikes passed; results still need reconciliation into canonical design/ADR/status.
- `PHASE_1_CODING_READY` — Phase 1 production implementation may begin.
- `CODING_BLOCKED` — a P0 failure, regression, or unresolved architectural ambiguity blocks implementation.

## A. Current-state recovery
Before evaluating this gate:
- [ ] Read `CLAUDE.md`.
- [ ] Read `docs/PROJECT_STATUS.md`.
- [ ] Read `docs/DEEP_DESIGN.md`.
- [ ] Read latest targeted blind-spot audit.
- [ ] Read `docs/HARNESS_SPEC.md` and `docs/HARNESS_SCHEMAS.md`.
- [ ] Read all relevant spike results and ADRs, including ADR-007/ADR-008.
- [ ] Confirm that completed/frozen work is not being reopened without new P0 evidence.

## B. Deep Design completeness
- [x] Phase boundaries defined.
- [x] Initial chain scope defined as Ethereum + Base + Robinhood Chain.
- [x] Source trust and discovery-vs-verification policy defined.
- [x] Source identity trust separated from CTA link safety.
- [x] Canonical entity/data contracts defined.
- [x] Asset-aware mint price semantics defined.
- [x] Multi-stage MintCampaign/MintStage semantics defined.
- [x] Legacy/reactivation/migration signal types defined.
- [x] Opportunity/state semantics defined.
- [x] Evidence conflict/version/staleness policy defined.
- [x] Scoring model and safety gates defined.
- [x] Wallet/influencer signal boundaries defined.
- [x] Runtime/storage architecture selected.
- [x] Retry/rate-limit/degradation/timezone/retention policies defined.
- [x] Security/non-automation boundaries defined.

## C. Executable Harness design completeness
- [x] H0–H8 harness stages defined.
- [x] Agent responsibilities and forbidden actions defined.
- [x] Typed logical I/O contracts defined.
- [x] Prompt contracts and injection boundaries defined.
- [x] Golden fixture families defined.
- [x] Failure/stop/error taxonomy defined.
- [x] Credential-free end-to-end design dry-run completed.
- [x] ADR-008 fixture requirements recorded for multi-stage/ERC20/compromised-official-channel cases.

Note: production harness runner code does not need to exist before this design gate, but production feature coding must not begin until provider evidence below is closed.

## D. Red Team / blind-spot gate
- [x] Source coverage blind spots reviewed.
- [x] Phase 1 chain coverage re-audited against actual user target pattern.
- [x] Official-account-compromise CTA risk reviewed.
- [x] Native-vs-ERC20 mint-price semantics reviewed.
- [x] Multi-stage GTD/FCFS/community/public mint structure reviewed.
- [x] OpenSea curation/completeness limitation reviewed.
- [x] Factory-deployer attribution risk reviewed.
- [x] Famous-wallet trap reviewed.
- [x] Influencer/shill manipulation reviewed.
- [x] Wash/sybil manipulation reviewed.
- [x] Discord self-bot/social automation trap reviewed.
- [x] Telegram phishing/noise trap reviewed.
- [x] Stale/edit/delete announcement risk reviewed.
- [x] Cost/rate-limit/provider-outage degradation reviewed.
- [x] P0 design findings closed through ADR-007/ADR-008.

## E. Operational spike gate — Phase 1 blocking
These are architecture/cost/utility-sensitive and must be observed or explicitly waived by ADR.

### X
- [ ] Real credential access succeeds.
- [ ] Small search/stream trial completed.
- [ ] Detection latency measured.
- [ ] Delivered/noise volume measured.
- [ ] Cost projection measured from current console/pricing.
- [ ] Final mode frozen: `STREAM_PRIMARY`, `SEARCH_PRIMARY`, `HYBRID`, or `X_OPTIONAL`.

### OpenSea
- [ ] Live upcoming sample succeeds across **Ethereum + Base + Robinhood Chain**.
- [ ] At least 10 real drops map to canonical MintCampaign/MintStage/Opportunity.
- [ ] Multi-stage allowlist/public structure mapping verified on real samples.
- [ ] Asset-aware pricing mapping verified, including non-native token pricing when present.
- [ ] Required fields/coverage gaps documented.
- [ ] Manual comparison against off-OpenSea discoveries completed; OpenSea completeness must not be assumed.
- [ ] Failure/degradation behavior confirmed.

### Telegram
- [ ] Bot token available through secret/config path without disclosure.
- [ ] User has started bot and chat target is known.
- [ ] One real dry-run alert arrives exactly once under local outbox/dedup semantics.
- [ ] Korean text and safe verified-link rendering verified.
- [ ] Failure/retry result recorded.

## F. Non-blocking later-phase spikes
These do not block Phase 1 unless architecture is later changed to depend on them.
- [ ] Dune real freshness/credit test — Phase 1.5.
- [ ] AlphaWallet benchmark tested out-of-sample to reduce survivorship/look-ahead bias — Phase 1.5.
- [ ] Galxe live credential/query test — before production Galxe adapter enablement.
- [ ] PREMINT partner access test — optional adapter.
- [ ] Guild integration feasibility — optional adapter.
- [ ] Discord authorized server-read test — Phase 3.

## G. Freeze reconciliation
After all Phase 1 blocking spikes:
- [ ] Spike results are saved as retained evidence.
- [ ] Observed evidence is reconciled into canonical design/ADRs/status.
- [ ] Any pre-ADR-007 chain assumptions are marked superseded.
- [ ] Any pre-ADR-008 native-only/single-stage/T1-CTA assumptions are marked superseded.
- [ ] No unresolved P0 provider ambiguity remains.
- [ ] No downstream contract is silently stale.
- [ ] Phase 1 source scope and runtime topology are frozen.

## H. Coding authorization
Production Phase 1 coding may start only when every item in E and G is checked, or a named item has an explicit ADR waiver with rationale, risk, fallback, and revalidation trigger.

When authorized, set authoritative status to:

`PHASE_1_CODING_READY`

Then implementation order is:
1. canonical schemas/domain primitives including ChainIdentity, AssetAmount, MintCampaign and MintStage;
2. evidence store + identity/verification/CTA-safety core;
3. selected P0 source adapters;
4. normalization/state machine;
5. scoring/decision gates;
6. transactional outbox;
7. Telegram reporter;
8. scheduler/worker integration;
9. fixture/eval regression suite;
10. end-to-end controlled dry run.

## I. Regression rule
If later evidence invalidates a frozen P0 assumption:
1. mark affected design/contracts `STALE`;
2. stop only the impacted production path;
3. run targeted Red Team/spike;
4. PATCH/CUT first;
5. use NEW DESIGN only if architecture truly cannot absorb the evidence;
6. re-enter this gate only for affected criteria.

Do not reset the whole project for a local provider change.

## Current gate verdict

`SPIKE_REQUIRED / PRODUCTION CODING BLOCKED`

Blocking evidence remaining:
1. X operational mode/cost;
2. OpenSea live multi-chain/multi-stage sample and coverage;
3. Telegram real delivery.
