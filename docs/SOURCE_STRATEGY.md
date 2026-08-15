# Source Strategy

## Goal
Find high-quality NFT allowlist/mint opportunities early, then verify them before asking the user to spend time, money, or sign anything.

## Core principle: discovery != verification
A source can be excellent for finding alpha and poor for proving eligibility details. Every signal is tagged with both a trust tier and a role.

Roles:
- `DISCOVERY`: helps find something early.
- `VERIFICATION`: can corroborate project-controlled facts.
- `ONCHAIN`: objective public-chain evidence.
- `SENTIMENT`: measures community attention, not truth.
- `BEHAVIOR`: wallet/entity actions that may predict interest.

## Source matrix

### T0 — On-chain / objective evidence
Priority: highest for contract/wallet facts.

Sources:
- Ethereum/EVM block explorers such as Etherscan and chain-native explorers
- Solana explorers where relevant
- directly indexed RPC/log data
- Dune queries built from decoded/raw chain data

Uses:
- contract deployment detection
- deployer/treasury movement
- mint start/transactions
- supply and holder concentration
- early-wallet cohorts
- smart-money/watched-wallet interactions
- wash-trading/manipulation heuristics

Important: on-chain activity proves that an action occurred; it does not prove an unofficial mint site is safe.

### T1 — Official project channels
Sources:
- official website/docs/blog
- official X account
- official Discord announcement channels
- official Telegram announcement channel
- official GitHub when relevant

Uses:
- mint/WL dates
- holder eligibility
- snapshots
- official contract links
- quest instructions
- changes/cancellations

### T2 — Structured campaign/marketplace sources
Sources:
- PREMINT
- Galxe
- Guild
- OpenSea mint/drop pages
- Magic Eden launch/drop pages
- other chain-native launchpads after source-specific validation

Uses:
- registration windows
- raffle/allowlist mechanics
- task requirements
- mint price/supply
- campaign progress/status

### T3 — Alpha/analytics entities
Sources:
- Dune community dashboards and analysts
- public smart-money/collector wallets
- established NFT analysts and collectors on X
- Arkham/Nansen-style labels if later integrated
- specialized NFT analytics dashboards

Uses:
- project discovery
- wallet cohort behavior
- unusual accumulation/minting
- early-wallet overlap between successful launches
- mindshare shifts

Rule: T3 never supplies an actionable mint URL without T0/T1/T2 corroboration.

### T4 — Community chatter
Sources:
- Reddit
- public Telegram alpha groups
- generic Discord communities
- generic X accounts/threads
- Farcaster/community feeds where useful

Uses:
- weak early discovery
- sentiment change
- rumor clustering

Rule: community chatter is a lead, not evidence.

## Platform priority

### X — P0
Why:
- project announcements and giveaway/WL tasks often appear here first
- supports discovery of Follow/Like/Repost/Comment/Tag tasks

Watch keywords:
`allowlist`, `whitelist`, `WL`, `mintlist`, `raffle`, `giveaway`, `premint`, `early access`, `holders`, `snapshot`, `free mint`, `mint`, `repost`, `retweet`, `tag`, `discord`, `role`, `OG`, `FCFS`, `FCFS`, `guaranteed`

### Official websites/docs — P0
Why:
- final source for official links, mechanics and contract pointers

### PREMINT/Galxe/Guild — P0
Why:
- structured allowlist and quest information; essential for Phase 2.

### On-chain + Dune — P0/P1
Dune is not a social discovery feed. It is a query/analytics layer for confirming and discovering behavior patterns.

Dune use cases:
1. Watched-wallet mint detection.
2. First-N-minter cohort extraction.
3. Overlap: wallets that minted multiple historically successful collections early.
4. Fresh-wallet activity around a new contract.
5. Holder concentration and post-mint distribution.
6. Collection buyer/seller growth and unique-wallet velocity.
7. Deployer/funder relationships.
8. Wallet co-occurrence graph between projects.
9. Detect repeated counterparties/wash-like patterns.
10. Build a proprietary `Alpha Wallet Score` from repeat early-entry performance rather than blindly following celebrity wallets.

Dune integration plan:
- Phase 1: consume selected public query results/manual query IDs only if API access is available; otherwise define SQL/query specs and keep integration optional.
- Phase 2: parameterized watched-wallet / project queries.
- Phase 3+: scheduled cohort refresh and proprietary smart-wallet scoring.

### Discord — P1 for discovery, P0 for WL execution intelligence
Phase 1: official links and public/manual announcement references.
Phase 2: parse disclosed Discord requirements.
Phase 3: permitted bot/API read access for announcement/role/progress data.

Never use a user self-bot or automated engagement.

### Telegram — P1 source + P0 notification destination
Source side:
- official announcement channels: T1
- public alpha groups: T4

Destination side:
- primary user alert channel
- only action-worthy changes should notify

### Reddit — P2
Useful for:
- finding emerging chatter before broad X visibility
- post-launch reputation/scam complaints
- community qualitative checks

Not useful enough for primary alerting by itself. Treat as T4 and corroborate.

### Farcaster / niche communities — P2
Optional source for native onchain/social communities; add only if measurable incremental signal exists.

## Wallet intelligence strategy
Do not maintain a simplistic `famous_whales.txt` and copy trades.

Maintain `WalletEntity` with:
- public address / ENS / chain
- identity verification source
- category: collector, trader, artist, fund, deployer, influencer, unknown
- active_since / last_seen
- collections interacted with
- early_mint_count
- successful_early_mint_count
- median entry percentile
- median hold duration
- realized/unrealized behavior where measurable
- wash/sybil suspicion
- promotion conflict flags
- wallet confidence
- `alpha_wallet_score`

Signals:
- `single_wallet_hit`: watched wallet interacts with project
- `cohort_hit`: 3+ independent high-scoring wallets interact
- `cross-source_hit`: wallet cohort + official announcement/quest signal

A single famous wallet is weak evidence. A cohort of independently successful early minters is stronger.

## Influencer intelligence strategy
Maintain `InfluencerEntity` separately from wallets.

Fields:
- handle/name
- category: analyst, collector, artist, founder, trader, security researcher
- source reliability score
- promotion/shill risk
- wallet-linked confidence when publicly verified
- topic specialization
- historical lead time
- false-positive rate
- last_active

Influencer posts may raise discovery priority but cannot raise safety/verification confidence by themselves.

### Initial seed candidates — handles only, verify before activation
These are research candidates, not endorsements and not an investment recommendation:
- `punk9059` — data-oriented NFT market analysis
- `punk6529` — collector/strategic NFT perspective
- `pranksy` — long-running NFT collector
- `cozomomedici` — digital-art/NFT collector signal
- `zachxbt` — due-diligence/security risk signal, not a mint alpha signal

Before adding any wallet address, require a public first-party or strongly corroborated identity mapping and store the verification evidence.

## Important missing sources / blind spots
- marketplaces can change APIs and mint surfaces
- X API cost/rate limits can dominate Phase 1 architecture
- Discord content may be inaccessible without server-approved bot permissions
- Telegram public groups are noisy and phishing-heavy
- wallet labels can become stale or be split across multiple wallets
- public figures can use private/stealth wallets
- bot engagement can create fake X traction
- wash trading can create fake NFT volume
- historical wallet success can disappear when strategy/regime changes
- newly deployed contracts can be legitimate but still lack verified official linkage

## Alert policy
Send Telegram only when one of these occurs:
- S/A discovery with credible evidence
- allowlist/quest opens or materially changes
- deadline/action urgency changes
- watched cohort interacts with a candidate and confidence crosses threshold
- contract is officially linked/deployed
- risk grade materially worsens
- WL result/mint window changes

Do not send routine 'nothing found' spam.
