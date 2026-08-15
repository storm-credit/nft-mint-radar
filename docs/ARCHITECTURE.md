# Architecture

## Product direction
Implement Phase 1 first, but preserve interfaces for Phase 2–4.

## Four architecture options

### Option A — Simple Mint Radar
Collectors -> basic scoring -> Telegram

Pros:
- fastest implementation
- cheapest

Cons:
- weak allowlist support
- difficult to evolve without refactor

### Option B — Alpha Radar (chosen MVP)
Collectors -> event normalization -> evidence verification -> project/opportunity scoring -> decision engine -> Telegram

Pros:
- useful immediately
- preserves evidence and trust boundaries
- supports Phase 2 later

Cons:
- more structure than A

### Option C — Alpha + Quest
Option B + quest parser + effort scoring + user task tracker

Pros:
- directly optimizes WL acquisition

Cons:
- broader API/LLM/test surface
- premature for first integration pass

### Option D — Personal NFT Alpha Agent
Option C + Discord intelligence + watched wallets + personal eligibility + wallet/on-chain cohort engine + daily action planner

Pros:
- end-state product

Cons:
- over-scoped for initial implementation
- more credentials, permissions, failure modes and operating cost

## Decision
Use B as Phase 1 implementation target while modeling the domain so C/D can be added without reworking core entities.

## Logical pipeline

```text
Collectors
  X / websites / PREMINT / Galxe / Guild / marketplaces
  Dune / on-chain / watched wallets
  Reddit / Telegram / community (weak discovery)
        |
        v
Event Normalizer
        |
        v
Evidence Store + Source Trust
        |
        +-------------------+
        |                   |
        v                   v
Project Engine        Opportunity Engine
        |                   |
        v                   v
Quality/Alpha       WL/Mint State Machine
Risk Scores               |
        |                  +---- Phase 2: Quest Parser / Effort Score
        |                  +---- Phase 3: Discord Progress
        +---------+---------+
                  v
            Decision Engine
                  |
                  v
       Dedup / Urgency / Recheck
                  |
                  v
              Telegram
```

## Core entities

### Project
- id
- name
- chain(s)
- official links
- status
- quality_score
- alpha_score
- risk_score
- evidence confidence

### Source
- source_type
- trust_tier
- role(s)
- URL/identifier
- account/entity identity

### Evidence
- project_id/opportunity_id
- source
- captured_at
- claim key/value
- raw excerpt/reference hash if permitted
- confidence
- verification state

### Opportunity
Types:
- ALLOWLIST
- RAFFLE
- HOLDER_MINT
- FREE_MINT
- PAID_MINT
- PUBLIC_MINT
- AIRDROP
- OTHER

State examples:
- RUMORED
- DISCOVERED
- REGISTRATION_PENDING
- REGISTRATION_OPEN
- REGISTRATION_CLOSED
- RESULTS_PENDING
- WON
- WAITLISTED
- LOST
- MINT_SCHEDULED
- MINT_OPEN
- ENDED
- CANCELLED

### Quest (Phase 2)
Types:
- FOLLOW_X
- LIKE_X
- REPOST_X
- COMMENT_X
- TAG_FRIEND
- JOIN_DISCORD
- DISCORD_ROLE
- DISCORD_LEVEL
- GALXE
- GUILD
- PREMINT_REGISTER
- HOLD_NFT
- HOLD_TOKEN
- ONCHAIN_ACTION
- REFERRAL
- CUSTOM

Quest execution is never automated if it requires user-account impersonation, wallet signing, spam or prohibited automation.

### WalletEntity
Represents watched public wallets or cohorts.
Do not treat public identity labels as immutable truth; identity mappings require evidence and confidence.

### InfluencerEntity
Separate from WalletEntity because social influence and on-chain skill are not the same signal.

### UserProgress
Phase 2+ only:
- opportunity
- quest
- status
- verified_at
- source

### Notification
- fingerprint
- severity
- action
- reason
- sent_at
- last_material_change

## Scoring model outline
Keep component scores separate.

- Quality: 0–100, higher better
- Alpha: 0–100, higher earlier/more under-discovered
- Effort: 0–100, lower better
- Risk: 0–100, lower better
- Evidence confidence: LOW/MEDIUM/HIGH

Action score must be explainable. No black-box 'buy score'.

## Dune / wallet cohort architecture
Dune is an optional analytics adapter, not a runtime dependency for every alert.

Initial queries/specs:
1. `watched_wallet_recent_nft_interactions`
2. `early_minter_history_by_wallet`
3. `successful_collection_first_n_minter_overlap`
4. `collection_unique_wallet_velocity`
5. `holder_concentration`
6. `deployer_funder_graph`
7. `wash_like_counterparty_score`

Later proprietary signal:
`AlphaWalletScore = repeated early entry quality + independence + persistence - manipulation/sybil/wash/conflict penalties`

A cohort hit is stronger than one celebrity-wallet hit.

## Operational boundaries
- no private keys
- no wallet signing
- no transaction execution
- no self-bots
- no fake engagement
- no unaudited auto-follow/auto-repost behavior
- official URLs must be verified before notification CTA

## Phase roadmap

### Phase 1 — Discovery + Verification + Scoring + Telegram
Deliverable: useful S/A candidate alerts with evidence and next action.

### Phase 2 — WL / Quest Intelligence
Deliverable: parse qualification tasks, deadline and effort; maintain user checklist.

### Phase 3 — Discord Intelligence
Deliverable: permitted read-only announcement/role/progress intelligence; no user self-bot.

### Phase 4 — Personal Alpha Agent
Deliverable: wallet eligibility + task state + watched-wallet cohorts + final mint re-evaluation + daily action summary.
