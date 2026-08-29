# Source Access and Landscape Research — 2026-08-30

## Why this exists
The user challenged the discovery model: the radar was finding opportunities from a marketplace
calendar, but real mint access flows through **people** — known influencers, the circle around them,
and the projects they converge on. The stated goal was to reach whitelist/mint eligibility, and the
stated first step was "we need to know who those people are."

Two independent research passes were run to answer that. This file retains what they found, with
sources, so the resulting decision in `ADR-012` can be audited later.

**Sourcing caveat, stated up front.** X profile pages returned HTTP 403 to the researchers, and so
did `support.discord.com`, `support-dev.discord.com`, `support.reddithelp.com` and `redditinc.com`.
Claims from those sources came via search snippets or archived copies and are marked as such below.
Anything load-bearing must be re-verified against the live page before code depends on it.

---

## 1. The market changed shape, and it moved

- NFT trading volume is down roughly **93%** from peak; art-NFT monthly sales down **>98%** from the
  August 2021 peak; active NFT-trading wallets fell from ~529,000 to under 20,000
  ([DappRadar](https://dappradar.com/blog/nft-arts-shocking-collapse-from-2-9-billion-boom-to-23-8-million-bust-what-went-wrong),
  [crypto.news](https://crypto.news/nft-industry-impact-activity-slow-marketplace-collapse/)).
  Marketplace X2Y2 shut down citing "90% shrinkage".
- **Robinhood Chain is where the current mint cycle is.** Mainnet launched 2026-07-01
  ([Forbes](https://www.forbes.com/sites/ninabambysheva/2026/07/01/robinhood-launches-its-own-blockchain-new-stock-tokens-and-defi-products/))
  and within weeks posted more than double Ethereum's 24-hour NFT volume
  ([Crypto Briefing](https://cryptobriefing.com/robinhood-chain-surpasses-ethereum-nft-volume/)).
  Mints sell out in under an hour for seven figures — Spritehood took $1.28M in 53 minutes
  ([KuCoin](https://www.kucoin.com/news/flash/spritehood-nft-mint-generates-1-28m-on-robinhood-chain-in-53-minutes)).
- **Base weakened.** In July 2026 Jesse Pollak publicly conceded the onchain-social/creator strategy
  had failed and stepped back from Base App leadership
  ([CoinDesk](https://www.coindesk.com/business/2026/07/15/coinbase-s-jesse-pollak-steps-back-from-base-app-leadership-after-admitting-his-crypto-social-strategy-failed)).
  This independently explains why our own OpenSea probes returned **0 upcoming Base drops** on every run.
- **Robinhood Chain is scam-dense**, with widespread drainers, phishing pages and rug-pulls since
  launch ([Protos](https://protos.com/the-controversial-return-of-pudgy-penguins-founder-colethereum/)).
- Mint **count** hit a record ~1.34B in 2026 while revenue fell: supply exploded as demand collapsed.

**The line that reframes the product:** the scarce resource is **filtering, not discovery**. A radar
optimized purely for speed surfaces a torrent of worthless mints.

---

## 2. Chat platforms: membership is not access

This is the finding that killed most of the proposed approach.

**Discord.** A bot reads a server only if someone with Manage Server permission invites it. The
user's own membership in an alpha server grants no API rights, and alpha groups do not permit
member-run bots because information exclusivity is their product. A compliant Discord reader
therefore covers **only servers the user administers** — near-zero coverage for alpha purposes.

Self-bots are explicitly prohibited. Discord ToS §9, effective 2025-09-29
(<https://discord.com/terms>):

> "scraping our services without our written consent, including by using any robot, spider, crawler,
> scraper, or other automatic device, process, or software"

Discord's Developer Policy (archived 2022-10-01 revision in Discord's own docs repo —
[source](https://raw.githubusercontent.com/discord/discord-api-docs/48d3c2d324796d8236355262ace3b22c1d29acb0/docs/policies_and_agreements/Developer_Policy.md)):

> "You may not mine or scrape any data, content, or information available on or through Discord services"

The popular libraries in this space (`discord.py-self`, `discord.js-selfbot-v13`) are self-bot
tooling. Rate limiting and human-like delays are evasion, not compliance.

A legitimate bot, where a server admin does invite it, needs gateway intents `GUILD_MESSAGES` and the
privileged `MESSAGE_CONTENT`, plus `VIEW_CHANNEL` and `READ_MESSAGE_HISTORY`. The privileged-intent
review threshold is now **10,000 unique users**, so a single-user tool needs no Discord review — the
only gate is admin consent. Reported policy also restricts using Discord message content to train or
run ML/AI models without permission; **not verified verbatim against the live page.**

**Telegram.** Same structural blocker: only a channel administrator can add a bot. Telegram Bot API
10.3 (2026-08-24, <https://core.telegram.org/bots/api>) delivers `channel_post` updates, and the Bot
FAQ confirms bots receive "All messages from channels where they are a member" — but membership is
granted by the admin, not the subscriber.

The MTProto client API would read everything the *user* has joined. Stated precisely, because this
distinction matters: Telegram **permits third-party clients**, so a userbot is not the clear ToS
violation a Discord self-bot is. It is excluded by **our own design rule** against user-account
automation, and it carries ban risk — not because Telegram forbids it.

Public-channel web scraping via `t.me/s/<channel>` is trivial, but Telegram's Content Licensing and
AI Scraping Terms (<https://telegram.org/tos/content-licensing>) state:

> "Telegram firmly prohibits the scraping, indexing, harvesting, aggregation or use of data obtained
> from its platform to train, fine-tune, validate or otherwise engage in the development,
> enhancement, benchmarking or deployment of artificial intelligence, machine learning models and
> similar technologies."

The prohibition is scoped to AI/ML use. A pure regex filter arguably sits outside it — but the moment
scraped posts feed an LLM to classify mints, which a mint radar naturally wants, it is inside.

**Reddit.** Legitimately accessible and free at our volume, but **consistently late**: Reddit is a
vote-ranked discussion medium and allowlists close in minutes. Access rules changed hard and recently
— unauthenticated `.json` endpoints were deprecated 2026-05-28 and now return 403; a Responsible
Builder Policy (reported updated 2026-06-05) requires approval before access, with self-service
registration reportedly closed and a 2–4 week manual turnaround; free tier is 100 queries/minute.
**All four Reddit policy pages 403'd; these figures are from secondary reporting and must be
re-verified.** Reddit's real value here is negative signal — rug reports and scam warnings.

---

## 3. Paid alpha groups: no evidence of edge

No independent performance data was found. No audited track records, no third-party backtests, no
academic study. Every performance claim traces back to the groups' own marketing or to affiliate
content earning referral fees.

The structurally identical **paid crypto signal group** does have literature, and it is damning:
signal groups are organized exactly like pump-and-dump groups, and paid tiers advertising better
accuracy do not remove the underlying structure
([arXiv:2105.00733](https://arxiv.org/pdf/2105.00733), which documented **1,108 pump-and-dump events**
across 4 exchanges; see also [arXiv:2503.01686](https://arxiv.org/html/2503.01686v1)).

The mechanic that matters most: alpha groups are frequently **compensated in allowlist spots by the
projects they call**. The "alpha" and the paid promotion are structurally the same object.

---

## 4. The upstream sources that are earlier *and* legitimate

The researchers converged, unprompted, on the same answer:

1. **Allowlist platforms.** PREMINT is the dominant Ethereum access-list service (~70M registration
   entries, 40k+ projects including XCOPY, Murakami, Moonbirds) and offers documented API access
   (<https://www.premint.xyz/>, <https://docs.premint.xyz/fundamentals/raffles>). Alphabot and Atlas3
   are peers. **An allowlist opening on PREMINT is strictly earlier than the announcement that
   reaches an alpha Discord** — it is upstream of the thing we were trying to read.
2. **On-chain contract deployment monitoring.** New ERC-721/1155 deploys and first-mint transactions
   need nobody's permission and are the earliest signal in absolute terms.
3. **Marketplace APIs.** OpenSea drops, Magic Eden, Reservoir, Alchemy.

Both PREMINT and on-chain were **already in our source list** — PREMINT as P1 optional, on-chain as
P0. The source list was not wrong. The priority order was.

---

## 5. Candidate X seed accounts

Behavior-sourced tier — the researcher read actual mint-call posts from these, rather than trusting a
listicle:

| Handle | Observed behavior |
|---|---|
| `@weingfo` | Structured pre-mint cards: project, founder, supply, price, date, chain, before details are public |
| `@Rhynotic` | Precise pre-mint allowlist mechanics: per-collection allocation, AL window length, over-allocation warnings |
| `@0xRohitz` | Robinhood Chain free-mint calls including team lineage |
| `@AndreWGMI` | Robinhood Chain commentary with explicit skepticism ("would not call it a full NFT comeback") |
| `@g13m` | Ranks live Robinhood collections by volume and mechanics — lagging, useful for triangulation |
| `@Asher_0210` | Odaily journalist mapping Robinhood Chain projects; structurally late, useful for seed expansion |
| `@zachxbt` | On-chain investigator, 100+ scams exposed — reactive, so a kill-switch feed, not a lead source |
| `@realScamSniffer` | Real-time phishing and drainer alerts |

Disclosed conflicts, recorded rather than hidden: `@fxnction` states he is launching on Robinhood
Chain himself, so he is not a neutral observer; `@ninjalerts` monetizes a paid alpha tier.

**Excluded from the seed, with cause.** `Serpent` is described in older coverage as a security
analyst, but ZachXBT later accused him of orchestrating memecoin scams totalling $3.5M+
([icoholder](https://icoholder.com/en/news/zachxbt-accuses-serpent-of-3-5m-memecoin-scam-in-crypto)).
`Beanie` is repeatedly listed as an OG alpha caller, but faced a detailed serial-scamming allegation
thread and $BGLD rug association ([RedLion](https://www.redlion.news/article/beanie-got-doxxed)).
These are sourced allegations, not proven findings — but a person accused of running scams is the
worst possible occupant of a risk-signal feed, so neither is seeded.

**Nobody on this list is verified to be early.** Lead-time measurements are zero, because X profile
pages 403'd. Every "known for" is a description, not a track record. This is exactly the gap
`InfluencerEntity.historical_lead_time_minutes` and `false_positive_rate` exist to close.

Follower counts are not merely weak evidence — drainer operations artificially inflate them
([Blockaid](https://www.blockaid.io/blog/how-crypto-drainers-are-using-x-twitter-to-target-web3-users)),
making them **adversarially manipulated** evidence. They must not enter scoring.

---

## 6. The build-critical safety finding

Blockaid documents drainer crews that seed fake mint links into the **reply and repost graph of
legitimate verified accounts**, and register lookalike domains within hours of a real launch
([source](https://www.blockaid.io/blog/how-crypto-drainers-are-using-x-twitter-to-target-web3-users)).

An author-scoped rule that captures a real caller's post will also capture the phishing swarm
beneath it. Therefore: **extract links from the author's own post body only — never from replies,
quote-posts, or embedded cards.** Without this, false positives are dominated by phishing rather than
by bad calls, and the CTA gate becomes the only line of defense instead of the second one.

This is now a safety invariant in `PHASE_1_FROZEN_CONFIG.md` and is recorded in `ADR-012`.
