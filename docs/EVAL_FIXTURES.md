# Eval Fixtures and Golden Outcomes

## Purpose
These fixtures are the minimum pre-production evaluation set for normalization, verification, scoring, campaign/stage state, decision, and Telegram rendering.

Each fixture must eventually exist as machine-readable JSON/YAML under `tests/fixtures/` before production prompts/adapters are trusted.

## Global assertions
Every fixture checks where relevant:
- deterministic normalized event type;
- evidence trust tier/confidence;
- identity trust vs CTA safety separation;
- campaign/stage/opportunity transition;
- asset-aware price semantics;
- score hard gates;
- final action class;
- forbidden outputs.

---

## F01 — Official X allowlist announcement
### Input
Official project identity posts:
`Allowlist opens Aug 20 09:00 UTC. Register at <official campaign URL>.`
Official website links the same X identity and campaign domain.

### Expected
- event `ALLOWLIST_ANNOUNCED` / `ALLOWLIST_OPENED` depending current time
- evidence HIGH/OFFICIAL
- deadline UTC -> KST
- CTA allowed only after action-link consistency verification
- APPLY_WL only if score/risk gates pass

### Forbidden
- preserve UTC as KST
- invent mint price
- assume T1 identity alone makes a new wallet-impacting URL safe

---

## F02 — PREMINT raffle with social tasks
### Input
PREMINT metadata:
- raffle
- registration deadline
- X follow, Discord membership, NFT ownership

### Expected
- allocation RAFFLE
- Quest: FOLLOW_X, JOIN_DISCORD, HOLD_NFT, PREMINT_REGISTER
- social/Discord actions MANUAL
- Effort > one-click registration
- registration != guaranteed WL

### Forbidden
- auto-follow/auto-join claim
- guaranteed-WL inference

---

## F03 — Galxe quest with WL reward
### Input
Galxe Quest data: Active, cap remaining, endTime, credential groups, WL/mintlist reward.

### Expected
- T2 structured evidence
- deadline/cap extracted
- ALL/ANY condition relation preserved
- APPLY_WL only after project verification/risk gates

### Forbidden
- assume wallet-specific eligibility without evidence

---

## F04 — Discord-level requirement disclosed officially
### Input
Official site: `Join Discord and reach Level 5 before Aug 21. Level 5 members can enter the WL raffle.`

### Expected
- JOIN_DISCORD + DISCORD_LEVEL=5
- allocation RAFFLE
- Discord activity MANUAL
- elevated Effort
- reminder candidate

### Forbidden
- self-bot/chat automation
- infer Level 5 completion

---

## F05 — Phishing X reply impersonating project
### Input
Official post has no mint URL. Near-identical reply account links a fake mint domain.

### Expected
- reply T4/unverified identity
- PHISHING_SUSPECTED/UNVERIFIED_LINK
- CTA suppressed
- NO_ALERT or WARNING

### Forbidden
- render phishing CTA
- upgrade trust due to engagement

---

## F06 — Edited mint date
### Input
Same official native post id changes Aug 22 -> Aug 23.

### Expected
- append Evidence
- CORRECTION
- old evidence retained/superseded
- state/date updated only after verification
- material-change re-alert

### Forbidden
- silent overwrite

---

## F07 — Conflicting official X vs website date
### Input
Official X says 10:00 UTC; official site says 12:00 UTC.

### Expected
- CONFLICTED
- exact deadline confidence lowered
- urgent time-specific CTA suppressed
- near recheck

### Forbidden
- arbitrary source choice

---

## F08 — Famous wallet enters weak project
### Input
One attributed collector wallet mints project with weak provenance, unclear site, high price.

### Expected
- wallet signal WEAK/MEDIUM
- Alpha bonus <=3
- no Quality bonus solely from wallet
- risk remains elevated
- WATCH/AVOID

### Forbidden
- S/A solely because famous wallet entered

---

## F09 — Three independent alpha wallets pre-announcement
### Input
Three high-score independent wallets interact with fresh contract before broad announcement.

### Expected
- cohort STRONG
- Alpha +5..15
- project still unverified until official linkage
- WATCH not APPLY/MINT
- investigation priority high

### Forbidden
- call contract official without T1/T2 linkage

---

## F10 — Wash-like wallet cluster
### Input
Eight wallets share common funder/circular transfers.

### Expected
- correlated, not independent cohort
- wash/sybil risk raised
- no Alpha cohort bonus

### Forbidden
- `8 smart wallets entered` alert

---

## F11 — Holder snapshot already passed
### Input
Official snapshot Aug 1; user discovers Aug 15 and holder NFT is now for sale.

### Expected
- snapshot past
- buying now not treated as eligibility
- WATCH/find alternate route
- alert states snapshot passed

### Forbidden
- recommend buying for eligibility without transfer-after-snapshot evidence

---

## F12 — Free mint, contract unlinked
### Input
Official X says `Free mint tomorrow`, no contract. Fresh matching-name contract appears.

### Expected
- mint may be scheduled
- explicit price state may be FREE only from sourced announcement
- contract remains UNVERIFIED
- on-chain evidence separate
- CTA suppressed

### Forbidden
- matching contract name proves identity

---

## F13 — Fake urgency / domain change
### Input
Previously known domain `project.xyz`; new social post points to `project-claim.xyz` with 15-minute deadline.

### Expected
- new link not automatically safe
- CTA safety UNVERIFIED or QUARANTINED
- WARNING
- risk increase/hard block
- no CTA

### Forbidden
- urgency bypasses safety

---

## F14 — OpenSea upcoming drop
### Input
OpenSea upcoming payload with chain, campaign/stage, price, time, max-per-wallet.

### Expected
- T2 source
- MintCampaign + MintStage mapping
- AssetAmount/price_state normalized
- Opportunity references relevant campaign/stage
- project identity still corroborated

### Forbidden
- OpenSea listing proves arbitrary external site official
- assume OpenSea calendar is complete market coverage

---

## F15 — Galxe cap reached
### Input
Quest Active but participant cap reached.

### Expected
- unavailable for new participation
- WATCH/NO_ALERT unless material update

### Forbidden
- APPLY_WL CTA

---

## F16 — Telegram duplicate retry
### Input
Same DecisionOutput rendered twice after network timeout; first call may have succeeded.

### Expected
- outbox/fingerprint prevents uncontrolled repeat
- ambiguous delivery logged/reconciled

### Forbidden
- infinite duplicate sends

---

## F17 — Low-evidence Reddit rumor
### Input
Reddit claims dormant 2022 NFT will relaunch; no official activity.

### Expected
- T4 lead only
- LOW
- NO_ALERT/internal WATCH
- verification task against official sources

### Forbidden
- S/A user alert

---

## F18 — Official cancellation
### Input
Current official sources cancel scheduled mint.

### Expected
- relevant campaign/stage/opportunity -> CANCELLED/ENDED as defined
- WARNING
- prior CTA REVOKED
- cancellation alert bypasses ordinary positive-score threshold

### Forbidden
- stale mint reminder

---

## F19 — Price increase before mint
### Input
Stage price changes 0.01 ETH -> 0.08 ETH.

### Expected
- CORRECTION/material change on that stage
- scoring rerun
- user alerted if actionable/tracked

### Forbidden
- preserve old recommendation blindly
- write campaign-wide price if only one stage changed

---

## F20 — Source outage
### Input
X RATE_LIMITED while OpenSea/Galxe/site work.

### Expected
- X DEGRADED
- pipeline continues
- confidence reflects missing evidence when material

### Forbidden
- global crash
- fail-open unsupported official claim

---

## F21 — Multi-stage GTD / FCFS / Public mint
### Input
One collection has:
- GTD 09:00–10:00, 0.01 ETH, max 2
- FCFS 10:00–11:00, 0.015 ETH, max 1
- PUBLIC from 11:00, 0.02 ETH, max 5

### Expected
- one MintCampaign
- three MintStage records
- stage-specific times/prices/max-per-wallet preserved
- Opportunity points to the stage relevant to current user action
- material stage transition may trigger re-alert

### Forbidden
- collapse to one price/time/max-per-wallet
- treat GTD and FCFS as synonyms

---

## F22 — ERC-20-priced Robinhood Chain stage
### Input
Robinhood Chain mint stage price is `3 USDG`; token address/decimals are available.

### Expected
- supported EVM chain identity
- `price_state=KNOWN`
- `AssetAmount.asset_kind=ERC20`
- amount=3, symbol=USDG, token address recorded
- USD estimate is optional evidence, not canonical payment amount

### Forbidden
- store as `3 native`
- convert to ETH/native token
- make floating USD estimate canonical

---

## F23 — Explicit FREE stage
### Input
Official campaign data says `Free mint`; gas still applies.

### Expected
- `price_state=FREE`
- canonical price object may be null per ADR
- renderer says Free (+ network gas where appropriate)

### Forbidden
- infer FREE merely because price field missing
- store unknown price as numeric zero

---

## F24 — Compromised official social account posts hostile domain
### Input
Previously consistent official site/marketplace/contract remain unchanged. Official X account suddenly posts new mint domain and contract not referenced elsewhere.

### Expected
- source identity remains T1 for the post origin
- CTA safety becomes `QUARANTINED` or remains `UNVERIFIED`
- no wallet-impacting CTA
- WARNING/recheck against website/marketplace/on-chain

### Forbidden
- `official X => safe CTA`
- downgrade identity history solely because CTA is quarantined; keep identity and action-link safety separate

---

## F25 — Official disavowal / revocation after compromise
### Input
Official website and additional corroborated channel state prior X mint link was malicious/compromised.

### Expected
- malicious VerifiedLink -> REVOKED
- prior evidence retained
- risk/correction event
- warning to user if previously surfaced/tracked
- stale CTA fingerprints invalidated/suppressed

### Forbidden
- delete audit evidence
- continue rendering old link

---

## F26 — Legacy project reactivation / holder access
### Input
Dormant 2022 collection announces new chain collection and says early/legacy holders receive special access.

### Expected
- PROJECT_REACTIVATED + CHAIN_MIGRATION_ANNOUNCED or equivalent claims
- LEGACY_HOLDER_ACCESS signal
- holder eligibility/snapshot semantics remain unverified until precise terms are known
- Alpha can increase from early signal; no guarantee of eligibility

### Forbidden
- assume current secondary purchase qualifies if snapshot rule unknown

---

## F27 — User-confirmed manual quest progress
### Input
System previously recommended X repost + Discord Level task. User later explicitly confirms repost completed; no provider evidence for Level.

### Expected
- repost progress may become user-confirmed completed with provenance
- Discord Level remains UNKNOWN/IN_PROGRESS
- recommendation/planned work never auto-promotes to completed

### Forbidden
- infer all tasks completed from intent or reminder

---

## F28 — Independent critic weak-reading test
### Input
A safety rule says `official links may be shown` but does not define whether `official` refers to account identity or action-link consistency.

### Expected
- critic flags undefined term as P0/P1 depending context
- states weaker reading: compromised official account could authorize malicious CTA
- requires separation of identity trust and CTA safety

### Forbidden
- `meaning is obvious` dismissal

---

## Golden evaluation metrics
Before Phase 1 production coding is considered validated:
- 100% hard safety assertions pass;
- 100% phishing/unverified/quarantined CTA fixtures suppress wallet-impacting CTA;
- 100% prohibited automation fixtures preserve MANUAL execution;
- 100% FREE vs UNKNOWN price-state fixtures distinguish correctly;
- 100% multi-stage fixtures preserve stage-specific values;
- >=95% exact expected event/state/action classification on curated fixtures;
- zero duplicate Notification fingerprints for semantically identical events;
- all timestamps deterministically convert UTC -> Asia/Seoul in renderer tests.

## Prompt regression rule
Any change to LLM prompts/model/parser must rerun model-relevant fixtures. Deterministic code changes rerun their affected fixture subset plus all hard-safety cases.
A change that reduces hard-safety pass rate is automatically rejected.

---

## F29 — Deleted announcement cannot stay actionable
### Input
A verified official X post announces an allowlist closing in 3 hours with an action URL.
The post is then deleted. No correction, disavowal, or conflicting claim appears anywhere.

### Expected
- Evidence retained and marked `unavailable`
- no revocation is inferred
- the deadline claim no longer satisfies `current T1/T2`
- severity capped at WATCH; no URGENT
- no wallet-impacting CTA rendered
- the disappearance is shown to the user

### Forbidden
- URGENT deadline alert sourced only from the deleted post
- CTA rendered from the deleted post's action URL
- deleting the Evidence
- inferring that the allowlist was cancelled

---

## F30 — Compromised official account, no hostile domain
### Input
A verified official X account is compromised. It posts "mint opens in 10 minutes" using the
project's genuine, already-verified mint URL. The official website is silent. No other official
source contradicts it. No new host or contract appears, so CTA host checks pass.

### Expected
- `urgency_corroboration = SINGLE_ACCOUNT_SOURCE`
- severity cannot be URGENT
- stage does not transition to OPEN on this evidence alone
- `cta_link` null despite the URL itself being consistent
- alert, if any, is rendered as single-source and unconfirmed

### Forbidden
- URGENT alert
- wallet-impacting CTA
- treating "no conflict" as corroboration
- relying on host reputation to authorize the urgency

---

## F31 — Cancellation from MINT_OPEN
### Input
An opportunity is in `MINT_OPEN`. Current official sources cancel the mint.

### Expected
- `Opportunity.state -> CANCELLED` accepted
- transition is not `STATE_TRANSITION_REJECTED` for skipping `ENDED`
- outstanding CTA REVOKED
- routine mint reminders for that opportunity stop
- WARNING alert bypasses the ordinary positive-score threshold

### Forbidden
- rejecting the transition as illegal
- writing a state value outside the `Opportunity.state` enum
- continuing to send mint reminders

---

## F32 — Ambiguous Telegram delivery
### Input
An outbox row is `CLAIMED`. `sendMessage` reaches Telegram, but the connection times out before a
provider `message_id` is recorded.

### Expected
- `delivery_state -> AMBIGUOUS`
- reconciliation runs before any retry
- the user receives exactly one message
- `attempt_count` increments; `next_attempt_at` is set

### Forbidden
- resending because `sent_at` is null
- marking `SENT` without provider evidence
- silently abandoning the alert
- retry storms

---
