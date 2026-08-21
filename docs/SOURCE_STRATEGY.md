# Source Strategy

## Goal
Find high-quality NFT allowlist/mint opportunities early, then verify them before asking the user to spend time, money, connect a wallet, or sign anything.

## Core principle: discovery != verification != CTA safety
A source can be excellent for finding alpha and still be insufficient for proving eligibility or safe wallet interaction.

Every signal is tagged with roles:
- `DISCOVERY`: helps find something early.
- `VERIFICATION`: corroborates project-controlled facts.
- `ONCHAIN`: objective public-chain evidence.
- `SENTIMENT`: measures community attention, not truth.
- `BEHAVIOR`: wallet/entity actions that may predict interest.

In addition, wallet-impacting links have a separate CTA-safety state. Even a real official social account can be compromised.

## Phase 1 chain target
EVM-first target set:
- Ethereum
- Base
- Robinhood Chain

Do not infer completeness beyond these chains in Phase 1. Non-EVM chains require separate adapter/ADR work.

## Source matrix

### T0 — On-chain / objective evidence
Priority: highest for contract/wallet facts.

Sources:
- EVM block explorers and chain-native explorers
- directly indexed RPC/log data
- Dune queries built from decoded/raw chain data

Uses:
- contract deployment detection
- factory/creator/admin/funder relationships
- mint start/transactions
- supply and holder concentration
- early-wallet cohorts
- smart-money/watched-wallet interactions
- wash-trading/manipulation heuristics

Important: on-chain activity proves an action occurred; it does not prove a mint site or social announcement is safe.

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
- project-declared contracts/links
- quest instructions
- changes/cancellations

Critical rule: T1 identity means `official identity`, not `safe CTA`. A newly introduced host/contract still passes independent CTA/link consistency checks.

### T2 — Structured campaign/marketplace sources
Sources:
- PREMINT
- Galxe
- Guild
- OpenSea mint/drop pages and APIs
- Magic Eden launch/drop pages when later justified
- other chain-native launchpads after source-specific validation

Uses:
- registration windows
- raffle/allowlist mechanics
- stage-specific tasks
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

Rule: T3 never supplies an actionable mint URL without T0/T1/T2 corroboration and CTA-safety checks.

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

### X — P0 discovery / P0 official-change source when access is viable
Why:
- project announcements and giveaway/WL tasks often appear here early
- useful for legacy-project reactivation, migration, holder-benefit and quest signals
- supports discovery of Follow/Like/Repost/Comment/Tag requirements

Watch keywords/classes:
- `allowlist`, `whitelist`, `WL`, `mintlist`, `raffle`, `giveaway`, `premint`
- `early access`, `holders`, `snapshot`, `free mint`, `mint`
- `repost`, `retweet`, `tag`, `discord`, `role`, `OG`, `FCFS`, `guaranteed`
- `migration`, `new chain`, `holders first`, `legacy`, `early wallets`, `claim`

Safety rule: an X post linking a new mint host is not automatically a safe CTA merely because the account is official.

### Official websites/docs — P0 verification
Why:
- primary cross-check for canonical links, mechanics and contract pointers
- useful for detecting when social announcements introduce an unexpected domain or contract

### OpenSea — P0 structured drop/stage source, not completeness authority
Why:
- provides strong structured mint-stage evidence: allowlist/public stages, times, prices, limits and supply
- supports active NFT ecosystems including Robinhood Chain

Limit:
- the Drops calendar is curated/filtered and self-serve drops are not guaranteed calendar placement
- absence from OpenSea Drops does **not** mean an opportunity does not exist

Use:
- structured discovery for listed drops
- stage/price/schedule verification
- eligibility/mint-state evidence when available
- coverage comparison against X/official-site/campaign/on-chain discoveries

### PREMINT/Galxe/Guild — P0/P1 campaign intelligence
Why:
- structured allowlist and quest information is essential for Phase 2

Current adapter posture:
- Galxe: supported structured path, optional/degradable
- PREMINT: partner API when approved, otherwise official-registration-reference/manual path
- Guild: supported/public-reference path only after operational validation

### On-chain + Dune — P0/P1
On-chain evidence is core verification/behavior infrastructure. Dune is an analytics layer, not a social feed.

Dune use cases:
1. Watched-wallet mint detection.
2. First-N-minter cohort extraction.
3. Overlap of wallets that entered multiple historically successful collections early.
4. Fresh-wallet activity around a new contract.
5. Holder concentration and post-mint distribution.
6. Collection buyer/seller growth and unique-wallet velocity.
7. Deployer/funder/factory/creator relationships.
8. Wallet co-occurrence graph between projects.
9. Repeated counterparty/wash-like patterns.
10. Proprietary `Alpha Wallet Score` from repeat early-entry performance rather than celebrity copying.

Dune integration plan:
- Phase 1: optional selected cached/public result use only if access is available
- Phase 1.5: parameterized watched-wallet/cohort queries and out-of-sample benchmark evaluation
- later: scheduled cohort refresh if source ROI justifies cost

Bias rule: future AlphaWallet validation must prevent survivorship/look-ahead bias by freezing benchmark windows/definitions before evaluation.

### Discord — P1 discovery, Phase 2 requirement source, Phase 3 permitted read integration
Phase 1: official links/manual announcement evidence where available.
Phase 2: parse disclosed Discord role/level/activity requirements.
Phase 3: permitted bot/API read access for announcement/role/progress data.

Never use a user self-bot or automated engagement.

### Telegram — P1 source + P0 notification destination
Source side:
- official announcement channels: T1 identity source
- public alpha groups: T4 discovery only

Destination side:
- primary action alert channel
- only material/action-worthy changes notify

### Reddit — P2
Useful for:
- emerging chatter before broad visibility
- reputation/scam complaints
- qualitative community reaction

Never page the user from a Reddit-only signal.

### Farcaster / niche communities — P2
Optional; add only if measured incremental lead-time/unique-signal ROI is positive.

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

On-chain relationship roles must distinguish where possible:
- factory
- deployer
- creator
- admin/owner
- funder
- collector/trader

A shared launchpad factory is not creator provenance by itself.

Signals:
- `single_wallet_hit`: watched wallet interacts with project
- `cohort_hit`: 3+ independent high-scoring wallets interact
- `cross_source_hit`: wallet cohort + official announcement/quest signal

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
Research candidates, not endorsements:
- `punk9059` — data-oriented NFT market analysis
- `punk6529` — collector/strategic NFT perspective
- `pranksy` — long-running NFT collector
- `cozomomedici` — digital-art/NFT collector signal
- `zachxbt` — due-diligence/security risk signal, not mint alpha

Before adding any wallet address, require first-party or strongly corroborated identity mapping and evidence.

## Legacy-project revival intelligence
The radar must explicitly detect the pattern:
`dormant/legacy project -> renewed official activity -> chain migration/new collection -> early/legacy-holder access -> registration/WL -> mint`.

Relevant normalized events include:
- `PROJECT_REACTIVATED`
- `CHAIN_MIGRATION_ANNOUNCED`
- `LEGACY_HOLDER_ACCESS_ANNOUNCED`

This is a first-class discovery strategy, not a special-case hack.

## Important missing sources / blind spots
- marketplace APIs/calendars may omit valid projects
- X API cost/rate limits can dominate Phase 1 architecture
- official social accounts can be compromised
- Discord content may be inaccessible without server-approved bot permissions
- Telegram public groups are noisy and phishing-heavy
- wallet labels can become stale or span multiple wallets
- public figures can use private/stealth wallets
- bot engagement can create fake X traction
- wash trading can create fake NFT volume
- historical wallet success can regress
- shared factory deployers can create false provenance links
- newly deployed contracts can be legitimate but still lack verified official linkage
- provider schemas can drift and must fail closed/quarantine parse errors

## Alert policy
Send Telegram only when one of these occurs:
- S/A discovery with credible evidence
- legacy project reactivation/migration crosses watch threshold
- allowlist/quest opens or materially changes
- deadline/action urgency changes
- watched cohort interacts with a candidate and confidence crosses threshold
- contract becomes officially and safely linked
- risk grade materially worsens
- WL result/mint window changes

A wallet-impacting CTA is included only when `action_link_safety=CONSISTENT` under current evidence.

Do not send routine 'nothing found' spam.
