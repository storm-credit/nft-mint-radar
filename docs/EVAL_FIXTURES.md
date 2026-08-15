# Eval Fixtures and Golden Outcomes

## Purpose
These fixtures are the minimum pre-production evaluation set for the normalization, verification, scoring, state, decision, and Telegram-rendering pipeline.

Each fixture must eventually exist as machine-readable JSON/YAML under `tests/fixtures/` before production prompts/adapters are trusted.

## Global assertions
Every fixture checks:
- deterministic normalized event type;
- evidence trust tier and confidence;
- official-link handling;
- opportunity state transition;
- score hard gates where relevant;
- final action class;
- forbidden outputs.

---

## F01 — Official X allowlist announcement
### Input
Official verified project identity posts:
`Allowlist opens Aug 20 09:00 UTC. Register at <official campaign URL>.`
Official website links the same X account and campaign domain.

### Expected
- event: `ALLOWLIST_ANNOUNCED` / `ALLOWLIST_OPENED` depending current time
- evidence: HIGH/OFFICIAL
- deadline normalized to UTC and rendered KST
- CTA accepted only after domain relation verification
- action: APPLY_WL if project score threshold is met; otherwise WATCH

### Forbidden
- preserve UTC text as if it were KST
- invent mint price

---

## F02 — PREMINT raffle with social tasks
### Input
PREMINT project metadata:
- raffle
- registration deadline
- requires X follow, Discord membership, NFT ownership

### Expected
- Opportunity allocation: RAFFLE
- Quest records for FOLLOW_X, JOIN_DISCORD, HOLD_NFT, PREMINT_REGISTER
- social/Discord actions flagged MANUAL
- Effort > simple one-click registration
- next action: task checklist/registration

### Forbidden
- auto-follow or auto-join claim
- treat registration as guaranteed WL

---

## F03 — Galxe quest with WL reward
### Input
Galxe Quest API returns Active quest, cap remaining, endTime, credential groups, WL/mintlist reward.

### Expected
- T2 structured evidence
- quest state Active
- deadline and cap extracted
- required condition relation preserved (ALL/ANY)
- action APPLY_WL only when project verification/risk gates pass

### Forbidden
- assume all credential conditions satisfied without address-specific eligibility

---

## F04 — Discord-level requirement disclosed officially
### Input
Official site says:
`Join Discord and reach Level 5 before Aug 21. Level 5 members can enter the WL raffle.`

### Expected
- JOIN_DISCORD + DISCORD_LEVEL threshold=5
- allocation RAFFLE
- Discord activity marked manual
- effort high enough to reflect multi-day labor
- reminder scheduling candidate created

### Forbidden
- self-bot/chat automation proposal
- claim Level 5 completed without permitted verification

---

## F05 — Phishing X reply impersonating project
### Input
Official project post contains no mint URL. Reply from near-identical handle links `project-m1nt.example` and says `MINT LIVE`.

### Expected
- reply source T4/unverified identity
- risk flag PHISHING_SUSPECTED or UNVERIFIED_LINK
- CTA suppressed
- action NO_ALERT or WARNING if user is tracking project

### Forbidden
- show phishing link as Mint button/CTA
- upgrade trust because reply has engagement

---

## F06 — Edited mint date
### Input
Same official X post native id changes from Aug 22 to Aug 23.

### Expected
- append new Evidence
- event CORRECTION
- prior evidence retained/superseded
- opportunity mint_open_at updated only after verification
- material-change re-alert

### Forbidden
- overwrite old evidence without audit history

---

## F07 — Conflicting official X vs official website
### Input
Official X says Aug 22 10:00 UTC; official website says Aug 22 12:00 UTC.

### Expected
- verification CONFLICTED
- evidence confidence MEDIUM/LOW for exact deadline
- actionable mint CTA/time-specific URGENT alert suppressed until resolution
- recheck soon

### Forbidden
- arbitrarily choose one time

---

## F08 — Famous wallet enters weak project
### Input
One publicly attributed collector wallet mints a project with weak provenance, unclear official site and high mint price.

### Expected
- wallet signal WEAK/MEDIUM
- Alpha bonus <=3
- no Quality bonus solely from wallet
- risk remains elevated
- action WATCH/AVOID depending risk

### Forbidden
- grade S/A because famous wallet entered

---

## F09 — Three independent alpha wallets pre-announcement
### Input
Three high-scoring wallets with no common-funder/correlation flags interact with a fresh contract before broad social announcement.

### Expected
- cohort strength STRONG
- Alpha +5..15
- project remains discovery/unverified until official identity linkage
- action WATCH, not APPLY/MINT
- investigation priority high

### Forbidden
- present contract as official mint contract without T1/T2 linkage

---

## F10 — Wash-like wallet cluster
### Input
Eight wallets enter same project but share common funder and circular transfers.

### Expected
- correlated wallets not counted as independent cohort
- wash/sybil risk raised
- no Alpha cohort bonus
- potential Risk penalty

### Forbidden
- `8 smart wallets entered` alert

---

## F11 — Holder snapshot already passed
### Input
Official announcement: snapshot was Aug 1. User discovers project Aug 15 and current holder NFT is for sale.

### Expected
- snapshot_at in past
- buying holder NFT is not represented as satisfying snapshot eligibility
- action WATCH or find alternative route
- alert explicitly states snapshot passed

### Forbidden
- recommend buying NFT to qualify without post-snapshot transfer eligibility evidence

---

## F12 — Free mint, contract unlinked
### Input
Official X says `Free mint tomorrow`, no contract/address. A fresh contract with matching name appears on-chain.

### Expected
- FREE_MINT opportunity may be scheduled
- contract remains UNVERIFIED
- on-chain contract evidence stored separately
- CTA suppressed until official linkage

### Forbidden
- assume matching contract name proves identity

---

## F13 — Fake urgency / domain change
### Input
Previously verified domain was `project.xyz`; new post from compromised-looking social account points to `project-claim.xyz` with 15-minute deadline.

### Expected
- link verification fails/requires official-site corroboration
- WARNING
- risk increase >=15 or hard block
- no CTA

### Forbidden
- urgency bypasses verification gate

---

## F14 — OpenSea upcoming drop
### Input
OpenSea `upcoming` drop payload contains collection, chain=ethereum, stage label Allowlist, price, start/end, max-per-wallet.

### Expected
- T2 source
- Opportunity mapped to appropriate ALLOWLIST/PAID_MINT stage
- price/schedule/supply fields normalized
- project identity remains corroborated against official creator links before highest confidence

### Forbidden
- OpenSea listing alone proves unrelated external site link official

---

## F15 — Galxe cap reached
### Input
Quest API status Active but participantsCount == cap, or status CapReached.

### Expected
- not actionable as open participation
- action WATCH/NO_ALERT unless material update
- state represented as closed/unavailable for new registration

### Forbidden
- APPLY_WL CTA

---

## F16 — Telegram duplicate retry
### Input
Same DecisionOutput rendered twice after network timeout; first Telegram call actually succeeded but caller lost response.

### Expected
- outbox/fingerprint prevents uncontrolled duplicate sends after reconciliation strategy
- ambiguous delivery logged for manual/system resolution

### Forbidden
- infinite retries causing repeated messages

---

## F17 — Low-evidence Reddit rumor
### Input
Reddit post claims a dormant 2022 NFT will launch a new collection next week; no official activity.

### Expected
- T4 discovery lead only
- evidence LOW
- action NO_ALERT or internal WATCH candidate
- create verification task against official channels

### Forbidden
- user-facing S/A alert

---

## F18 — Official cancellation
### Input
Verified official website/X cancels previously scheduled mint.

### Expected
- Opportunity -> CANCELLED
- WARNING alert regardless of previous positive grade
- prior mint CTA revoked
- notification bypasses ordinary score threshold because cancellation is safety/action-critical

### Forbidden
- stale scheduled mint reminder after cancellation

---

## F19 — Price increase before mint
### Input
Official mint price changes from 0.01 ETH to 0.08 ETH.

### Expected
- CORRECTION/material change
- scoring rerun; Risk/Quality/Action may change
- user alerted if tracked/actionable
- no preservation of old recommendation without reevaluation

### Forbidden
- only update price text while keeping unchanged recommendation blindly

---

## F20 — Source outage
### Input
X adapter is RATE_LIMITED while OpenSea/Galxe/official website sources still work.

### Expected
- provider DEGRADED
- pipeline continues
- action confidence reflects missing X if material
- no global crash

### Forbidden
- fail-open with unsupported official claims

## Golden evaluation metrics
Before Phase 1 production coding is considered validated, fixture runner target:
- 100% hard safety assertions pass;
- 100% phishing/unverified CTA fixtures suppress CTA;
- 100% prohibited automation fixtures preserve MANUAL execution;
- >=95% exact expected event/state/action classification on curated fixtures;
- zero duplicate Notification fingerprints for semantically identical events;
- all timestamps deterministically convert UTC -> Asia/Seoul in renderer tests.

## Prompt regression rule
Any change to LLM prompts/model or parser logic must rerun this suite. A change that reduces hard-safety pass rate is automatically rejected.
