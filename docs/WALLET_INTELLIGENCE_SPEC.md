# Wallet / Dune Intelligence Specification

## Objective
Use public on-chain behavior to discover projects earlier and prioritize investigation. Wallet intelligence is not copy-trading and never proves project legitimacy.

## 1. Wallet categories
- `SEED_PUBLIC`: publicly attributed collector/analyst wallet used to bootstrap research.
- `DISCOVERED_ALPHA`: unnamed wallet discovered through historical behavior.
- `DEPLOYER_TEAM`: project/deployer/treasury related; excluded from independent alpha cohorts.
- `UNKNOWN`: insufficient history.

## 2. Identity policy
A named identity mapping needs:
- first-party published address/ENS; or
- two strong independent corroborations including one stable public profile/chain identity relation.

Identity confidence expires/rechecks when:
- ENS/address ownership changes;
- public profile removes mapping;
- contradictory evidence appears.

Never infer identity from display name alone.

## 3. Historical launch cohort
AlphaWalletScore is calibrated only against collections that have:
- known mint/deployment timing;
- sufficient on-chain minter history;
- non-trivial public trading/activity history;
- obvious scam/drainer collections excluded from positive benchmark but retained as negative samples.

### Successful-collection benchmark v1
Avoid defining success only as floor price or hindsight profit.
For each launch cohort (same chain and rolling era), calculate normalized metrics:
1. 7-day unique holder retention percentile;
2. 7-day unique secondary buyer/activity percentile;
3. 7-day secondary volume normalized by supply percentile;
4. 30-day surviving active-holder/activity percentile where data exists.

A collection is `BENCHMARK_POSITIVE` if it ranks in the top quartile composite and is not disqualified by severe wash/manipulation evidence.
A collection is `BENCHMARK_NEGATIVE` if it has sufficient data but ranks in the bottom quartile or collapses into clear inorganic/manipulated activity.
Middle 50% remains neutral for scoring calibration.

This benchmark labels historical network/activity quality, not guaranteed investment return.

## 4. Early-entry percentile
For each wallet/collection:
```text
entry_percentile = 100 * (wallet_first_mint_or_buy_rank - 1) / max(unique_early_participants - 1, 1)
```
Lower is earlier.
Store separately:
- mint_entry_percentile
- secondary_buy_entry_percentile

Do not conflate minting with buying later.

Candidate early buckets:
- EARLY_1: <=1%
- EARLY_5: <=5%
- EARLY_10: <=10%
- NORMAL: >10%

Exact calibration may change after Dune backtest.

## 5. Independence graph
Wallets are linked for cohort-independence analysis by edges such as:
- direct transfers;
- common funder within configured hop/time window;
- repeated shared counterparties;
- same project treasury/deployer relationship;
- synchronized transaction pattern.

### Independence rule v1
A cohort counts only one vote per connected component when strong correlation evidence exists.
`independent_wallet_count = count(correlation_components)` rather than raw wallet count.

Strong correlation indicators:
- same fresh-wallet funder within 7 days;
- repeated direct ETH/token transfers among candidate wallets;
- team/deployer funding relation;
- circular NFT transfers.

Weak indicators alone do not collapse wallets.

## 6. Wash/sybil risk features
- common fresh funder
- circular transfers
- repeated reciprocal NFT trading
- highly synchronized entries/exits
- no independent funding/history
- same counterparty concentration
- creator/team funding

Output `wash_sybil_risk` 0–100 with evidence, never a hidden binary label.

## 7. AlphaWalletScore v1
Provisional formula:
```text
early_quality       = average quality of early entries into BENCHMARK_POSITIVE launches
negative_avoidance  = inverse rate of early entries into BENCHMARK_NEGATIVE launches
diversity           = entropy / independent project diversity
persistence         = holding/activity persistence proxy
recency             = exponential recency weighting

raw = 0.35*early_quality
    + 0.15*negative_avoidance
    + 0.20*diversity
    + 0.15*persistence
    + 0.15*recency

AlphaWalletScore = raw - wash_sybil_penalty - team_conflict_penalty
```

Minimum sample policy:
- fewer than 5 qualifying historical launches -> score confidence LOW;
- 5–14 -> MEDIUM maximum;
- >=15 with adequate era diversity -> eligible for HIGH confidence.

## 8. Cohort signal
A candidate project can emit:
- WEAK: 1 validated alpha wallet
- MEDIUM: 2 independent validated wallets
- STRONG: >=3 independent wallets with aggregate score threshold and no strong correlation warning

Cohort signal only affects Alpha; official verification remains separate.

## 9. Dune query specifications

### Q1 `wallet_recent_nft_interactions`
Inputs:
- wallet list
- chain
- since timestamp

Outputs:
- wallet
- contract
- token/event type
- tx hash
- block time
- counterparty
- value where available

### Q2 `collection_first_participants`
Inputs:
- contract
- participant window or first N

Outputs:
- wallet
- first mint time/rank
- first secondary buy time/rank
- quantity

### Q3 `wallet_historical_early_entries`
Inputs:
- wallet list
- benchmark collection list

Outputs:
- wallet
- collection
- mint percentile
- buy percentile
- benchmark label

### Q4 `wallet_correlation_edges`
Inputs:
- candidate wallet list
- lookback window

Outputs:
- wallet_a
- wallet_b
- edge_type
- evidence txs
- strength

### Q5 `project_holder_concentration`
Outputs:
- unique holders
- top1/top5/top10 concentration
- creator/team-linked concentration where known

### Q6 `project_unique_wallet_velocity`
Outputs by time bucket:
- unique minters
- unique buyers
- unique holders
- new wallets
- repeat wallets

### Q7 `deployer_funder_graph`
Outputs:
- contract deployer
- deployer funding source(s)
- related contracts
- suspicious/known entity labels only with provenance

## 10. Refresh policy before spike
Design target, not final runtime commitment:
- cached latest results may be read every 10–15 minutes for small filtered result sets;
- fresh watched-wallet query execution target <=60 minutes;
- historical AlphaWalletScore benchmark refresh daily/weekly, not per alert;
- expensive correlation/deployer queries run on-demand for high-priority candidates.

`SPIKE-DUNE-001` may alter these cadences without changing schemas.

## 11. Seed candidates
Publicly known collectors/analysts may enter research configuration only after address mapping evidence is captured. Names mentioned during planning (e.g. Pranksy, punk6529, dingaling) are candidate seeds, not hard-coded endorsements.

The system should outperform a static famous-wallet list by discovering unnamed wallets with repeat validated early behavior.

## 12. Failure modes
- historical regime change -> recency weighting + score decay
- wallet rotates addresses -> identity graph may fragment; do not guess merge
- creator gifts NFT to whale -> distinguish transfer/airdrop from voluntary mint/buy
- sponsored wallet interaction -> promotion conflict flag
- late famous-wallet entry -> no early-entry credit
- thin collections -> insufficient-sample confidence

## 13. Alert integration
Wallet signal can trigger a Telegram alert only when:
- project candidate already exists or cohort strength is STRONG enough to create an internal investigation candidate; and
- user-facing alert has clear statement that official project linkage may still be unverified.

Never send a raw contract interaction as a mint CTA.
