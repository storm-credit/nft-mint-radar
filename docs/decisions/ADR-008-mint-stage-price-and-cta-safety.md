# ADR-008 — Mint Stage, Asset-Aware Price, and CTA Safety

## Status
Accepted — 2026-08-22

## Context
The blind-spot audit found three coupled P0 defects in the original logical model:
1. `mint_price_native` cannot represent ERC-20-priced mints such as USDG-priced Robinhood Chain drops;
2. a single Opportunity cannot safely collapse multiple GTD/FCFS/community/public stages with different prices/times/limits;
3. an official social account can be compromised, so T1 identity alone cannot make a new mint link safe.

## Decision

### 1. Asset-aware amount
Use:

```yaml
AssetAmount:
  amount: decimal
  asset_kind: NATIVE|ERC20|OTHER
  chain_key: string
  token_address: string|null
  symbol: string|null
  decimals: integer|null
  usd_estimate: decimal|null
  usd_estimate_at: datetime_utc|null
```

Every stage also has:
`price_state: FREE|KNOWN|UNKNOWN|VARIABLE`.

FREE is an explicit sourced state, not an inferred numeric zero.

### 2. MintCampaign + MintStage
Introduce:

```yaml
MintCampaign:
  id: string
  project_id: string
  chain_key: string
  contract_address: string|null
  supply: integer|null
  source_campaign_id: string|null
  state: string

MintStage:
  id: string
  campaign_id: string
  label: string|null
  stage_type: ALLOWLIST|HOLDER|COMMUNITY|FCFS|RAFFLE|PUBLIC|TEAM|OTHER
  allocation_type: FCFS|RAFFLE|GUARANTEED|HOLDER|PUBLIC|UNKNOWN
  open_at: datetime_utc|null
  close_at: datetime_utc|null
  price_state: FREE|KNOWN|UNKNOWN|VARIABLE
  price: AssetAmount|null
  max_per_wallet: integer|null
  eligibility_ref: string|null
  official_action_url: VerifiedLink|null
  evidence_ids: [string]
```

`Opportunity` remains the action/prioritization object and references a specific campaign/stage where applicable.

### 3. Legacy/reactivation event support
Add normalized event types:
- `PROJECT_REACTIVATED`
- `CHAIN_MIGRATION_ANNOUNCED`
- `LEGACY_HOLDER_ACCESS_ANNOUNCED`

This supports the user's target pattern of old NFT projects reactivating and granting early-holder access to new collections/chains.

### 4. CTA safety is independent of source identity trust
Add a separate action-link safety state:

`UNVERIFIED|CONSISTENT|QUARANTINED|REVOKED`

T1 source identity does not automatically imply `CONSISTENT`.

Before `ACTION`, `URGENT`, `APPLY_WL`, or `MINT_RECHECK` includes a clickable wallet-impacting CTA, require current cross-source/marketplace/on-chain consistency. Unexpected host/contract changes become `QUARANTINED` and suppress the CTA.

## Consequences
- OpenSea stage mapping becomes lossless enough for GTD/FCFS/community/public structures.
- Scoring can compare actual asset-denominated costs without pretending all prices are native gas tokens.
- Telegram can display `Free`, `0.002 ETH`, `3.00 USDG`, or `Unknown` correctly.
- A compromised official account cannot bypass link safety simply because the account is T1.
- Existing Project/Evidence/Verification architecture is preserved; this is a targeted schema patch.

## Harness impact
Add fixtures for:
1. three-stage mint with different prices;
2. ERC-20-priced stage;
3. explicitly free stage;
4. official social account linking a new hostile domain while canonical website is unchanged;
5. official compromise/disavowal correction.

## Rejected alternatives
### Keep one Opportunity per whole drop
Rejected because stage-specific facts collide.

### Store all prices as USD
Rejected because USD conversion is time-dependent evidence, not the canonical payment asset.

### Trust any T1 link as safe
Rejected because official accounts can be compromised.

## Revalidation trigger
Revisit if a major launchpad introduces pricing or stage semantics that cannot be represented without source-specific branching in core domain objects.
