# Architecture

## Product direction
Implement Phase 1 first while preserving interfaces for Phase 2–4. The production hot path is **deterministic-first**; logical roles do not imply autonomous agents.

## Chosen architecture
ADR-001 chose Alpha Radar rather than a simple mint calendar. ADR-007/008/009 subsequently patch chain scope, mint-stage modeling, CTA safety, and orchestration.

```text
Source adapters
  official site / X / OpenSea / Galxe / on-chain
  optional PREMINT / Guild / Dune / Telegram source
  weak Reddit / community discovery
        |
        v
RawEvent normalization
        |
        v
Evidence Store + Project Identity
        |
        +----------------------+
        |                      |
        v                      v
Verification / CTA       MintCampaign
Safety Rules                 |
        |                  MintStage
        |                      |
        +----------+-----------+
                   v
              Opportunity
                   |
          Quality / Alpha /
          Effort / Risk
          deterministic score
                   |
                   v
             Decision Gates
                   |
          Dedup / Recheck /
       Transactional Outbox
                   |
                   v
               Telegram
```

Conditional model-driven nodes are limited to unstructured extraction, ambiguous entity resolution, Phase 2 quest parsing, and independent critique. See ADR-009 and `LOCAL_ACTION_SPACE_AUDIT.md`.

## Phase 1 chain scope
- Ethereum
- Base
- Robinhood Chain

EVM-first only. Non-EVM expansion requires a separate ADR.

## Core domain

### Project
Identity, aliases, chains, official relations, contracts and lifecycle.

### Source
Source type, trust tier, role, identity, auth profile and health.

### Evidence
Append-only support for claims. Can reference Project, Campaign, Stage or Opportunity.

### MintCampaign
One collection/drop campaign on a chain/contract.

### MintStage
Stage-specific GTD/allowlist/holder/community/FCFS/raffle/public terms including time, allocation, asset-aware price and max-per-wallet.

### Opportunity
The action/prioritization object. It can reference one Campaign/Stage; it does not duplicate all mint-stage facts.

### Quest — Phase 2
Required/optional eligibility actions. Social/Discord/wallet-impacting actions are manual only.

### UserProgress — Phase 2+
Explicit progress with provenance; recommendations never equal completion.

### WalletEntity / InfluencerEntity
Kept separate because on-chain behavior, public identity and social influence are different evidence regimes.

### Notification
Deduplicated action alert with campaign/stage context and current safety state.

## Trust and CTA model
`source identity trust != claim verification != CTA safety`.

A T1 official account can still be compromised. Wallet-impacting CTA is rendered only when current link/contract evidence produces `ActionLinkAssessment=CONSISTENT`.

## Scoring
Keep separate, explainable components:
- Quality 0–100 — higher better
- Alpha 0–100 — higher earlier/better
- Effort 0–100 — lower better
- Risk 0–100 — lower better
- Evidence confidence

Deterministic formula/hard gates own the numeric decision. No black-box buy score and no guaranteed-return output.

## Wallet intelligence
Dune/other analytics are optional adapters, never mandatory for core alerts.

Potential queries:
1. watched-wallet recent NFT interactions
2. early-minter history
3. first-N minter overlap
4. unique-wallet velocity
5. holder concentration
6. deployer/funder/factory graph
7. wash-like counterparty score

A cohort of independently successful early minters is stronger than one celebrity wallet. Factory/deployer relations are not creator provenance without corroboration.

## Operational boundaries
- no private keys / seed
- no wallet signing / approval / transaction execution
- no Discord self-bot
- no automated social engagement/referral farming
- no unverified or quarantined wallet-impacting CTA
- source failures degrade independently
- paid adapters have hard budgets

## Phase roadmap

### Phase 1 — Discovery + Verification + Scoring + Telegram
Deliverable: useful S/A candidate alerts with evidence, campaign/stage context and safe next action.

### Phase 2 — WL / Quest Intelligence
Deliverable: parse qualification tasks, deadline and effort; maintain explicit user checklist/progress.

### Phase 3 — Discord Intelligence
Deliverable: permitted server-opt-in announcement/role/progress intelligence; no user self-bot.

### Phase 4 — Personal Alpha Assistant
Deliverable: wallet eligibility + task state + watched-wallet cohorts + final mint re-evaluation + daily action summary.

## Authority
Detailed field semantics live in `DEEP_DESIGN.md` + Accepted ADRs. This file is architecture overview only and must not become a second schema authority.
