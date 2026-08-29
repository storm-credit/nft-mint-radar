# ADR-012 — Upstream Discovery Path

## Status
Accepted — 2026-08-30

Supersedes the discovery-path assumption behind `ADR-011`'s slice 1 source choice. Does not change
any safety invariant, schema, or gate criterion. Adds one safety invariant.

## Context
Discovery was calendar-first: OpenSea `upcoming` produced candidates, everything else verified them.
Our own probes made that look thin — 14 drops on one run, 11 on another, across all three target
chains, with Base returning zero every time.

The user rejected the model directly: real mint access flows through **people** — known influencers,
the circle around them, the projects they converge on — and the goal is to reach whitelist eligibility.
The stated first step was to identify who those people are.

Research (`docs/research/SOURCE_ACCESS_RESEARCH_2026-08-30.md`) confirmed the instinct and refuted
the proposed channels.

### What the research established
1. **Membership is not access.** On Discord and Telegram, only a server or channel administrator can
   install a bot. The user belonging to an alpha community grants zero API rights over it, and alpha
   groups will not admit member-run bots because exclusivity is their product. Every tool that gets
   around this is a self-bot or userbot.
2. **Reddit is legitimately readable and consistently late.** Vote-ranked discussion cannot lead an
   allowlist that closes in minutes.
3. **Paid alpha groups have no evidenced edge**, and are frequently compensated in allowlist spots by
   the projects they call, which makes the "alpha" and the paid promotion the same object.
4. **The genuinely earliest legitimate signals are upstream of chat**: allowlist platforms with APIs
   (PREMINT and peers), and on-chain contract deployment. An allowlist opening on PREMINT precedes
   the announcement that reaches any alpha Discord.
5. **Robinhood Chain is a significant new venue** with sub-hour seven-figure sellouts, and it is
   drainer-dense. *(Corrected 2026-08-30: this point originally claimed Robinhood Chain had passed
   double Ethereum's NFT volume. It had not. CryptoSlam for the week to 2026-08-29 puts Ethereum at
   $35.56M organic sales against Robinhood's reported ~$1.05M/24h — Ethereum remains roughly 5x
   larger. The original claim came from one promotional-sounding source and was not cross-checked.
   The decision below does not depend on it: upstream-first discovery and the chat-platform
   exclusions rest on access facts, not on volume rankings.)*
6. **Mint count hit a record while revenue fell.** The scarce resource is filtering, not discovery.

## Decision

### 1. Discovery becomes upstream-first, not calendar-first
Phase 1 P0 discovery sources, in priority order:

1. **Allowlist platforms** (PREMINT and peers) — earliest legitimate signal of an obtainable
   allowlist. Promoted from P1 optional to **P0**.
2. **On-chain contract deployment and first-mint activity** — earliest signal in absolute terms.
   Already P0; now an active discovery trigger rather than only verification evidence.
3. **X, author-scoped** — the people layer, under `ADR-010`'s existing rule discipline.
4. **OpenSea and marketplace APIs** — demoted from discovery-first to **structured verification and
   stage/price detail**, which is what `ADR-007` already said it was good at.

### 2. Chat platforms are ruled out, with reasons recorded
- **Discord**: a reader may cover only servers the user administers. Build it only if such servers
  exist; never promise coverage of alpha groups the user merely belongs to. Self-bots stay forbidden.
- **Telegram**: excluded. Bot API cannot reach the channels that matter without admin consent. The
  MTProto userbot route is excluded **by our own design rule against user-account automation**, not
  by a clear Telegram prohibition — Telegram permits third-party clients, and the record should say
  so accurately. Web scraping collides with Telegram's AI-scraping terms exactly where a mint radar
  would use an LLM.
- **Reddit**: excluded as a discovery source. Retained only as a scam/rug warning feed, if at all.
- **Paid alpha groups**: not built toward. If their content ever surfaces, it must never be presented
  with implied credibility.

### 3. Influencers trigger discovery but still cannot raise quality
`ADR-004` caps influencer signal at +5 Alpha and +0 Quality, to resist shilling. That cap stands.

The resolution is that **discovery and scoring are different stages**. An influencer post may create
a candidate and may contribute Alpha through convergence — several independently-scored accounts
moving toward the same project within a window. It may not raise Quality, and it can never satisfy
verification. Verification remains the job of official surfaces, the allowlist platform, and on-chain
evidence.

### 4. New safety invariant — author-body-only link extraction
Drainer crews seed fake mint links into the reply and repost graph beneath legitimate verified
accounts, and register lookalike domains within hours of a real launch.

**Links are extracted from the author's own post body only. Never from replies, quote-posts, or
embedded cards.** Without this, an author-scoped rule harvests the phishing swarm along with the
signal, and the CTA gate becomes the only defense rather than the second one.

### 5. Chain priority
Scope stays Ethereum + Base + Robinhood Chain per `ADR-007` — no chain is added or removed. Within it,
**Ethereum and Robinhood Chain are both primary; Base is deprioritized** until evidence changes. Base's
zero-result probes are a market fact rather than an adapter defect.

Corrected 2026-08-30: an earlier revision made Robinhood Chain *the* primary venue on the strength of
a volume claim that did not survive cross-checking. Ethereum remains roughly 5x larger. Robinhood
Chain stays a first-class target because sub-hour seven-figure mints demonstrably happen there, not
because it leads.

### 6. Influencer seed list
Seeded from behaviour-sourced candidates, not follower counts: `@weingfo`, `@Rhynotic`, `@0xRohitz`,
`@AndreWGMI`, `@g13m`, `@Asher_0210`, plus `@zachxbt` and `@realScamSniffer` as a risk overlay.
Disclosed conflicts are recorded with the entries. Two widely-listed accounts are excluded because of
sourced scam allegations.

No account is assumed to be early. Each earns or loses its place from measured
`historical_lead_time_minutes` and `false_positive_rate`. **Follower count must not enter scoring** —
drainer operations inflate it, so it is adversarially manipulated evidence, not merely weak evidence.

## Consequences
- Slice 1's source changes from OpenSea to an upstream source. The domain primitives and the safety
  core built so far are unaffected and are reused as-is.
- PREMINT access becomes a Phase 1 question rather than a later one, and needs its own operational
  spike: current API terms, access conditions, cost, and whether it covers Robinhood Chain.
- `ADR-010`'s X mode is untouched, but its latency rationale weakens further: if filtering rather
  than speed is the scarce resource, seconds-level stream delivery matters less than `ADR-010`
  implied. Recorded, not yet acted on.
- Discord/Telegram/Reddit stop consuming design attention.

## What this ADR does not claim
- It does not claim the seed accounts are early. Zero lead-time measurements exist.
- It does not claim PREMINT is usable. That is now an open spike, not a settled fact.
- It does not claim the product thesis is proven. `BS-1` remains open; upstream sourcing improves the
  odds of answering it, it does not answer it.

## Revisit triggers
- the PREMINT spike shows the API is unavailable, unaffordable, or blind to Robinhood Chain;
- measured convergence signal from the seed list shows no lead time over the allowlist platform;
- Robinhood Chain activity collapses or another chain overtakes it;
- a platform's terms change such that a ruled-out source becomes legitimately readable.
