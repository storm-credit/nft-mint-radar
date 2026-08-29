# SPIKE-WL-001 Result — Allowlist platform access

## Status
**ONE VIABLE PLATFORM FOUND / DECISION BLOCKED ON A PAID ONE-MONTH TRIAL**

Research only, zero cost. Opened by `ADR-012`, which promoted allowlist platforms to P0 discovery.

## Question
Can a single-user tool legitimately read *other projects'* currently-open allowlists, and does that
data cover the chains we care about?

---

## Verdict table

| Platform | Public API | Third-party read of others' lists | Auth | Cost | Robinhood Chain | Alive | Verdict |
|---|---|---|---|---|---|---|---|
| **Alphabot** | Yes — live OpenAPI 3 spec v1.0.8 | **Yes** — `GET /raffles` is site-wide | Bearer key, self-service | $8/mo annual, $12/mo monthly | **Yes — `RH`, chainId 4663** | Yes, verified live | **Only viable option** |
| PREMINT | "Project API" page exists | **NOT VERIFIED** — doc fetch failed twice | unknown | unknown | NOT RESEARCHED | site up; ToS last updated 2022-03-30 | unresolved, smells stale |
| Atlas3 | none found | NOT VERIFIED | — | — | NOT RESEARCHED | page loads; no evidence of life or death | likely dead end |
| Superful, Mintify, Galxe, Layer3 | NOT RESEARCHED | — | — | — | — | — | — |

`ADR-012` named PREMINT as the likely candidate. That was wrong in emphasis: PREMINT could not be
verified at all, and **Alphabot** is the platform that actually satisfies the requirement.

## Alphabot — why it qualifies

Third-party read is **self-service, not partner-gated**. From the live spec:

> "Any user or team with an active subscription can access this API. Users with a premium
> subscription can find and refresh their API key and Webhook URL in their profile"

No project ownership, no partner application, no approval step. `GET /raffles` returns "a paginated
list of raffles using the same sorting and filtering options found on the Alphabot website" and is
marked available to **User**, not just Team. That is the read we need.

Robinhood Chain support was confirmed from their own app bundle, not from marketing copy:
`{name:"Robinhood",symbol:"RH",chainId:4663,isEvm:true,nativeToken:"ETH"}`.

Terms permit the API and forbid scraping, which is the right way round:

> "Right to Use Our APIs. Subject to these Terms, we hereby grant you a non-exclusive,
> non-transferable, non-sublicensable, worldwide, revocable right and license to use our APIs"

against a separate clause prohibiting robots, spiders and crawlers against the site itself. Logged
out, the site shows only marketing, so there is no public surface to read even if we wanted to.

Note the ToS also says **"personal non-commercial use only"** — fine for this tool as specified, and
a hard blocker if it were ever productised.

### Limits the marketing does not mention
- `/projects`, `/projects/{id}` and `/winners` are **Team-only**. A personal subscriber cannot use them.
- `/raffles` has **no blockchain filter** — that filter lives on the team-gated `/projects`. Robinhood
  filtering must happen client-side on the returned `blockchain` field.
- **30 requests/hour** on `/raffles`, page size max 50.
- Webhooks partly compensate: `raffle:active` and `project:minting` are User-available, and
  `project:minting` fires roughly 15 minutes before mint. But **`raffle:created` is Team-only**, so a
  personal account learns a raffle exists when it *opens*, not when it is created. That is a real
  reduction in the lead time this path was chosen for.

---

## The finding that should make us cautious

The researcher verified that Alphabot **supports** Robinhood Chain. They could **not** verify that a
single actual Robinhood Chain mint has run through an Alphabot raffle. Those are different claims,
and the second is the one the product depends on. A chain entry in an enum is cheap to add; it is
evidence of ambition, not of liquidity.

This lines up with `SPIKE-CHAIN-001`, which found that Robinhood Chain's two largest mints were open
or free with no whitelist at all, and that the gated ones used token burns or holdings rather than an
allowlist signup.

Honest synthesis: allowlist platforms look substantially like an **Ethereum-2022 artifact**. The
mechanic they automate — sign up days early, prove Discord/X engagement, get drawn — presumes mints
that oversubscribe *and* teams that want to pre-distribute access. Robinhood Chain has so far resolved
that differently. Alphabot may be a good feed for the wrong chain: strong on legacy Ethereum allowlist
flow, thin exactly where several recent mints happened.

## A correction this spike forced

The researcher challenged a claim this project had already written into frozen documents: that
Robinhood Chain had passed double Ethereum's NFT volume. Cross-checking confirmed the challenge.
CryptoSlam for the seven days to 2026-08-29 shows **Ethereum at $35.56M organic sales**, still the
largest NFT chain, against Robinhood's reported ~$1.05M/24h — **Ethereum is roughly 5x larger**.

The original figure came from one promotional-sounding source and was accepted without cross-checking.
`ADR-012`, `PHASE_1_FROZEN_CONFIG`, `PROJECT_STATUS`, `SPIKE_PLAN` and the research record have all
been corrected. Robinhood Chain remains a first-class target because sub-hour seven-figure mints
demonstrably happen there — not because it leads.

---

## Recommendation — a bounded paid trial, with a kill condition

Alphabot is the only platform worth an access attempt, and it is cheap: **$8–12/month, self-service,
no gatekeeper, terms-clean via the documented API**.

It should be bought as a **one-month spike, not as a build decision**. The single thing that must be
true before any production integration:

> `GET /raffles` returns a non-trivial, sustained flow of raffles with `blockchain == "RH"`.

That is one API call, paged for a week. If Robinhood entries are a handful of stragglers while the
real mints happen open and free on-chain, then discovery for this cycle belongs on-chain — which
`SPIKE-CHAIN-001` already found to be cheap and buildable — and the allowlist-platform branch is
killed rather than half-built.

This requires the user's money and therefore the user's decision. It is not authorized by this spike.

## What could not be verified
- **PREMINT's Project API** scope, auth, cost and chain coverage. The decisive question for that
  platform; the docs page timed out twice. NOT RESEARCHED, not inferred.
- **Atlas3** beyond "the domain serves a page". `api.atlas3.io` and `docs.atlas3.io` do not resolve,
  but absence was not confirmed.
- **All peer platforms** — Superful, Mintify, Magic Eden, Galxe, Layer3.
- **Whether any real Robinhood Chain mint has used Alphabot.** The most important open question, and
  it needs a paid key to answer.
- Alphabot's rate limits and tier gating are quoted from its own spec and were not tested live.

## Gate impact
`ADR-012` promoted allowlist platforms to P0 discovery on the assumption that access existed. Access
does exist, on one platform, cheaply. Whether the data covers the mints we care about is unproven,
and slice 1's source remains undecided until the trial runs or the branch is killed.
