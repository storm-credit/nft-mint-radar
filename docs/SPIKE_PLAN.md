# Technical Spike Plan

## Purpose
Spikes answer provider/architecture uncertainties without allowing disposable experiments to become production code.

Rules:
- one bounded question per spike;
- no production feature code;
- no committed credentials;
- explicit success/failure/cost cap;
- result retained under `docs/spikes/`;
- provider failure must degrade behind an adapter, not break core architecture;
- paid calls require the smallest practical test budget and explicit user approval where new spend is required.

---

## SPIKE-MARKET-001 — OpenSea live coverage/mapping — CLOSED
See `docs/spikes/SPIKE-MARKET-001-RESULT.md`.

Observed live through GitHub Actions:
- instant free key issuance works;
- `ethereum`, `base`, `robinhood` chain keys resolve;
- combined/per-chain calls succeed;
- 10/10 detail sample succeeded;
- multi-stage GTD/FCFS/holder/free/public structures observed;
- Base `upcoming` returned zero during a period with active Base mint surfaces.

Decision:
- OpenSea is a valuable structured discovery/verification source;
- OpenSea `upcoming` is not a completeness authority;
- outside official/campaign/on-chain discovery remains required.

No longer Phase 1 blocking.

---

## SPIKE-TG-001 — Telegram delivery — CLOSED 2026-08-29 (PASS)
### Question
Can one action alert be delivered safely and observably to the user's Telegram with local dedup/outbox semantics?

### Current readiness
Credential-path smoke already ran and proved:
- workflow/probe path is ready;
- `TELEGRAM_BOT_TOKEN` was absent at the observed run;
- no network send occurred without the secret.

### User prerequisite
1. create a bot with `@BotFather`;
2. store only `TELEGRAM_BOT_TOKEN` as GitHub/runtime secret;
3. send `/start` once.

`TELEGRAM_CHAT_ID` is optional for a clean test bot; the disposable probe can resolve the latest private chat through `getUpdates` when no webhook is configured.

### Method after credential exists
1. rerun guarded disposable probe;
2. resolve target;
3. send one Korean no-wallet-action dry-run;
4. observe provider response/message id;
5. verify local correlation/dedup behavior.

### Success
- user sees one intended dry-run;
- secret not logged;
- response observable;
- retry/dedup behavior recorded.

### Artifact
`docs/spikes/SPIKE-TG-001-RESULT.md`

---

## SPIKE-X-001 — X discovery access/noise — CLOSED 2026-08-29, mode frozen in ADR-010
### Question
Can official-project/reactivation/WL signals be detected with acceptable useful/noise ratio using a bounded Pay-per-use configuration?

### Paper validation now closed
Current official documentation observed 2026-08-29 states:
- Post read: `$0.005/resource`;
- Pay-per-use has no subscription/minimum-spend requirement stated in public docs;
- Filtered Stream is available to Pay-per-use;
- Filtered Stream: 1,000 rules/project, 1 connection, core operators;
- approximate 6–7 second P99 stream delivery;
- pay-per-use cap: 3,000,000 Post reads/month before Enterprise (rechecked 2026-08-29);
- Bearer Token supports app-only public-data reads.

Prices are rechecked in Developer Console at execution/production time.

### Frozen mode
`STREAM_PRIMARY_WITH_SEARCH_RECOVERY` — frozen by `ADR-010` on measured evidence.

Constraints that are part of the freeze: stream rules must be author-scoped `from:` clauses over
verified official accounts with `-is:retweet -is:reply`; broad keyword-only rules are forbidden;
Recent Search is recovery-only advanced by `since_id`; a deterministic source budget gates every paid
read; the adapter degrades to `X_OPTIONAL` under ADR-002 if measured signal ROI stays poor.

Also measured: the Free plan returns 403 on both endpoints and cannot serve this product.

### Bounded paid method
The disposable probe hard-caps the initial test at the observed public rate:

1. Recent Search: <=10 returned Posts -> <= `$0.05` Post-read cost.
2. Filtered Stream: <=10 delivered Posts -> <= `$0.05` Post-read cost.
3. Combined mode Post-read ceiling -> <= **`$0.10`**.
4. Stream refuses to run if any pre-existing stream rule exists, preventing unrelated rules from creating unbounded test reads.
5. Temporary stream rule is removed after the experiment.
6. Any paid call still requires exact manual opt-in `I_UNDERSTAND_X_MAY_COST`.
7. Cost is estimated over every Post the provider actually returned, never over a locally truncated view. If the returned count exceeds a cap, or the estimated Post-read cost exceeds the declared ceiling, the probe fails the run instead of reporting a bounded PASS.
8. Known accounting bound: the Filtered Stream figure counts Posts the probe read. X may additionally bill a small number of Posts already delivered into the socket buffer when the bounded loop stops, so the stream leg's recorded spend is a close lower bound rather than an exact charge.

### Success
- Bearer-token access succeeds;
- search sample can be classified into useful/noise;
- stream rule lifecycle/connection succeeds, or a precise access restriction is observed;
- execution-time rate matches or supersedes the documented `$0.005` assumption;
- final mode can be frozen as `STREAM_PRIMARY_WITH_SEARCH_RECOVERY`, `SEARCH_PRIMARY`, or `X_OPTIONAL`.

### Failure
- credential/access unavailable;
- stream unavailable for actual account despite current Pay-per-use documentation;
- signal quality is too poor for the cost;
- provider terms/rates materially invalidate the cost model.

### Outcome
Closed 2026-08-29 on a Pay Per Use project. Recent Search HTTP 200 at 225.9 ms; Filtered Stream
delivered 10 Posts in 16.9 s at 4.3-5.1 s lag with a clean rule create/delete cycle; total actual
spend `$0.055` of a `$0.10` ceiling. The Free plan was measured to return 403 on both endpoints and
cannot serve this product. Mode frozen in `ADR-010`.

### Artifact
`docs/spikes/SPIKE-X-001-RESULT.md`

---

# Non-blocking adapter spikes

## SPIKE-CAMPAIGN-001 — Galxe / PREMINT / Guild
Goal: select `API|OPTIONAL_API|PUBLIC_REFERENCE_ONLY|DISABLED` without protected scraping.

- Galxe structured path should be validated before production adapter enablement.
- PREMINT partner access is optional.
- Guild must have supported/public access or remain reference-only.

Artifact: `docs/spikes/SPIKE-CAMPAIGN-001-RESULT.md`.

## SPIKE-DUNE-001 — wallet cohort analytics — Phase 1.5
Measure cached/fresh result latency, credits/size, reproducibility and benchmark validity. Core radar must survive Dune unavailable.

Also validate AlphaWallet evaluation out-of-sample to reduce survivorship/look-ahead bias.

Artifact: `docs/spikes/SPIKE-DUNE-001-RESULT.md`.

## SPIKE-DISCORD-001 — permitted Discord intelligence — Phase 3
Use only explicitly authorized server/bot access. Test announcement read/member role data and required intents/permissions. No user token/self-bot/activity automation.

Artifact: `docs/spikes/SPIKE-DISCORD-001-RESULT.md`.

## SPIKE-RUNTIME-001 — runtime topology — RESOLVED
Prior spike/ADR selected hybrid topology with Railway worker + PostgreSQL and GitHub Actions only for non-critical batch/eval. Do not reopen absent new P0 evidence.

---

## Current execution order
**No Phase 1 blocking spike remains.** OpenSea, Telegram and X are all closed.

Remaining work is freeze reconciliation, then production implementation in the frozen order recorded
in `docs/PHASE_1_FROZEN_CONFIG.md`.

Campaign/Dune/Discord do not block Phase 1 unless a future ADR makes them mandatory.

## Phase 1 coding gate
Before production Phase 1 code:
- OpenSea live mapping resolved — DONE;
- Telegram delivery/config resolved — DONE;
- X resolved and mode frozen by ADR-010 — DONE;
- runtime already resolved;
- spike results reconciled into canonical design/status;
- no stale derived authority remains;
- no unresolved P0 provider feasibility ambiguity.
