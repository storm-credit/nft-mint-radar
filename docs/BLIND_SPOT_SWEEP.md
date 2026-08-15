# Blind-Spot Sweep

## 1. Discovery coverage gaps
A radar limited to X + OpenSea will miss:
- PREMINT/Galxe/Guild qualification campaigns
- Discord-only role/level requirements
- Telegram-only official announcements
- on-chain contract deployments before social announcements
- wallet-cohort accumulation/mint behavior
- Reddit/community rumors that can be useful as weak leads
- chain-specific launchpads and marketplaces

Recommendation: broad discovery, narrow verification.

## 2. Dune is valuable but has a different job
Dune should be included as an on-chain analytics adapter, not treated like X.

Strong Dune jobs:
- identify repeat early minters
- rank wallets by historic entry percentile into later-successful NFT collections
- detect wallet overlap across collections
- monitor unique-wallet growth and concentration
- detect fresh-wallet clusters
- create cohort alerts when several independent high-score wallets interact
- investigate deployer/funder links and suspicious counterparty loops

Weak Dune jobs:
- proving an allowlist URL is official
- parsing Discord social requirements
- real-time social announcements

Operational caveat: Dune query/API compute can consume credits. Prefer cached/latest results and targeted queries before high-frequency query execution.

## 3. Famous wallet trap
Do not equate fame with predictive alpha.
Risks:
- public wallet may be only one of many wallets
- purchases may be art collecting, not a trade signal
- sponsored/promotional conflict
- celebrity wallet entry can be late
- wallet can transfer assets between own addresses
- historical performance can regress

Better approach: build a proprietary wallet cohort score and treat named collectors as only one seed set.

## 4. Influencer trap
Follower/engagement counts can be manipulated. Promotions and giveaways may be paid or botted.

Required controls:
- separate analyst/security/collector/founder/trader categories
- promotion conflict flags
- historical false-positive rate
- lead time vs official announcement
- corroboration before action

## 5. Discord automation trap
Required WL work may include joining, levels, roles, activity and moderator selection.

Safe automation:
- parse requirements
- read permitted announcement channels
- read role/progress data through server-approved APIs/bots when available
- remind the user

Unsafe/out-of-scope:
- user self-bot
- automated `gm`/spam activity
- fake conversations
- automatic invite/referral farming

## 6. X automation trap
The system may discover Repost/Like/Follow/Comment/Tag tasks, but should not blindly execute social actions.
Reasons:
- account risk/rate limits/ToS
- accidental shilling/scam propagation
- friend-tag spam
- campaigns can change/delete instructions

Phase 2 default: extract + checklist + deep link; user performs action.

## 7. Telegram trap
Telegram is both a useful official source and the highest-risk phishing/noise source when using public alpha groups.

Controls:
- official channel identity evidence
- never trust forwarded mint links by default
- rewrite links from verified project source when possible
- public alpha groups = discovery only

## 8. Reddit role
Include Reddit, but low priority.
Useful for:
- weak early leads
- reputation complaints
- scam reports
- qualitative community reaction

Do not page the user from a Reddit-only signal.

## 9. Wallet/on-chain tools we should consider
### Dune
Best for custom NFT cohort analytics and reproducible SQL.

### Nansen (optional/paid)
Useful for wallet labels, Smart Money cohorts, profiler/related wallets and activity. Treat Nansen labels as useful context, not unquestionable truth.

### Arkham (optional)
Useful for entity/address transaction alerts and can itself deliver alerts via Telegram/webhook. This can reduce custom monitoring work for specific wallets.

Decision: keep adapters optional. Phase 1 must work without paid Nansen/Arkham dependencies.

## 10. Marketplace blind spots
NFT activity spans multiple chains and marketplaces. OpenSea alone is insufficient.
Future adapters should be chosen based on actual target-chain activity rather than implemented speculatively.

Candidate categories:
- OpenSea
- Magic Eden
- Blur where relevant
- Solana-native markets/launchpads where relevant
- chain-native marketplaces for emerging ecosystems

## 11. Time-to-alpha metric
A candidate quality score without timing is insufficient.
Track:
- first discovery timestamp
- first official confirmation
- first WL task publication
- first watched-wallet cohort hit
- first contract deployment
- public visibility proxy

Use these to measure whether each source actually gives lead time.

## 12. Source ROI metric
Every source costs engineering/runtime attention.
Track per source:
- actionable leads found
- unique leads not found elsewhere
- median lead time
- false-positive rate
- operational cost
- API cost

Remove low-value integrations instead of collecting everything forever.

## 13. Security and financial decision boundary
The radar provides evidence, prioritization and action prompts. It does not guarantee profit and does not automatically transact.

Before any mint CTA becomes `READY`, require:
- official linkage verification
- current contract/address recheck when available
- mint terms recheck
- material risk-change recheck

## 14. Phase recommendation
Architecture should anticipate Phase 4, but implementation order remains:
1. Phase 1 — Discovery/verification/scoring/Telegram.
2. Phase 2 — WL/quest extraction and effort tracking.
3. Phase 3 — permitted Discord intelligence.
4. Phase 4 — personalized wallet/quest/alpha orchestration.

Wallet cohort/Dune analytics can begin as a narrow Phase 1.5 experiment because they strengthen discovery without requiring personal-account automation.
