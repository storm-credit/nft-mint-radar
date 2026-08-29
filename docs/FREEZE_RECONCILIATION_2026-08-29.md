# Freeze Reconciliation — 2026-08-29

## Purpose
Start gate section G. Verify that after the cross-system Red Team patches, no derived
schema/prompt/fixture/spike mapping is stale, freeze the Phase 1 source/runtime configuration, and
confirm no unresolved P0 provider ambiguity remains.

## Method
An independent read-only sweep was given the ten facts that changed during the day and asked to find
every document that still asserts an older version, every pair of documents that now disagree, every
reference to a schema field or fixture that does not exist, and every new hard rule that no fixture
exercises. Historical spike results and changelog entries describing an earlier date were explicitly
out of scope, so they would not be reported as stale.

18 findings returned; every cited line was re-read before acceptance. All 18 were accepted and closed.

## P0 findings closed

### F-012 — the `unavailable` safety rule referenced a field that did not exist
The Red Team patch made "`unavailable` evidence is not `current` evidence" a load-bearing safety rule,
and `DEEP_DESIGN.md` had said "mark unavailable" since before that. But the `Evidence` schema had no
availability field. `verification_state` carries `STALE` and `REVOKED`, neither of which means "the
source can no longer be fetched". The rule was therefore unimplementable, and `F29` asserted an
outcome no schema could produce.

**Closed:** `Evidence` gains `source_availability: AVAILABLE|UNAVAILABLE|UNKNOWN` and
`source_unavailable_since`. Availability is deliberately separate from verification: a deleted post is
`UNAVAILABLE` without becoming `REVOKED`, because disappearance is not disavowal.

This is the most valuable finding of the sweep. It was created by the same session that wrote the rule.

### F-001, F-002 — README advertised a superseded gate
`README.md` still showed `SPIKE_REQUIRED` and listed Telegram and X as remaining blockers.
**Closed:** gate corrected to `FREEZE_PENDING`, blocker list replaced with a pointer to
`PROJECT_STATUS.md`, and the completed list updated.

### F-003 — credential readiness still claimed an outstanding X blocker
**Closed:** blocker count is now zero; both secrets are configured and exercised.

### F-006, F-007 — the spike plan still described closed spikes as blocking and X mode as provisional
**Closed:** both spikes marked closed, provisional mode replaced with the `ADR-010` frozen mode and
its constraints, execution order replaced with freeze reconciliation.

## Non-P0 findings closed
| ID | Finding | Close |
|---|---|---|
| `F-004`, `F-005`, `F-008` | superseded 2,000,000 Post-read cap in three files | 3,000,000, with the earlier revision kept where it is historical |
| `F-009` | `PROJECT_STATUS` claimed synchronization that was not yet true | claim narrowed and dated, pointing at this record |
| `F-010` | start gate said the Red Team was both complete and remaining | remaining-work list corrected |
| `F-011` | `HARNESS_SCHEMAS` discovery candidate tokens did not match canonical `event_type` values | declared coarse discovery classes that must be mapped during normalization and never persisted as event types |
| `F-013`–`F-018` | six new hard rules had no fixture | `F33`–`F38` added |

## Fixtures added
- `F33` deadline passes with no result evidence -> `EXPIRED`
- `F34` unavailable evidence cannot open a stage
- `F35` `official_action_url` is never rendered directly
- `F36` fingerprint buckets come from claim time; wording-only correction does not re-alert
- `F37` cursor never advances ahead of persisted evidence
- `F38` X stream rule discipline: keyword-only rejected, author-scoped accepted

Fixture count is now `F1`–`F38`.

## Chain scope — re-confirmed, not reopened
The question of BNB Chain and Solana was raised during reconciliation and answered with measurement
rather than opinion. OpenSea probe run `33257068301`:

- `bnb`, `bsc`, `binance`: **unresolved** — OpenSea does not expose a matching chain identity;
- `solana`: chain identity resolves, but the upcoming-drops query returns **HTTP 400**;
- `ethereum` 6 upcoming, `robinhood` 5, `base` 0, `polygon` 0, `arbitrum` 0.

So neither chain is a configuration toggle. BNB is EVM and reuses the domain model and on-chain
adapter, but our P0 structured discovery source returns nothing for it, so it would need a new
discovery adapter. Solana is non-EVM and would additionally require generalizing `ChainIdentity`,
address validation, contract matching and the CTA safety path, plus un-forbidding a Solana discovery
source that this same day's Red Team declared `NOT_READ_IN_PHASE_1`.

**Decision: Phase 1 chain scope stays Ethereum + Base + Robinhood, per `ADR-007`.** The measurement is
retained so the revalidation trigger in `ADR-007` — another chain repeatedly contributing missed
S/A-grade opportunities — can be judged against production miss data instead of intuition.

## Section G status
- [x] OpenSea spike result saved and reconciled
- [x] X paper/access contract reconciled
- [x] Telegram real-delivery result saved
- [x] X credentialed result saved
- [x] final X source mode and budget assumptions updated (`ADR-010`)
- [x] no derived schema/prompt/fixture/spike mapping is stale
- [x] Phase 1 source/runtime configuration frozen (`docs/PHASE_1_FROZEN_CONFIG.md`)
- [x] no unresolved P0 provider ambiguity

## Verdict
Freeze reconciliation complete. Unresolved P0 = 0.
