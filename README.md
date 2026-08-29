# NFT Mint Radar

> **Early NFT opportunity intelligence for mint / allowlist / holder access — without auto-signing, auto-minting, or fake social activity.**

`nft-mint-radar` is a design-first personal NFT alpha assistant intended to answer one practical question:

> **What is worth looking at early, what do I need to do to qualify, and when should I act?**

The project is currently in **pre-production validation**. The architecture, trust model, harness and evaluation contracts are designed, but production collectors are intentionally blocked until the remaining provider spikes pass.

## What it is meant to detect

- upcoming NFT mints
- allowlist / whitelist registrations
- raffles / GTD / FCFS / public stages
- holder-only and legacy-holder access
- free or paid mint stages
- X social requirements: follow / like / repost / comment / tag
- Discord join / role / level requirements
- Galxe / PREMINT / Guild-style qualification flows
- project reactivation after dormancy
- chain migration / new collection launches
- smart-wallet / early-minter cohort signals
- suspicious or conflicting mint links
- deadline, price, contract and eligibility changes

## Target experience

```text
Discovery
   ↓
Evidence / identity verification
   ↓
Project + MintCampaign + MintStage normalization
   ↓
Quality / Alpha / Effort / Risk
   ↓
Allowlist / quest requirements
   ↓
Decision + urgency
   ↓
Telegram action alert
```

Example target alert:

```text
🔥 A — Allowlist action
Project ABC

마감: 8/30 21:00 KST
현재: GTD 신청 가능

오늘 할 일
✓ X Follow
□ Repost
□ Discord Join
□ PREMINT Register

Quality 86 / Alpha 88
Effort 22 / Risk 18
Evidence: HIGH

판단: WL 작업 추천
```

## Phase roadmap

### Phase 1 — Discovery / Verification / Scoring / Telegram
Initial EVM target:
- Ethereum
- Base
- Robinhood Chain

Core sources are designed to degrade independently. OpenSea is a strong structured source but **not** treated as complete NFT coverage.

### Phase 2 — WL / Quest Intelligence
Parse and track requirements such as:
- X social tasks
- PREMINT / Galxe / Guild
- holder/token conditions
- Discord role/level requirements
- registration deadlines and allocation type

User-account actions remain manual.

### Phase 3 — Discord Intelligence
Permitted server-installed bot/API reads for announcements and role/progress where available.

No Discord user self-bot or automated community farming.

### Phase 4 — Personal Alpha Assistant
Combine:
- user progress
- wallet eligibility
- deadlines
- verified mint stages
- watched-wallet/cohort signals
- final pre-mint risk recheck

## Smart-wallet philosophy

The project does **not** simply copy famous wallets.

Longer-term wallet intelligence is intended to identify repeat early minters across historically successful launches, then penalize:
- common-funder clusters
- sybil-like behavior
- wash patterns
- promotion conflicts
- correlated wallets

Named collectors can seed research, but one celebrity-wallet interaction never proves project quality or mint safety.

## Trust model

Discovery and verification are separate jobs.

```text
T0  on-chain evidence
T1  official project channels
T2  structured platforms / launchpads
T3  analysts / collectors / smart wallets
T4  community chatter
```

T3/T4 can create a research lead. They cannot create a trusted mint CTA by themselves.

Even a genuine official X/Discord account does **not** automatically make a new link safe. Wallet-impacting links have an independent consistency/safety gate because official accounts can be compromised.

## Safety boundaries

This project will not automate:
- seed/private-key handling
- wallet signatures
- token/NFT approvals
- mint transactions
- Discord user self-bots
- automated `gm` / chat farming
- fake referrals
- automated repost/comment/tag spam
- impersonation

It may discover requirements, verify evidence, create checklists, and notify the user what to do manually.

## Minimum-Action architecture

This repository adopts selected principles from [`storm-credit/minimum-action-agent-os`](https://github.com/storm-credit/minimum-action-agent-os):

- least tool
- least context
- least authority
- deterministic code before unnecessary LLM calls
- logical role != autonomous agent
- independent critique only where it adds real separation
- plan-drift records
- Shadow Authority / stale-derived-artifact checks
- bounded model action spaces

The Phase 1 hot path is deterministic-first. LLM use is reserved for narrow ambiguous work such as unstructured announcement extraction or conservative identity resolution.

## Current status

See [`docs/PROJECT_STATUS.md`](docs/PROJECT_STATUS.md) for the source of truth.

Current high-level gate:

```text
FREEZE_PENDING / PRODUCTION CODING BLOCKED
```

Completed:
- Deep Design v1.1 canonical sync
- Telegram operational spike (PASS)
- X operational spike (CLOSED, mode frozen in ADR-010)
- cross-system Red Team (P0 = 0)
- minimum-action governance adoption
- harness logical contracts + schemas
- golden eval fixture design
- local action-space audit
- OpenSea operational provider spike

OpenSea live validation observed:
- Ethereum/Base/Robinhood provider keys resolved
- live upcoming queries worked for all three target keys
- 10/10 bounded detail requests succeeded
- 7/10 sampled drops were multi-stage
- 25 total mint stages observed
- real GTD / FCFS / holder / free / public structures observed
- Base returned zero `upcoming` rows while active Base mint surfaces existed, confirming that one calendar/API view is not complete discovery coverage

All Phase 1 blocking operational spikes are closed: OpenSea, Telegram (`SPIKE-TG-001` PASS,
real delivery observed), and X (`SPIKE-X-001` CLOSED, mode frozen in `ADR-010`). The cross-system
Red Team ran on 2026-08-29 and closed every P0.

Remaining before coding: freeze reconciliation only. See
[`docs/PROJECT_STATUS.md`](docs/PROJECT_STATUS.md), which is the authority for current state.

Production feature coding starts only after the start gate is reconciled and set to `PHASE_1_CODING_READY`.

## Important documents

- [`CLAUDE.md`](CLAUDE.md) — project operating constitution / authority map
- [`docs/PROJECT_STATUS.md`](docs/PROJECT_STATUS.md) — current canonical status
- [`docs/PRODUCTION_CODING_START_GATE.md`](docs/PRODUCTION_CODING_START_GATE.md) — coding authorization gate
- [`docs/DEEP_DESIGN.md`](docs/DEEP_DESIGN.md) — canonical product/domain design
- [`docs/SOURCE_STRATEGY.md`](docs/SOURCE_STRATEGY.md) — source trust and discovery strategy
- [`docs/HARNESS_SPEC.md`](docs/HARNESS_SPEC.md) — execution harness contract
- [`docs/HARNESS_SCHEMAS.md`](docs/HARNESS_SCHEMAS.md) — typed logical I/O
- [`docs/EVAL_FIXTURES.md`](docs/EVAL_FIXTURES.md) — adversarial/golden evaluation cases
- [`docs/MINIMUM_ACTION_ADOPTION.md`](docs/MINIMUM_ACTION_ADOPTION.md) — minimum-action adaptation
- [`docs/spikes/SPIKE-MARKET-001-RESULT.md`](docs/spikes/SPIKE-MARKET-001-RESULT.md) — live OpenSea validation

## Disposable operational spikes

The `spikes/` directory and manual GitHub Actions workflows exist only to remove provider uncertainty before production implementation.

They are **not production collectors** and must not silently grow into the product runtime.

See [`spikes/README.md`](spikes/README.md).
