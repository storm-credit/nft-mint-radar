# Project Status

## Current verdict

**All Phase 1 blocking operational spikes closed (OpenSea, Telegram, X) / X mode frozen in ADR-010 /
cross-system Red Team complete with P0 = 0 / freeze reconciliation complete / Phase 1 configuration
frozen / Production coding AUTHORIZED for Phase 1 in the frozen order**

Current gate: **`PHASE_1_CODING_READY`**.

Cross-system Red Team ran 2026-08-29 and closed every P0. Freeze reconciliation completed the same
day (`docs/FREEZE_RECONCILIATION_2026-08-29.md`) and the Phase 1 configuration is frozen
(`docs/PHASE_1_FROZEN_CONFIG.md`).

Current state is stated here and, as a dated decision record, in
`docs/PRODUCTION_CODING_START_GATE.md`. No other document restates it — they point here.

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

Cross-system Red Team 2026-08-29 (`docs/RED_TEAM_2026-08-29.md`): 5 P0 raised, 4 accepted, 1
downgraded to P1, 6 P1 accepted, **all closed by PATCH**, unresolved P0 = 0. No NEW DESIGN was
required. Derived artifacts were synchronized in the same change: `HARNESS_SCHEMAS` gained the
`ActionLinkAssessment` CTA carrier, `urgency_corroboration`, and opportunity-state hard rules;
`EVAL_FIXTURES` gained `F29`-`F32`.

Design changes worth carrying into implementation:
- `unavailable` evidence is not `current` evidence for ACTION/URGENT/CTA;
- a single account-based official source cannot escalate a new or shortened deadline to URGENT;
- `Opportunity.state` is a finite enum with always-legal `CANCELLED`/`EXPIRED`;
- the outbox has an explicit delivery state machine; a null `sent_at` never authorizes a resend;
- `official_action_url` is never renderable; only an `ActionLinkAssessment` reaches the user.

Cross-artifact consistency audit on 2026-08-29 (canonical docs vs `spikes/` runners vs `.github/workflows/`)
found and closed two doc-vs-code contradictions: an X Recent Search cap that was documented as enforced but
existed only as an outbound request parameter, and a `--max-results` flag documented in `spikes/README.md`
that the runner never accepted. See the 2026-08-29 entry in `docs/deviations/CHANGELOG_DECISIONS.md`.
No shadow-authority finding. No architecture, schema, or ADR change.

`DEEP_DESIGN`, `ARCHITECTURE`, `SOURCE_STRATEGY`, `SOURCE_ADAPTER_CONTRACTS`, `HARNESS_SPEC`,
`HARNESS_SCHEMAS`, `PROMPT_CONTRACTS`, `EVAL_FIXTURES`, `SPIKE_PLAN`, `README`,
`CREDENTIAL_READINESS`, and the Production Coding Start Gate were re-swept on 2026-08-29 after the
Red Team patches and synchronized to the current design. The sweep is recorded in
`docs/FREEZE_RECONCILIATION_2026-08-29.md`.

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

## Telegram operational spike — PASS
See `docs/spikes/SPIKE-TG-001-RESULT.md`.

Real delivery observed 2026-08-29 (run `33255435740`):
- provider HTTP 200, `ok: true`, `message_id: 4`, latency 467.8 ms;
- chat resolved automatically via `getUpdates-private-chat`; no `TELEGRAM_CHAT_ID` configured;
- `chat_id_matches: true`; Korean text sent; `cta_present: false`;
- one `sendMessage` call produced exactly one provider Message.

Fail-closed behavior observed on the same bot before `/start` existed
(runs `33254983732`, `33255307246`): `update_count: 0`, no send attempted, no target guessed.

Bot in use: `@nftmr_bot`. `TELEGRAM_CHAT_ID` was never needed.

Dedup remains a local outbox responsibility; Telegram is still not treated as
exactly-once transport, and this spike does not claim to prove repeat-suppression.

---

## X operational spike - CLOSED, mode frozen
See `docs/spikes/SPIKE-X-001-RESULT.md` and `ADR-010`.

Measured 2026-08-29, total actual spend **$0.055** of an approved `$0.10` ceiling:
- Free-plan project 403s on both endpoints; **Pay Per Use is required**;
- Recent Search: HTTP 200, 225.9 ms; `from:opensea` returned 1 Post in 7 days, useful 0 / noise 1;
- Filtered Stream: 10 Posts in 16.9 s, delivery lag **4.3-5.1 s (mean about 4.8 s)**, better than
  the documented ~6-7 s P99;
- temporary rule create/delete lifecycle clean, `cleanup_status: 200`, nothing left behind;
- broad keyword rule produced **useful 0 / noise 10** at about 35 Posts/min, about **$250/day**.

Frozen mode: **`STREAM_PRIMARY_WITH_SEARCH_RECOVERY`**, with author-scoped rules mandatory,
broad keyword rules forbidden, Recent Search restricted to recovery, deterministic source budget,
and degradation to `X_OPTIONAL` if production signal ROI stays poor.

Proven: access, latency, rule lifecycle, cost mechanics.
**Not proven: signal yield.** Neither tested query shape produced an actionable mint signal,
which is why the degradation path is part of the frozen decision.

## Remaining Phase 1 P0 blockers - 0

All three Phase 1 blocking operational spikes are closed: OpenSea, Telegram, X.

No user-owned credential is outstanding. `TELEGRAM_BOT_TOKEN` and `X_BEARER_TOKEN` are configured
and both have been exercised against live providers.

Every pre-coding gate is closed: cross-system Red Team (P0 = 0, 2026-08-29), freeze reconciliation
across derived artifacts, and the Phase 1 configuration freeze. Nothing blocks implementation.

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
**AUTHORIZED for Phase 1** as of 2026-08-29, in the frozen implementation order in
`docs/PHASE_1_FROZEN_CONFIG.md`. Later phases remain out of scope; designing their interfaces is
allowed, implementing their behavior is not.

The regression rule still applies: if new evidence invalidates a frozen assumption, mark the affected
artifacts STALE, stop the impacted path, and re-enter only the affected gate criteria.

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
- [x] Telegram real delivery complete.
- [x] X credentialed bounded run complete and final mode frozen (ADR-010).
- [x] remaining results reconciled into canonical status/ADR.
- [x] no unresolved P0 provider feasibility ambiguity.

---

## Discovery path changed 2026-08-30 — ADR-012
The user rejected calendar-first discovery: real mint access flows through people, and the goal is
whitelist eligibility. Research confirmed the instinct and refuted the proposed channels.

- **Membership is not access.** Discord and Telegram grant bot read rights to community *operators*,
  not members. A compliant reader covers only servers the user administers. Every tool that gets
  around this is a self-bot or userbot.
- **Reddit is legitimately readable and consistently late.** Retained only as a scam-warning feed.
- **Paid alpha groups have no evidenced edge**, and are typically paid in allowlist spots by the
  projects they call.
- **The earliest legitimate signals are upstream of chat**: allowlist platforms with APIs, then
  on-chain deployment, then author-scoped X. Both were already in the source list — the priority
  order was wrong, not the list.
- **Robinhood Chain is where the current cycle is** (>2x Ethereum NFT volume, sub-hour seven-figure
  sellouts) and it is drainer-dense. Base's creator strategy was publicly abandoned in July 2026,
  which explains our zero-result Base probes as a market fact, not an adapter defect.
- **Mint count hit a record while revenue fell**: the scarce resource is filtering, not discovery.

Two new safety invariants: links come from the author's own post body only, never the reply graph
where drainers seed fake mint links; and follower count never enters scoring, because it is
adversarially inflated.

Evidence: `docs/research/SOURCE_ACCESS_RESEARCH_2026-08-30.md`.

**New open spike:** allowlist-platform (PREMINT and peers) access, cost, and whether it covers
Robinhood Chain. Slice 1's source now waits on it, with on-chain deploy monitoring as the fallback.

## Next action
Resolve the allowlist-platform spike from `ADR-012`, then build slice 1 against the chosen upstream
source. `ADR-011`'s vertical-first shape is unchanged; only the source moved.

A blind-spot sweep (`docs/BLIND_SPOT_SWEEP_2026-08-29.md`) found no safety defect and no unmet gate
criterion, but three CRITICAL open questions that the original horizontal order would have answered
last: whether useful signal volume exists at all, how late the human actually sees an alert, and
whether silence is distinguishable from a dead worker. Slice 1 measures all three at once.

The slice is thin in coverage, never in safety. Keep spike code out of production code.

Rules that survive the gate and must not be weakened during implementation:
- the nine safety invariants in `docs/PHASE_1_FROZEN_CONFIG.md`;
- deterministic-first: scoring, state transitions, dedup, budget, CTA verdict, send decision and
  Telegram transport are code, not prompts;
- fixtures `F1`-`F40` are the acceptance contract, not documentation.

Carry into implementation: X signal yield is unproven. `METRICS_SLO` already measures source ROI by
median unique lead time, so this resolves as data rather than as an assumption — but no design may
quietly depend on X being first.
