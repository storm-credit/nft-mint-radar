# Blind-Spot Sweep — 2026-08-22

> **Historical record of the 2026-08-22 sweep. Not current state.**
> The findings below were closed by ADR-007/ADR-008 and later work.
> `docs/PROJECT_STATUS.md` is the authority for current gate state.

## Scope
Targeted re-audit after the Production Coding Start Gate was introduced. This audit does not reopen already-frozen design areas unless new evidence exposes a P0 defect.

## Verdict
**4 new P0 design defects found and patchable without architecture reset.**

The overall architecture remains KEEP. Required action is PATCH, not NEW DESIGN.

## P0-1 — Phase 1 chain scope misses Robinhood Chain

### Finding
The canonical Deep Design currently fixes Phase 1 to Ethereum + Base. This no longer matches the user's primary alpha use case: legacy NFT projects such as The Saudis are moving toward Robinhood Chain, and OpenSea is already showing active Robinhood Chain NFT mints with allowlist/public stages.

### Why P0
A radar can be technically correct yet miss the exact class of opportunity the user wants.

### Patch
Phase 1 target set becomes:
- Ethereum
- Base
- Robinhood Chain

All three remain EVM-family targets, so this does not require a non-EVM domain redesign.

Chain identity must not be a free-form display string only. Persist a normalized chain key plus EIP-155 chain id when known.

### Verification impact
`SPIKE-MARKET-001` must sample Robinhood Chain alongside Ethereum/Base before the Phase 1 coding gate closes.

---

## P0-2 — Official social account != safe CTA

### Finding
The trust model treats official X/Discord/Telegram/web channels as T1. Identity can be official while the account/session is compromised. A malicious mint link can therefore originate from a legitimately named channel.

### Why P0
A false-positive CTA can cause irreversible wallet loss.

### Patch
Separate:
1. `source_identity_trust` — is this the real project-controlled identity?
2. `action_link_safety` — is this specific URL/contract consistent with current multi-source/on-chain evidence?

For any wallet-impacting CTA, T1 identity alone is insufficient.

Require at least one of:
- current official website + official social cross-link consistency;
- official marketplace/launchpad identity + project linkage;
- previously verified canonical domain with no unexpected host change + current project corroboration;
- officially linked contract plus T0 existence/provenance check.

Unexpected domain/contract changes trigger `CTA_QUARANTINED` and WARNING, even if the announcement came from T1.

### New harness fixtures
- compromised official social posts a new mint domain;
- official social and official website disagree on mint host;
- official account restores/disavows compromised announcement.

---

## P0-3 — Native-only mint price model is insufficient

### Finding
Canonical Opportunity currently stores `mint_price_native`. Active Robinhood Chain NFT drops on OpenSea can be priced in non-native assets such as USDG.

### Why P0
Incorrect price semantics affect scoring, user cost, alert rendering and comparisons.

### Patch
Replace the conceptual single native price with an asset-aware amount:

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

Mint stage pricing uses `AssetAmount|null`; `null` may mean FREE or UNKNOWN only when paired with explicit price state.

Add:
`price_state: FREE|KNOWN|UNKNOWN|VARIABLE`

Never encode FREE as an assumed numeric zero without source evidence.

---

## P0-4 — Opportunity needs explicit multi-stage mint model

### Finding
Real drops can contain multiple simultaneous/sequential stages: treasury, GTD allowlist, FCFS allowlist, community allowlist, holder access and public mint, each with different time, price, wallet limit and eligibility.

### Why P0
Collapsing a whole drop into one Opportunity can overwrite stage-specific facts and produce wrong next-action alerts.

### Patch
Introduce `MintCampaign` + `MintStage` semantics.

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

`Opportunity` remains the user-action opportunity layer and can reference one campaign/stage. A single project may therefore produce multiple concurrent Opportunities without data collision.

### Additional user-intent event types
Add normalization support for:
- `PROJECT_REACTIVATED`
- `CHAIN_MIGRATION_ANNOUNCED`
- `LEGACY_HOLDER_ACCESS_ANNOUNCED`

These are important for old-collection revival alpha such as legacy-holder access to a new-chain mint.

---

## P1-1 — OpenSea drop calendar is not coverage-complete alpha discovery

### Finding
OpenSea documents the Drops page as curated/live-upcoming and states that creating a self-serve drop does not guarantee calendar placement. Therefore OpenSea is excellent structured mint-stage evidence but cannot be assumed to discover every early opportunity.

### Patch
Keep OpenSea P0 for structured marketplace/drop data, but classify it as:
- strong structured discovery for listed drops;
- strong stage/price/schedule evidence;
- **not a completeness source**.

Coverage must be measured against X/official-site/campaign/on-chain discoveries in `SPIKE-MARKET-001`.

---

## P1-2 — Factory deployers can create false wallet/deployer attribution

Common NFT factories/launchpads may deploy many unrelated collections. A raw deployer address can therefore represent a platform factory rather than the creator.

Patch for wallet/on-chain intelligence:
- distinguish `factory`, `creator`, `admin/owner`, `funder` and `deployer` roles;
- do not award/penalize project provenance from a shared factory address alone;
- resolve emitted creator/owner/configuration evidence when available.

---

## P1-3 — Alpha scoring has survivorship/look-ahead bias risk

The future Dune/AlphaWallet benchmark can accidentally label wallets as smart because benchmark collections were selected after they became successful.

Phase 1.5 requirement:
- time-sliced benchmark windows;
- frozen success definition before scoring wallets;
- out-of-sample evaluation;
- report precision/recall/lead-time, not just profitable anecdotes.

No Phase 1 block because Dune remains optional Phase 1.5.

---

## P1-4 — Manual task completion must be first-class

X repost/comment, CAPTCHA, Discord activity and some wallet-gated checks cannot always be programmatically verified. `UserProgress` must allow `USER_CONFIRMED` separate from `PROVIDER_VERIFIED` and must never fabricate completion.

Phase 2 patch target:
`verification_mode = USER_CONFIRMED|PROVIDER_VERIFIED|ONCHAIN_VERIFIED|UNKNOWN`.

---

## P2 observations
- Consider a fallback notification destination only after Telegram reliability is measured; do not add channels speculatively.
- Wallet addresses used for personal eligibility should be redacted from routine logs and user-configurable for deletion.
- Add schema-version drift quarantine for provider payload changes.
- Track source lead-time distribution by chain, not only globally.

## Red Team decision
- Architecture: **KEEP**
- Domain model: **PATCH**
- Chain scope: **PATCH**
- CTA safety: **PATCH**
- OpenSea role: **PATCH**
- Dune Phase 1.5 evaluation design: **PATCH LATER**

## Gate impact
Deep Design is temporarily `PATCH_RECONCILIATION_REQUIRED` until ADR-007/ADR-008 and status/gate documents incorporate the four P0 findings. Production coding remains blocked. Technical spikes remain allowed.
