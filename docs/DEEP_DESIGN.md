# Deep Design

## 0. Readiness intent
This document converts the architecture skeleton into a concrete design contract. Production feature code remains blocked until the spike gates in `SPIKE_PLAN.md` are resolved or explicitly waived by ADR.

## 1. Product contract

### Primary user
A single NFT participant who wants to discover credible allowlist/mint opportunities early enough to act, while minimizing wasted social/Discord work and phishing risk.

### Primary job-to-be-done
`Find -> verify -> prioritize -> tell me exactly what matters next.`

The product must answer:
1. What opportunity appeared?
2. Is it official/credible?
3. Is it still early enough to act?
4. What must the user do now or later?
5. How much time/cost/risk is involved?
6. What changed since the last alert?

### Phase 1 success conditions
- Candidate events from configured sources are normalized into one canonical event model.
- Actionable facts are never promoted from T3/T4 discovery-only sources without corroboration.
- S/A alerts contain evidence confidence, KST deadline when known, next action, and only verified official links.
- Duplicate/repeated signals do not create duplicate notifications.
- A changed official deadline/risk state can create a material-change re-alert.
- No wallet signature, approval, transaction, social engagement or Discord self-bot path exists.

### Phase 1 source scope
P0 runtime-capable sources:
- official websites/docs discovered from verified project identities
- official X when API/access budget allows; adapter must degrade cleanly if unavailable
- OpenSea upcoming/drop detail APIs
- Galxe Quest API for known/discovered quests
- public on-chain evidence through explorers/RPC/indexed APIs chosen per chain

P1/optional adapters:
- PREMINT Connect when API access is available; otherwise official registration URL is tracked as evidence and parsed manually/through permitted page access
- Guild public requirement pages/API surfaces when available
- Dune latest-query results / selected parameterized queries
- official Telegram announcement channels when lawful/public access is available

Phase 1 discovery-only weak sources:
- Reddit
- public Telegram alpha groups
- generic X accounts
- influencer/collector posts

### Initial chain scope
- Ethereum
- Base

Rationale: keep the first contract/deployer/mint model EVM-only. Add Solana or other chains only through a new chain-adapter ADR after Phase 1 is stable.

### Explicit non-goals
- auto minting
- wallet signing/approval
- private-key/seed handling
- automated X follow/like/repost/comment/tag
- automated Discord chat/activity/referral farming
- guaranteed profit or financial advice
- universal coverage of every chain/marketplace in Phase 1

## 2. Canonical schemas

Schemas below are logical contracts. Implementation may use Pydantic/JSON Schema/TypeScript types but field semantics must remain stable.

### 2.1 Project
```yaml
Project:
  id: string                       # internal stable UUID
  canonical_name: string
  aliases: [string]
  chains: [string]
  official_links:
    website: [VerifiedLink]
    x: [VerifiedLink]
    discord: [VerifiedLink]
    telegram: [VerifiedLink]
    docs: [VerifiedLink]
    opensea: [VerifiedLink]
  contracts: [ContractIdentity]
  status: DISCOVERED|ACTIVE|DORMANT|ENDED|SUSPECT|BLOCKED
  created_at: datetime_utc
  updated_at: datetime_utc
```

### 2.2 Source
```yaml
Source:
  id: string
  source_type: X|WEBSITE|DISCORD|TELEGRAM|OPENSEA|PREMINT|GALXE|GUILD|DUNE|ONCHAIN|REDDIT|OTHER
  trust_tier: T0|T1|T2|T3|T4
  roles: [DISCOVERY|VERIFICATION|ONCHAIN|SENTIMENT|BEHAVIOR]
  identity: string
  canonical_url: string|null
  auth_profile: string|null
  enabled: boolean
  health: HEALTHY|DEGRADED|DISABLED|UNKNOWN
```

### 2.3 Evidence
```yaml
Evidence:
  id: string
  project_id: string|null
  opportunity_id: string|null
  source_id: string
  source_event_id: string|null
  captured_at: datetime_utc
  source_published_at: datetime_utc|null
  claim_key: string
  normalized_value: any
  raw_excerpt_or_hash: string|null
  canonical_url: string|null
  trust_tier: T0|T1|T2|T3|T4
  confidence: LOW|MEDIUM|HIGH
  verification_state: UNVERIFIED|CORROBORATED|OFFICIAL|CONFLICTED|REVOKED|STALE
  valid_until: datetime_utc|null
  supersedes_evidence_id: string|null
```
Evidence is append-only. Corrections create new Evidence; prior evidence is never silently overwritten.

### 2.4 Opportunity
```yaml
Opportunity:
  id: string
  project_id: string
  type: ALLOWLIST|RAFFLE|HOLDER_MINT|FREE_MINT|PAID_MINT|PUBLIC_MINT|AIRDROP|OTHER
  state: string
  chain: string|null
  contract_address: string|null
  registration_open_at: datetime_utc|null
  registration_close_at: datetime_utc|null
  snapshot_at: datetime_utc|null
  results_at: datetime_utc|null
  mint_open_at: datetime_utc|null
  mint_close_at: datetime_utc|null
  mint_price_native: decimal|null
  max_per_wallet: integer|null
  supply: integer|null
  allocation_type: FCFS|RAFFLE|GUARANTEED|HOLDER|PUBLIC|UNKNOWN
  official_action_url: VerifiedLink|null
  evidence_ids: [string]
  evidence_confidence: LOW|MEDIUM|HIGH
  updated_at: datetime_utc
```

### 2.5 Quest
Defined now so Phase 2 does not force a domain rewrite.
```yaml
Quest:
  id: string
  opportunity_id: string
  action_type: FOLLOW_X|LIKE_X|REPOST_X|COMMENT_X|TAG_FRIEND|JOIN_DISCORD|DISCORD_ROLE|DISCORD_LEVEL|GALXE|GUILD|PREMINT_REGISTER|HOLD_NFT|HOLD_TOKEN|ONCHAIN_ACTION|REFERRAL|CUSTOM
  required: boolean
  execution_mode: MANUAL|EXTERNAL_PLATFORM|READ_ONLY_VERIFY
  target: string|null
  quantity_or_threshold: string|null
  deadline_at: datetime_utc|null
  verification_source_id: string|null
  safety_class: SAFE_MANUAL|WALLET_SIGNATURE_REQUIRED|SOCIAL_ACTION|DISCORD_ACTIVITY|UNKNOWN
```

### 2.6 UserProgress
```yaml
UserProgress:
  user_key: string
  opportunity_id: string
  quest_id: string|null
  state: UNKNOWN|TODO|IN_PROGRESS|COMPLETED|VERIFIED|WON|WAITLISTED|LOST|EXPIRED|SKIPPED
  observed_at: datetime_utc
  verification_source_id: string|null
  note: string|null
```

### 2.7 WalletEntity
```yaml
WalletEntity:
  id: string
  chain: string
  address: string
  labels: [string]
  category: COLLECTOR|TRADER|ARTIST|FUND|DEPLOYER|INFLUENCER|UNKNOWN
  identity_confidence: LOW|MEDIUM|HIGH
  identity_evidence_ids: [string]
  alpha_wallet_score: float|null
  wash_sybil_risk: float|null
  last_seen_at: datetime_utc|null
```

### 2.8 InfluencerEntity
```yaml
InfluencerEntity:
  id: string
  platform: string
  handle: string
  category: ANALYST|COLLECTOR|ARTIST|FOUNDER|TRADER|SECURITY_RESEARCHER|OTHER
  reliability_score: float|null
  promotion_risk: float|null
  historical_lead_time_minutes: float|null
  false_positive_rate: float|null
  last_active_at: datetime_utc|null
```

### 2.9 Notification
```yaml
Notification:
  id: string
  fingerprint: string
  project_id: string
  opportunity_id: string|null
  class: DISCOVERY|WL_OPEN|DEADLINE|COHORT_HIT|CONTRACT_LINKED|RISK_DOWNGRADE|WL_RESULT|MINT_RECHECK
  severity: INFO|WATCH|ACTION|URGENT|WARNING
  action: WATCH|APPLY_WL|PREPARE|MINT_RECHECK|AVOID|NO_ALERT
  material_change_keys: [string]
  rendered_payload_hash: string
  sent_at: datetime_utc|null
```

### 2.10 VerifiedLink
```yaml
VerifiedLink:
  url: string
  normalized_host: string
  relation: OFFICIAL_SITE|OFFICIAL_SOCIAL|OFFICIAL_CAMPAIGN|OFFICIAL_MARKETPLACE|OFFICIAL_CONTRACT|OTHER
  verification_state: UNVERIFIED|CORROBORATED|OFFICIAL|REVOKED|SUSPICIOUS
  evidence_ids: [string]
  checked_at: datetime_utc
```

## 3. Project identity and merge/split rules

### Merge only when at least one strong relation exists
- same officially linked contract/deployer; or
- official site explicitly links both identities; or
- official T1 account announces rebrand/migration and links both identities.

### Never merge solely because
- names/logos are similar;
- an influencer says they are related;
- wallets overlap;
- community chatter claims a rebrand.

### Split when
- official channels disavow a cloned/migrated identity;
- contract ownership/team relation cannot be corroborated;
- a compromised domain/account is detected.

Identity operations are auditable and keep prior aliases/evidence.

## 4. Event normalization

### RawEvent envelope
```yaml
RawEvent:
  event_id: string
  source_id: string
  source_native_id: string|null
  fetched_at: datetime_utc
  published_at: datetime_utc|null
  event_kind: POST|PAGE|QUEST|DROP|CHAIN_EVENT|WALLET_EVENT|MESSAGE|OTHER
  canonical_url: string|null
  author_identity: string|null
  title: string|null
  text: string|null
  structured_payload: object|null
  content_hash: string
  fetch_metadata: object
```

### NormalizedEvent
```yaml
NormalizedEvent:
  id: string
  raw_event_ids: [string]
  project_candidate: string|null
  event_type: PROJECT_SIGNAL|ALLOWLIST_ANNOUNCED|ALLOWLIST_OPENED|ALLOWLIST_CLOSED|QUEST_CHANGED|SNAPSHOT_ANNOUNCED|SNAPSHOT_PASSED|MINT_SCHEDULED|MINT_OPENED|MINT_ENDED|CONTRACT_DEPLOYED|CONTRACT_OFFICIALLY_LINKED|RISK_SIGNAL|WALLET_SIGNAL|SOCIAL_SIGNAL|CORRECTION|CANCELLATION|OTHER
  claims: [NormalizedClaim]
  observed_at: datetime_utc
  source_time: datetime_utc|null
  confidence: LOW|MEDIUM|HIGH
```

### Time semantics
- `published_at/source_time`: timestamp asserted by the source.
- `fetched_at/observed_at`: when our system observed it.
- all stored UTC.
- render KST for user-facing deadlines.
- if source gives only a date/no timezone, confidence is downgraded and the alert must say timezone is unresolved.

### Edit/delete handling
- content hash change on same native id -> emit `CORRECTION` and append evidence.
- source disappears -> retain prior evidence; mark source event `DELETED_OR_UNAVAILABLE`; do not infer revocation unless official correction/disavowal exists.

### Dedup
Exact duplicate key:
`source_id + source_native_id + content_hash`.

Cross-source semantic dedup candidate:
`project_id + event_type + normalized primary claim + time bucket`.

Semantic dedup may merge notifications but never deletes evidence.

## 5. Verification model

### Claim classes and minimum evidence

#### Mint/WL URL
Must have one of:
- T1 official site/account directly links it; or
- T2 platform page is directly linked from T1; or
- official marketplace T2 page plus project identity corroboration.

T3/T4 link is never a CTA.

#### Contract address
`OFFICIAL` only when T1/T2 official channel links address/marketplace page and T0 chain data confirms the address exists.

#### Date/deadline
Actionable with one current T1 or T2 source unless conflict exists. If T1 and T2 conflict, state becomes `CONFLICTED` and no irreversible CTA is promoted until resolved.

#### Holder/snapshot eligibility
Requires T1/T2 claim plus wallet/collection identity verification. Past snapshots must be represented explicitly; buying after a passed snapshot must not be recommended as eligibility.

### Confidence
- HIGH: direct current T0/T1/T2 evidence with identity linkage and no conflict.
- MEDIUM: corroborated but incomplete, or time/identity detail remains unresolved.
- LOW: discovery-only signal, stale evidence, inferred relation, or unresolved conflict.

### Evidence freshness defaults
- mint/WL URL: recheck before every ACTION/URGENT alert and again within 15 minutes of mint CTA.
- mint/WL deadline: recheck within 60 minutes when D-1, within 15 minutes when under 2 hours.
- contract address: recheck official linkage before `MINT_RECHECK`.
- project identity links: 7-day soft TTL, immediate recheck on conflict/risk event.
- wallet labels: 30-day soft TTL unless first-party mapping persists.

## 6. Opportunity state machine

Canonical states:
`RUMORED -> DISCOVERED -> REGISTRATION_PENDING -> REGISTRATION_OPEN -> REGISTRATION_CLOSED -> RESULTS_PENDING -> (WON|WAITLISTED|LOST) -> MINT_SCHEDULED -> MINT_OPEN -> ENDED`

Alternative branches:
- holder/direct mint: `DISCOVERED -> MINT_SCHEDULED -> MINT_OPEN -> ENDED`
- cancellation: any pre-ended active state -> `CANCELLED`
- correction: state remains but fields/evidence version update; if correction changes phase, transition through validated target state.

Rules:
- state may advance only with sufficient evidence for that transition.
- backwards transition is not allowed except as `CORRECTION` with explicit official evidence.
- `MINT_OPEN` never derives only from a clock; require current official/platform/on-chain confirmation.
- `WON/WAITLISTED/LOST` is user-specific and belongs in UserProgress when wallet-specific; Opportunity stays at `RESULTS_PENDING/MINT_SCHEDULED` globally.
- illegal transition -> `STATE_TRANSITION_REJECTED` error + evidence retained for review.

## 7. Scoring model v1
Scores are prioritization aids, not return predictions.

### Quality 0–100
- team/project provenance: 0–20
- existing community/history: 0–20
- product/art/cultural differentiation: 0–15
- transparent mint mechanics: 0–15
- organic demand evidence: 0–15
- ecosystem/partner credibility: 0–10
- execution history: 0–5

### Alpha 0–100
- lead time before public mint: 0–25
- low public saturation / early-stage signal: 0–20
- WL still obtainable: 0–20
- early independent wallet cohort signal: 0–20
- unique-source lead advantage: 0–15

### Effort 0–100, lower is better
- simple register/follow: +5 to +15
- multiple social actions: +10 to +25
- Discord role/level over days: +20 to +50
- referral/invite dependency: +20 to +40
- on-chain paid action: +20 to +50
- uncertain/moderator-selected criteria: +20

### Risk 0–100, lower is better
Penalties accumulate:
- unverified official linkage +30
- contract/site mismatch +40
- suspicious domain/homograph +40
- conflicting official instructions +25
- anonymous/new team without history +10
- concentrated supply/team allocation concern +10 to +25
- wash/sybil-like activity +10 to +30
- promotion/shill conflict +5 to +20
- high mint price relative to evidence +5 to +20
- wallet-drainer/signature anomaly signal +100 hard block

### Evidence adjustment
- HIGH: x1.00
- MEDIUM: x0.85
- LOW: cannot exceed B/action WATCH regardless of raw score.

### Wallet cohort adjustment
- one famous wallet: +0 to +3 Alpha only
- 2 independent validated alpha wallets: +3 to +7 Alpha
- 3+ independent high-score wallets: +5 to +15 Alpha
- correlated/funded/sybil cluster: no bonus and may add Risk

### Influencer cap
Influencer/social mention may contribute at most +5 Alpha and 0 Quality unless independently supported by other evidence.

### Action score
```text
base = 0.35*Quality + 0.35*Alpha + 0.20*(100-Risk) + 0.10*(100-Effort)
action_score = base * evidence_multiplier
```
Hard gates override score:
- suspicious/unverified CTA link -> no APPLY/MINT action
- Risk >= 70 -> AVOID or WATCH only
- LOW evidence -> WATCH only

### Grades
- S: >= 88 and HIGH evidence and Risk < 30
- A: >= 78 and evidence >= MEDIUM and Risk < 45
- B: 65–77
- C: 50–64
- D/AVOID: <50 or hard-risk gate

Calibration rule: weights/thresholds are provisional until fixture regression + historical backtest. Any material change requires an ADR or scoring-version bump.

## 8. Dune / wallet intelligence design

### Seed wallet policy
A public wallet can be seeded only if address identity is first-party or strongly corroborated and stored with confidence evidence. Named wallets are discovery seeds, not endorsements.

### AlphaWalletScore v1 concept
```text
35% repeated early-entry percentile on later-successful collections
20% independent project diversity
15% holding/persistence quality
15% realized outcome proxy where measurable
15% recency
minus wash/sybil/conflict penalties
```
Do not compute a production score until historical benchmark definitions are fixed through the Dune spike.

### Cohort independence
Two wallets are not independent when strong evidence indicates:
- common funder at short distance;
- repeated direct transfers among them;
- same deployer/team-controlled cluster;
- synchronized high-frequency patterns suggesting automation/sybil.

### Dune use pattern
Prefer cached/latest result retrieval for frequent reads; trigger fresh executions only at planned refresh windows. Result filtering/column selection should minimize transferred rows/credits.

Fallback: Dune unavailable -> wallet cohort features become `UNKNOWN`; core discovery/verification continues.

## 9. Phase 2 WL/Quest contract

### Allocation representation
- FCFS: speed-sensitive, capacity required when known.
- RAFFLE: deadline/result time + winner count/odds proxy when known.
- GUARANTEED: eligibility conditions must be explicit.
- HOLDER: collection/token and snapshot semantics required.

### Mandatory vs optional
Every parsed task includes `required`. Ambiguous language produces `required=null/UNKNOWN` in parser output and blocks `all_requirements_complete` claims.

### Manual-only execution
Social actions, CAPTCHA, wallet connection/signing, Discord chat/activity, invite/referral actions are always user-performed. The system may deep-link and remind only.

## 10. Notification design

### Severity
- INFO: non-actionable context; normally batched/suppressed.
- WATCH: promising candidate, no immediate task.
- ACTION: user should perform a reversible/manual step such as WL registration.
- URGENT: deadline/mint recheck within configured urgency window.
- WARNING: material risk/correction/cancellation.

### Alert triggers
- first S/A candidate crossing confidence gate
- WL/quest becomes open
- material requirement/deadline change
- validated wallet cohort raises Alpha across threshold
- official contract linkage appears
- risk worsens by >=15 points or crosses 45/70 thresholds
- user-specific WL result becomes known
- mint window enters final recheck period

### No-alert policy
No notification for:
- repeated same evidence
- T3/T4 rumor without corroboration
- score change <5 with no state/action change
- routine source-health changes unless coverage becomes critically blind

### Fingerprint
`project_id | opportunity_id | notification_class | normalized_action | deadline_bucket | material_version`

### Material re-alert
Re-alert when any of:
- state changes
- deadline moves >=15 minutes when under D-1, or >=2 hours otherwise
- price/supply/max-per-wallet changes
- official action URL/contract changes
- risk +/-15 or threshold crossing
- allocation type/required quest set changes

### Telegram payload fields
1. grade + alert class
2. project/opportunity
3. current state
4. deadline KST
5. next action
6. Quality/Alpha/Effort/Risk
7. evidence confidence
8. top 2–4 reasons
9. risk flags
10. verified official CTA if allowed

Telegram text payload must remain <= 4096 characters; longer detail is summarized with links to evidence/dashboard.

## 11. Persistence/runtime design

### Storage choice
Phase 1 default: PostgreSQL-compatible relational database for Projects, Sources, Evidence, Opportunities, Notifications, progress/state; JSONB allowed for source-specific raw metadata.

Rationale:
- explicit state transitions and constraints
- evidence audit/history
- idempotency and unique indexes
- future analytics without premature event-stream infrastructure

Local/dev: SQLite may implement the same repository interfaces for fixtures/dry runs, but production semantics are PostgreSQL.

### Raw evidence retention
Store normalized metadata + hashes/references by default. Do not indiscriminately archive copyrighted/full social content. Retain only what is permitted/needed for audit and fixture use.

### Scheduler/worker
- source adapters expose `poll(cursor)` or event-consumer interface.
- central scheduler selects due adapters based on per-source cadence/health.
- normalization/verification/scoring are idempotent workers.
- notification outbox pattern sends Telegram after transaction commit.

### Idempotency
Unique constraints on `(source_id, source_native_id, content_hash)` where available; deterministic fallback hash for page-based sources.

### Retry/backoff
- transient 5xx/network: exponential backoff + jitter, capped retries.
- 429: honor reset/retry headers; source enters DEGRADED.
- 401/403: no blind retry loop; mark AUTH_REQUIRED/PERMISSION_REQUIRED.
- schema parse error: quarantine raw event; no user alert.

### Source degradation
One source failure must not stop pipeline. Candidate confidence reflects missing verification source. Critical T1/T2 blind spot may suppress action alerts rather than fail open.

### Cost budget
Every adapter records requests, returned records, estimated/actual cost when available. Hard daily/monthly budget caps are configurable. Paid source hitting budget -> DEGRADED, not surprise overspend.

## 12. Security design

### Secret inventory
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID (not secret like token but configuration)
- X credentials/API project keys
- DUNE_API_KEY
- GALXE_ACCESS_TOKEN
- OPENSEA_API_KEY
- optional PREMINT/Guild/Discord credentials
- RPC/indexer keys

All secrets via environment/GitHub Secrets/secret manager. Never persist in evidence/log payloads.

### Link safety gate
Before CTA:
1. normalize URL and punycode host;
2. reject unsupported schemes/userinfo/obvious redirect abuse;
3. compare host/path relation to verified official evidence;
4. re-resolve current official link close to action time;
5. label external platform clearly;
6. if link changed unexpectedly, send WARNING and suppress CTA until reverification.

### Financial/safety gate
No feature may accept private key/seed/signature payloads. No transaction construction is required for Phase 1–4 user assistant scope even if third-party APIs expose such endpoints.

## 13. Observability

Structured log fields:
`timestamp, correlation_id, source_id, adapter, event_id, project_id, opportunity_id, stage, result, error_code, latency_ms, retry_count, records, cost_units, notification_id`.

Health indicators:
- last successful fetch per source
- detection latency
- normalization error rate
- verification conflict rate
- duplicate suppression count
- action alert precision feedback
- Telegram delivery success
- source cost/lead-time ROI

Manual controls:
- disable source
- disable project
- suppress opportunity
- revoke verified link
- force recheck
- mute notification class

## 14. Data retention
- Evidence metadata: long-lived/auditable unless legal/source-policy requires deletion.
- Raw fetched body: shortest practical TTL; default 30 days if permitted, otherwise hash/reference only.
- Operational logs: default 30 days.
- Notification history: 180 days minimum for dedup/regression analysis.
- UserProgress: retained until user clears project/account data.

## 15. MVP technical choices to validate, not assume
The following decisions are architecturally isolated behind adapters and therefore may change after spikes without domain redesign:
- X stream vs recent-search/polling mix
- PREMINT partner API vs permitted page/manual ingest
- Guild access mechanism
- Dune fresh-execute cadence
- Discord announcement/role read feasibility
- exact RPC/indexer provider
- deployment scheduler: GitHub Actions vs long-running worker/serverless scheduler

See `SPIKE_PLAN.md`.
