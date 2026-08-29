# Phase 1 Frozen Configuration

## Status
`FROZEN 2026-08-29`

This file records what Phase 1 implementation is allowed to assume. It is a freeze record, not a new
authority: every entry points at the document or ADR that owns the decision. If an entry here ever
disagrees with its owner, the owner governs and this file is stale.

Changing anything frozen here requires the regression rule in
`PRODUCTION_CODING_START_GATE.md` section I: mark affected artifacts STALE, stop the impacted path,
targeted revalidation, KEEP/PATCH/CUT first.

---

## Chains
Ethereum, Base, Robinhood Chain. Owner: `ADR-007`. No chain added or removed by `ADR-012`.

Priority within that set, per `ADR-012`: **Robinhood Chain is a primary hunting ground alongside
Ethereum, not ahead of it.** Mainnet launched 2026-07-01 and hosts sub-hour seven-figure mints, and it
is drainer-dense, so the CTA safety gate is load-bearing there rather than decorative.
**Base is deprioritized**: its creator/social strategy was publicly abandoned in July 2026, which
independently explains why every OpenSea probe returned zero upcoming Base drops.

**CORRECTED 2026-08-30.** An earlier revision of this file stated that Robinhood Chain "passed
double Ethereum's 24h NFT volume". That was wrong. It rested on a single promotional-sounding source
and was not cross-checked before being written into a frozen document. CryptoSlam data for the seven
days to 2026-08-29 shows **Ethereum at $35.56M organic sales**, roughly $5M/day, still the largest
NFT chain, against Robinhood Chain's reported ~$1.05M/24h — Ethereum is about **5x larger**, not
smaller. Global NFT sales that week were $63.33M, down from $114.5M.

What survives the correction: Robinhood Chain doing roughly $7M/week at two months old is a genuinely
notable and fast-growing venue, it is where several sub-hour seven-figure mints actually happened, and
it is drainer-dense. What does not survive: any claim that it has overtaken Ethereum.

No other chain is in Phase 1 scope, including chains that appear in a source's response.

## Runtime
Railway as the Phase 1 MVP target: one long-running `radar-worker`, managed PostgreSQL, optional
non-time-critical batch work on GitHub Actions. Owner: `ADR-006`.

Not yet activated. No production deployment has occurred, and none is authorized by this freeze.
Railway outbound/runtime activation remains an open pre-deployment check, listed as non-blocking in
the start gate section F.

## Implementation stack
**Python, targeting 3.11+.** Recorded 2026-08-29 when slice 1 started, because no document had frozen
a language and one was needed.

Rationale, in order of weight: the disposable spikes that produced every operational measurement in
this project are Python, so the team already reads it here; `.gitignore` was already written for a
Python project; Railway supports it as a first-class runtime under `ADR-006`; and the deterministic
hot path needs no capability Python lacks.

3.11+ rather than the newest release, so the Railway image is not constrained by a version that may
not be available there. Local development on a newer interpreter is fine as long as no
newer-than-3.11 syntax is used.

This is an implementation choice consistent with `ADR-006`, not a competing decision. If it ever
becomes contested, an ADR supersedes this entry.

## Persistence
PostgreSQL with append-only Evidence and a transactional outbox. Owner: `ADR-003`.

The outbox delivery state machine (`delivery_state`, `attempt_count`, `next_attempt_at`,
`claimed_until`, `provider_message_id`, `last_error`) is part of the frozen contract. A null `sent_at`
never authorizes a resend. Owner: `DEEP_DESIGN.md` section 2.12, fixture `F32`.

---

## Sources

### P0 runtime-capable
Discovery is **upstream-first**, not calendar-first. Owner: `ADR-012`.

| Priority | Source | Role | Frozen constraint |
|---|---|---|---|
| 1 | Allowlist platforms (PREMINT and peers) | earliest legitimate signal of an **obtainable** allowlist | promoted from P1; access/cost/chain coverage is an OPEN SPIKE, not a settled fact |
| 2 | Public EVM on-chain | earliest signal in absolute terms | now an active discovery trigger, not only verification evidence |
| 3 | Official X, author-scoped | the people layer | `ADR-010` rule discipline; **author body only** - see invariant 10 |
| 4 | Official websites/docs | T1 identity, links, schedule, contract, corrections | verified/corroborated surfaces only; bounded depth; content hash for edits |
| 5 | OpenSea drop/detail/stage | **structured verification and stage/price detail** | demoted from discovery-first; never a completeness authority |
| - | Galxe Quest API | quest discovery where access exists | live query required before production enablement |

### P1 optional
PREMINT (partner access only), Guild (supported surface only), Dune (Phase 1.5), official Telegram
announcement channels where permitted. Each degrades cleanly; none is a required runtime dependency.

### Weak discovery only
Reddit, public Telegram alpha groups, influencer mentions. These can raise attention. They cannot
raise Quality, and they cannot satisfy verification.

### NOT_READ_IN_PHASE_1
Magic Eden and other launchpads, Farcaster and community feeds, official GitHub, niche surfaces
without a supported read contract. Owner: `SOURCE_STRATEGY.md`.

Ruled out by `ADR-012`, with reasons, so they are not reopened casually:
- **Discord** - a bot reads only servers the user *administers*. Membership grants no API rights, and
  alpha groups do not admit member bots. Build only for self-administered servers; never promise
  coverage of alpha groups the user merely belongs to. Self-bots remain forbidden.
- **Telegram** - excluded. Bot API needs channel-admin consent. The MTProto userbot route is excluded
  **by our own rule against user-account automation**, not by a clear Telegram prohibition; Telegram
  permits third-party clients and the record should stay accurate about that. Web scraping collides
  with Telegram's AI-scraping terms exactly where a mint radar would use an LLM.
- **Reddit** - excluded for discovery; consistently late. Retained only as a scam-warning feed.
- **Paid alpha groups** - no evidenced edge, and typically compensated in allowlist spots by the
  projects they call. Never surfaced with implied credibility.

A mint appearing **only** on one of these produces no candidate. This is an accepted coverage gap and
must be reported as miss reason `coverage`, never as a parser or scoring failure.

---

## X configuration — frozen
Owner: `ADR-010`. Measured in `SPIKE-X-001`.

| Item | Frozen value |
|---|---|
| Mode | `STREAM_PRIMARY_WITH_SEARCH_RECOVERY` |
| Plan | Pay Per Use. Free tier returns 403 on both endpoints and cannot serve this product |
| Stream rules | author-scoped `from:` over verified official accounts, with `-is:retweet -is:reply` |
| Broad keyword-only rules | **forbidden**, including temporarily |
| Recent Search | recovery/backfill only, advanced by `since_id`; not a polling discovery loop |
| Recovery limit | 7 days. A longer outage is irreversible coverage loss and must be reported as such |
| Observed Post-read rate | `$0.005/resource` on 2026-08-29; the Developer Console is the execution-time authority |
| Pay-per-use cap | 3,000,000 Post reads/month |
| Observed stream delivery | 4.3-5.1 s on a 10-Post sample. Not an SLO |
| Signal yield | **unproven**. Degrade to `X_OPTIONAL` under ADR-002 if measured ROI stays poor |

## Telegram configuration — frozen
Owner: `ADR-003`, measured in `SPIKE-TG-001`.

Bot token via secret only. Chat target resolved from the bot's private conversation; an explicit
`TELEGRAM_CHAT_ID` remains supported. Delivery is confirmed by provider `message_id`. Telegram is not
treated as exactly-once transport: deduplication is the local outbox's responsibility.

## Budgets
Per-adapter request/record/cost accounting with hard daily and monthly caps as deterministic
configuration. Budget exhaustion sets the adapter `DEGRADED`. There is no path to surprise overspend,
and no model decides a budget. Owner: `DEEP_DESIGN.md` section 12, `METRICS_SLO.md`.

---

## Safety invariants that implementation may not weaken
These are the guarantees the Red Team closed. They belong in deterministic code, schema, or CI — never
in prompt text alone.

1. No wallet signature, approval, transaction, minting, seed handling, Discord self-bot, fake
   engagement, or impersonation path exists anywhere in the system.
2. Only an `ActionLinkAssessment` with `safety_state = CONSISTENT` may render as a wallet-impacting
   CTA. `official_action_url` is source evidence and is never rendered.
3. `unavailable` evidence is not `current` evidence for ACTION/URGENT severity, stage transitions, or
   any CTA.
4. A single account-based official source cannot escalate a new or shortened deadline, or a
   transition to OPEN, to URGENT or to a CTA.
5. A stage never becomes OPEN because the local clock passed `open_at`.
6. `CANCELLED` and `EXPIRED` are always-legal Opportunity transitions; entering `CANCELLED` revokes
   the CTA and stops reminders.
7. Missing verification evidence suppresses or downgrades action. It never fails open.
8. Collected source content is untrusted data. Extract from it; never obey it.
9. Secrets live only in runtime/environment/secret storage, never in evidence, logs, or the repo.
10. Links are extracted from the **author's own post body only** - never from replies, quote-posts, or
    embedded cards. Drainer crews seed fake mint links into the reply graph beneath legitimate
    verified accounts and register lookalike domains within hours of a real launch. Without this,
    an author-scoped rule harvests the phishing swarm along with the signal.
11. Follower count never enters scoring. Drainer operations inflate it, so it is adversarially
    manipulated evidence, not merely weak evidence.

## Model-driven node boundary
Only four nodes may be model-driven in Phase 1: unstructured signal extraction, ambiguous entity
resolution, Phase 2 quest parsing, and independent critique. Owner: `ADR-009`,
`LOCAL_ACTION_SPACE_AUDIT.md`.

Scoring math, state transitions, dedup, budget enforcement, the CTA safety verdict, the notification
send decision, and Telegram transport are deterministic. No central agent orchestrates the pipeline.

---

## Implementation order — vertical-first (ADR-011)
`ADR-011` replaced the horizontal sequence below with a vertical-first order, after a blind-spot sweep
showed that the horizontal order answers the product's three CRITICAL open questions last.

### Slice 1 - thinnest end-to-end path
Source changed by `ADR-012` from OpenSea to an upstream source. The exact source waits on the
allowlist-platform spike; on-chain deploy monitoring is the fallback if that spike fails.

    upstream source -> minimal Project/Campaign/Stage/Opportunity -> Evidence -> CTA safety gate ->
    deterministic decision -> Telegram renderer + outbox -> one real alert

The domain primitives and safety core already built are unaffected and are reused as-is.

Thin in coverage, never in safety: all eleven invariants above apply from the first commit.

Required alongside slice 1, because the slice cannot measure what it exists to measure without them:
- `human_action_latency` = `user_seen_or_ack_at - notification_sent_at`;
- a low-frequency liveness/status signal, so silence is distinguishable from a dead worker;
- a user operating profile: timezone, sleep/work blackout, escalation threshold.

### After slice 1
Widen outward from the working path, choosing the next step by what the slice measures.

### Coverage checklist (no longer the sequence)
The list below remains the set of things Phase 1 must eventually contain. `ADR-011` governs the
order in which they are built.

1. canonical domain primitives
2. evidence / identity / CTA-safety core
3. persistence, evidence history, transactional outbox
4. OpenSea adapter
5. official website and on-chain adapters
6. X adapter in the frozen mode
7. normalization and campaign/stage/opportunity state machines
8. deterministic scoring
9. deterministic decision gate
10. Telegram renderer and notifier
11. scheduler/worker
12. fixture and eval runner
13. integration tests
14. controlled end-to-end dry run

Build the smallest working slice at each step. Spike code is never promoted into production code.

## Open pre-deployment checks (do not block coding)
Galxe live query before adapter enablement; Dune freshness and out-of-sample AlphaWallet validation in
Phase 1.5; Discord authorized server read in Phase 3; Railway outbound/runtime activation before any
deployment; a targeted non-native OpenSea payment-asset sample when one is available.
