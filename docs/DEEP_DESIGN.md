# Deep Design v1.1

## 0. Readiness and authority
This document is the canonical domain/runtime design contract for the current pre-production phase.

Accepted decisions incorporated here:
- ADR-007 — Phase 1 chain scope and OpenSea role.
- ADR-008 — MintCampaign/MintStage, asset-aware pricing, legacy reactivation, CTA safety separation.
- ADR-009 — Minimum-action deterministic-first orchestration.

Production feature code remains blocked until `PRODUCTION_CODING_START_GATE.md` passes.

---

# 1. Product contract

## Primary user
A single NFT participant who wants to discover credible allowlist/mint opportunities early enough to act while minimizing wasted social/Discord work, bad mints, and phishing risk.

## Primary job-to-be-done
`Find -> verify -> prioritize -> tell me exactly what matters next.`

The product answers:
1. What opportunity appeared?
2. Is the project/source/CTA credible right now?
3. Is it early enough to act?
4. Which exact campaign/stage is relevant?
5. What must the user do now/later?
6. What time/cost/risk is involved?
7. What changed since the previous alert?

## Phase 1 success conditions
- configured sources normalize into canonical events/evidence;
- T3/T4 discovery signals cannot become actionable facts without corroboration;
- project/source identity trust is separated from wallet-impacting CTA safety;
- S/A alerts show evidence confidence, KST deadline, next action, and stage-specific terms when known;
- multi-stage GTD/FCFS/holder/community/public structures remain distinct;
- FREE, known asset price, unknown price, and variable price remain distinct;
- duplicate/repeated signals do not create duplicate alerts;
- material correction/cancellation/risk changes can re-alert;
- no wallet signature, approval, transaction, social engagement, Discord self-bot, or fake referral path exists.

## Phase 1 source scope

### P0 runtime-capable
- official websites/docs from verified project identity;
- official X when API/access budget permits, degradable if unavailable;
- OpenSea drop/detail/stage APIs;
- Galxe Quest API for known/discovered quests where access is available;
- public EVM on-chain evidence through chain explorer/RPC/indexer adapter.

### P1 optional
- PREMINT Connect when partner/API access exists; otherwise official registration reference/manual permitted ingest;
- Guild supported public/API surface if available;
- Dune latest-query/parameterized results;
- official Telegram announcement channels when permitted.

### weak discovery only
- Reddit;
- public Telegram alpha groups;
- generic X accounts;
- influencer/collector chatter.

## Phase 1 chain scope
EVM-first:
1. Ethereum
2. Base
3. Robinhood Chain

Persist normalized chain identity, not display text only.

```yaml
ChainIdentity:
  chain_key: string
  eip155_chain_id: integer|null
  display_name: string
  native_symbol: string|null
```

No Solana/Bitcoin/non-EVM expansion in Phase 1 without a new ADR.

## OpenSea role
OpenSea is:
- strong structured discovery for listed drops;
- strong structured verification support for stage/price/schedule when project identity is corroborated;
- **not** complete global discovery coverage.

Missing from OpenSea never means the project/mint does not exist.

## Explicit non-goals
- auto minting;
- wallet signing/approval;
- private-key/seed handling;
- automated X follow/like/repost/comment/tag;
- automated Discord chat/activity/referral farming;
- guaranteed profit/return prediction;
- universal chain/marketplace coverage in Phase 1.

---

# 2. Canonical schemas
Implementation may use Pydantic/JSON Schema/TypeScript, but field semantics below remain stable unless versioned/changed by ADR.

## 2.1 Project
```yaml
Project:
  id: string
  canonical_name: string
  aliases: [string]
  chains: [ChainIdentity]
  official_links:
    website: [VerifiedLink]
    x: [VerifiedLink]
    discord: [VerifiedLink]
    telegram: [VerifiedLink]
    docs: [VerifiedLink]
    opensea: [VerifiedLink]
  contracts: [ContractIdentity]
  status: DISCOVERED|ACTIVE|DORMANT|REACTIVATED|ENDED|SUSPECT|BLOCKED
  created_at: datetime_utc
  updated_at: datetime_utc
```

## 2.2 Source
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

## 2.3 Evidence
```yaml
Evidence:
  id: string
  project_id: string|null
  campaign_id: string|null
  stage_id: string|null
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

Evidence is append-only. Corrections append new Evidence and retain prior history.

## 2.4 AssetAmount
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

USD estimate is contextual evidence, not canonical payment amount.

## 2.5 MintCampaign
```yaml
MintCampaign:
  id: string
  project_id: string
  chain_key: string
  contract_address: string|null
  supply: integer|null
  source_campaign_id: string|null
  state: DISCOVERED|SCHEDULED|ACTIVE|ENDED|CANCELLED|UNKNOWN
  created_at: datetime_utc
  updated_at: datetime_utc
```

## 2.6 MintStage
```yaml
MintStage:
  id: string
  campaign_id: string
  label: string|null
  stage_type: ALLOWLIST|HOLDER|COMMUNITY|FCFS|RAFFLE|PUBLIC|TEAM|OTHER
  allocation_type: FCFS|RAFFLE|GUARANTEED|HOLDER|PUBLIC|UNKNOWN
  state: PENDING|OPEN|CLOSED|CANCELLED|UNKNOWN
  open_at: datetime_utc|null
  close_at: datetime_utc|null
  price_state: FREE|KNOWN|UNKNOWN|VARIABLE
  price: AssetAmount|null
  max_per_wallet: integer|null
  eligibility_ref: string|null
  official_action_url: VerifiedLink|null
  evidence_ids: [string]
  evidence_confidence: LOW|MEDIUM|HIGH
```

Rules:
- FREE is explicitly sourced, never inferred from missing price;
- UNKNOWN is not numeric zero;
- stage-specific time/price/max values never get collapsed to campaign-wide values when they differ.

## 2.7 Opportunity
`Opportunity` is the action/prioritization object, not the container for every mint-stage fact.

```yaml
Opportunity:
  id: string
  project_id: string
  type: ALLOWLIST|RAFFLE|HOLDER_MINT|FREE_MINT|PAID_MINT|PUBLIC_MINT|AIRDROP|LEGACY_HOLDER_ACCESS|OTHER
  state: RUMORED|DISCOVERED|REGISTRATION_PENDING|REGISTRATION_OPEN|REGISTRATION_CLOSED|RESULTS_PENDING|MINT_SCHEDULED|MINT_OPEN|ENDED|CANCELLED|EXPIRED
  campaign_id: string|null
  stage_id: string|null
  registration_open_at: datetime_utc|null
  registration_close_at: datetime_utc|null
  snapshot_at: datetime_utc|null
  results_at: datetime_utc|null
  official_action_url: VerifiedLink|null
  evidence_ids: [string]
  evidence_confidence: LOW|MEDIUM|HIGH
  updated_at: datetime_utc
```

Mint-stage open/close/price/max-per-wallet live in `MintStage`; do not duplicate them into Opportunity.

## 2.8 Quest
```yaml
Quest:
  id: string
  opportunity_id: string
  campaign_id: string|null
  stage_id: string|null
  action_type: FOLLOW_X|LIKE_X|REPOST_X|COMMENT_X|TAG_FRIEND|JOIN_DISCORD|DISCORD_ROLE|DISCORD_LEVEL|GALXE|GUILD|PREMINT_REGISTER|HOLD_NFT|HOLD_TOKEN|ONCHAIN_ACTION|REFERRAL|CUSTOM
  required: boolean|null
  execution_mode: MANUAL|EXTERNAL_PLATFORM|READ_ONLY_VERIFY
  target: string|null
  quantity_or_threshold: string|null
  deadline_at: datetime_utc|null
  verification_source_id: string|null
  safety_class: SAFE_MANUAL|WALLET_SIGNATURE_REQUIRED|SOCIAL_ACTION|DISCORD_ACTIVITY|UNKNOWN
```

## 2.9 UserProgress
```yaml
UserProgress:
  user_key: string
  opportunity_id: string
  quest_id: string|null
  state: UNKNOWN|TODO|IN_PROGRESS|COMPLETED|VERIFIED|WON|WAITLISTED|LOST|EXPIRED|SKIPPED
  provenance: USER_CONFIRMED|PROVIDER_VERIFIED|SYSTEM_OBSERVED|UNKNOWN
  observed_at: datetime_utc
  verification_source_id: string|null
  note: string|null
```

Recommendation/planned work never auto-promotes to COMPLETED.

## 2.10 WalletEntity
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

## 2.11 InfluencerEntity
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

## 2.12 Notification
```yaml
Notification:
  id: string
  fingerprint: string
  project_id: string
  campaign_id: string|null
  stage_id: string|null
  opportunity_id: string|null
  class: DISCOVERY|WL_OPEN|DEADLINE|COHORT_HIT|CONTRACT_LINKED|RISK_DOWNGRADE|WL_RESULT|MINT_RECHECK|REACTIVATION
  severity: INFO|WATCH|ACTION|URGENT|WARNING
  action: WATCH|APPLY_WL|PREPARE|MINT_RECHECK|AVOID|NO_ALERT
  material_change_keys: [string]
  rendered_payload_hash: string
  delivery_state: PENDING|CLAIMED|SENT|AMBIGUOUS|FAILED|ABANDONED
  attempt_count: integer
  next_attempt_at: datetime_utc|null
  claimed_until: datetime_utc|null
  provider_message_id: string|null
  last_error: string|null
  sent_at: datetime_utc|null
```

A null `sent_at` alone never authorizes a resend. A provider timeout after a possible delivery moves
the row to `AMBIGUOUS`, which is reconciled before any retry. `SPIKE-TG-001` confirmed the provider
returns an observable `message_id` on success, so `SENT` is recorded from provider evidence rather
than inferred. Telegram is not exactly-once transport; this state machine, not the provider, is what
prevents both duplicate alerts and silently lost ones.

## 2.13 VerifiedLink
```yaml
VerifiedLink:
  url: string
  normalized_host: string
  relation: OFFICIAL_SITE|OFFICIAL_SOCIAL|OFFICIAL_CAMPAIGN|OFFICIAL_MARKETPLACE|OFFICIAL_CONTRACT|OTHER
  verification_state: UNVERIFIED|CORROBORATED|OFFICIAL|REVOKED|SUSPICIOUS
  evidence_ids: [string]
  checked_at: datetime_utc
```

`VerifiedLink.verification_state` describes identity/relation evidence. Wallet-impacting action safety is separate.

Consequently `official_action_url: VerifiedLink` on `MintStage` and `Opportunity` holds
**source/identity evidence only and is never directly renderable**. The only renderable
wallet-impacting URL is one carried by an `ActionLinkAssessment` whose `safety_state = CONSISTENT`.
Decision and notification payloads carry that assessment or its id, never the raw `VerifiedLink`.
This keeps the CTA gate in the schema rather than only in prose, so an implementation cannot reach a
renderable action URL without passing through the assessment.

## 2.14 ActionLinkAssessment
```yaml
ActionLinkAssessment:
  url: string
  safety_state: UNVERIFIED|CONSISTENT|QUARANTINED|REVOKED
  checked_at: datetime_utc
  project_id: string
  campaign_id: string|null
  stage_id: string|null
  contract_address: string|null
  evidence_ids: [string]
  reason: string|null
```

A T1 post does not automatically make a new CTA `CONSISTENT`.

---

# 3. Project identity and merge/split

Merge only with a strong relation such as:
- same officially linked contract/deployer relation;
- official site directly linking identities;
- official rebrand/migration announcement linking old/new identity.

Never merge solely because:
- names/logos resemble each other;
- influencer/community claims relation;
- wallet overlap exists.

Split/quarantine when:
- official channels disavow clone/migration;
- team/contract relation cannot be corroborated;
- compromised domain/account behavior is detected.

Identity history/aliases/evidence remain auditable.

---

# 4. Event normalization

## RawEvent
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

## NormalizedEvent
```yaml
NormalizedEvent:
  id: string
  raw_event_ids: [string]
  project_candidate: string|null
  event_type: PROJECT_SIGNAL|PROJECT_REACTIVATED|CHAIN_MIGRATION_ANNOUNCED|LEGACY_HOLDER_ACCESS_ANNOUNCED|ALLOWLIST_ANNOUNCED|ALLOWLIST_OPENED|ALLOWLIST_CLOSED|QUEST_CHANGED|SNAPSHOT_ANNOUNCED|SNAPSHOT_PASSED|MINT_SCHEDULED|MINT_OPENED|MINT_ENDED|CONTRACT_DEPLOYED|CONTRACT_OFFICIALLY_LINKED|RISK_SIGNAL|WALLET_SIGNAL|SOCIAL_SIGNAL|CORRECTION|CANCELLATION|OTHER
  claims: [NormalizedClaim]
  observed_at: datetime_utc
  source_time: datetime_utc|null
  confidence: LOW|MEDIUM|HIGH
```

## Time semantics
- source/published time = source assertion;
- observed/fetched time = system observation;
- store UTC, render KST;
- date without timezone lowers confidence and must be shown unresolved.

## Edit/delete
- same native id + new content hash -> CORRECTION + new Evidence;
- disappeared source -> retain Evidence + mark unavailable; do not infer revocation without correction/disavowal.

`unavailable` evidence is **not** `current` evidence. Evidence whose source has disappeared cannot
satisfy a `current T1/T2` requirement for `ACTION`/`URGENT` severity, for a stage transition, or for
any wallet-impacting CTA. The claim degrades to `WATCH` with the disappearance shown, until a current
source corroborates it again or an explicit correction/disavowal resolves it. This does not infer
revocation; it refuses to treat a vanished source as present evidence.

## Dedup
Exact key when available:
`source_id + source_native_id + content_hash`.

Cross-source notification dedup candidate:
`project_id + campaign_id + stage_id + event_type + primary_claim + time_bucket`.

Evidence is never deleted by semantic dedup.

---

# 5. Verification and CTA safety

## Discovery trust != action safety
A source can be official yet currently compromised. Therefore:
- source/project identity evidence;
- claim verification;
- wallet-impacting CTA safety;

are separate checks.

## Mint/WL/action URL
Identity/relation verification may use:
- current T1 official site/account relation;
- T2 campaign/marketplace page linked/corroborated to project;
- current known official domain history.

For wallet-impacting CTA (`APPLY_WL`, `MINT_RECHECK`, connect/mint/register URL):
- require `ActionLinkAssessment.safety_state=CONSISTENT`;
- unexpected host/contract changes -> QUARANTINED;
- disavowed/malicious link -> REVOKED;
- T3/T4 URL never becomes CTA by itself.

## Contract address
`OFFICIAL` only when current official/corroborated project evidence links the contract/marketplace relation and T0 confirms the address exists on expected chain.

## Date/deadline
One current T1/T2 source can make a date actionable when no conflict exists.
If current official sources conflict -> CONFLICTED; exact urgent CTA is suppressed until resolved.

### Single-source limit on urgency escalation
Conflict detection does not cover **silence**. A compromised official account can post a false
deadline that no other source contradicts, because the canonical surface is merely quiet. Therefore:

- one current T1/T2 source may make a date actionable at `WATCH`/`ACTION` level, which preserves the
  lead time this product exists to deliver;
- but a **newly appeared or shortened** deadline, or a stage transition to `OPEN`, that rests on a
  single **account-based** official source (X/Telegram/Discord post) must not by itself produce
  `URGENT` severity or a wallet-impacting CTA;
- escalation requires one of: a second independent official surface (site/docs/marketplace), on-chain
  evidence, or the same claim present on the canonical official surface;
- until then the alert is rendered as single-source and unconfirmed, with the CTA suppressed.

This is a deterministic gate, not a scoring nudge.

## Holder/snapshot
Requires current T1/T2 eligibility claim + collection/identity relation.
Past snapshot is explicit. Buying after snapshot is never assumed to qualify.

## Confidence
- HIGH: current T0/T1/T2 evidence, identity linked, no material conflict;
- MEDIUM: corroborated but incomplete/time/identity detail unresolved;
- LOW: discovery-only, stale, inferred, or conflicting.

## Freshness defaults
- action URL: recheck before every ACTION/URGENT and within 15 minutes of wallet-impacting CTA;
- deadline: within 60m at D-1, within 15m under 2h;
- contract linkage: recheck before MINT_RECHECK;
- project identity links: 7-day soft TTL, immediate on risk/conflict;
- wallet labels: 30-day soft TTL unless first-party mapping persists.

---

# 6. State models

## MintCampaign
Typical:
`DISCOVERED -> SCHEDULED -> ACTIVE -> ENDED`

Any active/pre-ended -> CANCELLED with sufficient current evidence.

## MintStage
Typical:
`PENDING -> OPEN -> CLOSED`

Rules:
- stage never becomes OPEN solely because local clock passed `open_at`; require current platform/official/on-chain evidence;
- correction can update schedule/terms while retaining prior Evidence;
- stage-specific fields stay stage-specific.

## Opportunity
Canonical action flow:
`RUMORED -> DISCOVERED -> REGISTRATION_PENDING -> REGISTRATION_OPEN -> REGISTRATION_CLOSED -> RESULTS_PENDING -> MINT_SCHEDULED -> MINT_OPEN -> ENDED`

Alternative holder/direct flows can skip registration states.

`CANCELLED` is reachable from **every** pre-`ENDED` state on current official cancellation evidence.
`EXPIRED` is reachable from every actionable state when the deadline passes with no result evidence.
Neither is an illegal transition, and neither may be rejected for skipping intermediate states.
Entering `CANCELLED` revokes any outstanding CTA and stops routine reminders for that opportunity.

Without this, `F18 — Official cancellation` cannot be satisfied: a cancellation would either be
rejected as an illegal transition or written as an uncontracted value, leaving a stale actionable
opportunity alive.

User-specific `WON|WAITLISTED|LOST` lives in UserProgress, not global Opportunity state.

Illegal transition -> `STATE_TRANSITION_REJECTED` + evidence retained.

---

# 7. Scoring model v1
Scores prioritize attention; they are not return forecasts.

## Quality 0–100
- team/project provenance 0–20
- existing community/history 0–20
- product/art/cultural differentiation 0–15
- transparent mint mechanics 0–15
- organic demand evidence 0–15
- ecosystem/partner credibility 0–10
- execution history 0–5

## Alpha 0–100
- lead time before public mint 0–25
- low saturation/early signal 0–20
- WL still obtainable 0–20
- independent wallet cohort 0–20
- unique-source lead advantage 0–15

## Effort 0–100 — lower better
- simple register/follow +5..15
- multiple social actions +10..25
- Discord role/level over days +20..50
- referral dependency +20..40
- paid on-chain action +20..50
- uncertain/mod-selected criteria +20

## Risk 0–100 — lower better
Typical penalties:
- unverified official relation +30
- contract/site mismatch +40
- suspicious domain/homograph +40
- CTA QUARANTINED +40 minimum and action suppression
- conflicting official instructions +25
- anonymous/new team no history +10
- concentrated supply/team allocation +10..25
- wash/sybil-like activity +10..30
- promotion/shill conflict +5..20
- high stage price relative to evidence +5..20
- wallet-drainer/signature anomaly +100 hard block

## Evidence adjustment
- HIGH x1.00
- MEDIUM x0.85
- LOW cannot exceed WATCH/B behavior regardless of raw score

## Wallet cohort
- one famous wallet: +0..3 Alpha only
- 2 independent validated alpha wallets: +3..7 Alpha
- 3+ independent high-score wallets: +5..15 Alpha
- correlated/sybil cluster: no bonus; may add Risk

## Influencer cap
Social/influencer mention: max +5 Alpha, +0 Quality unless supported independently.

## Action score
```text
base = 0.35*Quality + 0.35*Alpha + 0.20*(100-Risk) + 0.10*(100-Effort)
action_score = base * evidence_multiplier
```

Hard gates override score:
- CTA not CONSISTENT -> no wallet-impacting APPLY/MINT CTA;
- Risk >=70 -> AVOID/WATCH only;
- LOW evidence -> WATCH only.

Grades:
- S >=88 + HIGH evidence + Risk<30
- A >=78 + evidence>=MEDIUM + Risk<45
- B 65–77
- C 50–64
- D/AVOID <50 or hard block

Weights are provisional until fixture regression/historical calibration. Material changes require version bump/ADR.

---

# 8. Wallet / Dune intelligence

## Seed policy
Public wallet seed only with first-party/strongly corroborated mapping. Named collector wallets are discovery seeds, not endorsements.

## AlphaWalletScore concept
```text
35% repeated early-entry percentile on later-successful collections
20% independent project diversity
15% holding/persistence quality
15% realized outcome proxy where measurable
15% recency
minus wash/sybil/conflict penalties
```

Do not productionize until benchmark definitions/spike validation are fixed.

## Independence
Not independent with strong evidence of:
- common funder at short distance;
- repeated direct transfers;
- team/deployer-controlled cluster;
- synchronized sybil/automation patterns.

Factory/deployer infrastructure must not be mistaken for project team attribution without corroboration.

## Backtest safety
Avoid survivorship/look-ahead bias:
- benchmark cohort must be defined without using future success labels inside the entry-time features;
- keep training/calibration and evaluation periods separate when production calibration starts.

## Dune use
Cached/latest results preferred for frequent reads; fresh execution at bounded refresh windows. Core pipeline continues when Dune unavailable.

---

# 9. Phase 2 WL / Quest / progress

## Allocation semantics
- FCFS: speed-sensitive;
- RAFFLE: deadline/results/winner count when known;
- GUARANTEED: explicit eligibility required;
- HOLDER: collection/token + snapshot semantics;
- PUBLIC: no allowlist eligibility assumption.

## Mandatory vs optional
`required` can be null/unknown if source wording is ambiguous. Unknown blocks `all_requirements_complete`.

## Manual execution
Social actions, CAPTCHA, wallet connection/signing, Discord activity, invites/referrals are user-performed only.

## Progress provenance
UserProgress must distinguish:
- user-confirmed;
- provider-verified;
- system-observed;
- unknown.

A reminder/recommendation never counts as completion.

---

# 10. Notification design

## Severity
- INFO
- WATCH
- ACTION
- URGENT
- WARNING

## Alert triggers
- first S/A candidate crossing evidence gate;
- WL/quest opens;
- material requirement/deadline/stage change;
- validated wallet cohort crosses threshold;
- official contract relation appears;
- risk worsens >=15 or crosses hard threshold;
- user-specific WL result;
- mint window enters final recheck;
- legacy project reactivation / chain migration / holder-access signal when actionable/important.

## No-alert
Suppress:
- repeated same evidence;
- T3/T4 rumor without corroboration;
- score delta <5 without action/state change;
- routine source-health noise unless coverage becomes critically blind.

## Fingerprint
`project_id | campaign_id | stage_id | opportunity_id | notification_class | normalized_action | deadline_bucket | material_version`

Bucket and version semantics are deterministic and shared by every code path that builds a fingerprint:
- `deadline_bucket` and `time_bucket` are derived from the **canonical claim time in UTC**, never from
  observation/fetch time, so two sources reporting the same deadline collapse to one fingerprint;
- both bucket to a fixed grid; a claim time exactly on a boundary rounds down;
- `material_version` starts at 1 per fingerprint identity and increments **only** when a key listed
  under `Material re-alert` actually changes;
- new Evidence that changes no material key (for example a `CORRECTION` with identical claims) does
  not increment `material_version` and therefore does not re-alert.

## Material re-alert
Re-alert on:
- state change;
- deadline move >=15m under D-1 or >=2h otherwise;
- stage price/supply/max changes;
- action URL/contract change;
- CTA safety change;
- risk +/-15 or threshold crossing;
- allocation/required quest change.

## Telegram payload
When known:
1. grade/alert class
2. project
3. campaign/stage
4. current state
5. KST deadline
6. next user action
7. Quality/Alpha/Effort/Risk
8. evidence confidence
9. top reasons
10. risk flags
11. only CONSISTENT wallet-impacting CTA

Telegram text <=4096 chars; longer evidence stays in referenced detail/dashboard.

---

# 11. Persistence and runtime

## Storage
Production: PostgreSQL for Project, Source, Evidence, MintCampaign, MintStage, Opportunity, Notification, UserProgress and audit state; JSONB only for source-specific raw metadata where appropriate.

Local fixture/dry-run may use SQLite behind same repository interfaces.

## Raw evidence
Store normalized metadata + hashes/refs by default; do not indiscriminately archive full copyrighted/social content.

## Deterministic-first pipeline
```text
Source adapters
 -> normalization
 -> evidence/verification rules
 -> campaign/stage state
 -> scoring formula/hard gates
 -> decision rules
 -> transactional outbox
 -> Telegram renderer/sender
```

No central LLM selects among these services.

Conditional model-driven nodes are defined/audited in `LOCAL_ACTION_SPACE_AUDIT.md`.

## Idempotency
Unique `(source_id, source_native_id, content_hash)` where possible; deterministic fallback hash for page-like sources.

## Retry/backoff
- transient network/5xx: exponential backoff+jitter with cap;
- 429: honor retry/reset; source -> DEGRADED;
- 401/403: no blind loop; AUTH/PERMISSION state;
- parse failure: quarantine event; no user alert.

## Degradation
One source failure must not stop the whole pipeline. Missing critical verification can suppress ACTION rather than fail open.

## Cost
Per-adapter request/record/actual-estimated cost accounting. Hard daily/monthly caps are configuration/runtime guarantees. Budget hit -> DEGRADED, not surprise overspend.

---

# 12. Security

## Secrets
Examples:
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID config
- X credentials
- DUNE_API_KEY
- GALXE_ACCESS_TOKEN
- OPENSEA_API_KEY
- optional PREMINT/Guild/Discord credentials
- RPC/indexer keys

Secrets only through runtime/environment/GitHub Secrets/secret manager; never evidence/logs.

## CTA safety gate
Before wallet-impacting CTA:
1. normalize URL/punycode host;
2. reject bad scheme/userinfo/obvious redirect abuse;
3. compare current host/path to verified project relations;
4. cross-check current official site/platform/contract/on-chain consistency as required;
5. classify ActionLinkAssessment;
6. unexpected new host/contract -> QUARANTINED;
7. only CONSISTENT may render as wallet-impacting CTA.

## Financial boundary
No feature accepts private key/seed/signature payload. No transaction construction is needed for product scope.

---

# 13. Observability

Structured fields:
`timestamp, correlation_id, source_id, adapter, event_id, project_id, campaign_id, stage_id, opportunity_id, pipeline_stage, result, error_code, latency_ms, retry_count, records, cost_units, notification_id`.

Health:
- last successful fetch/source;
- detection latency;
- normalize error rate;
- verification conflicts;
- CTA quarantine/revocation count;
- duplicate suppression;
- alert precision feedback;
- Telegram delivery;
- source cost/lead-time ROI.

Manual controls:
- disable source/project;
- suppress opportunity/campaign/stage;
- revoke link;
- quarantine CTA;
- force recheck;
- mute notification class.

---

# 14. Retention
- Evidence metadata: auditable/long-lived unless policy/legal requires removal.
- Raw fetched body: shortest practical TTL; default 30d only when permitted, otherwise hash/reference.
- Operational logs: default 30d.
- Notification history: >=180d for dedup/regression.
- UserProgress: until user clears relevant data.

---

# 15. Remaining technical decisions are spike-driven
Architecturally isolated and not assumed:
- X stream vs search/polling and cost;
- OpenSea live coverage across Ethereum/Base/Robinhood;
- PREMINT partner API vs permitted fallback;
- Guild access mechanism;
- Dune fresh execution cadence/cost;
- Discord authorized announcement/role read feasibility;
- exact RPC/indexer provider;
- provider/runtime outbound behavior at deployment.

See `SPIKE_PLAN.md` and current `PROJECT_STATUS.md` for what still blocks Phase 1 coding.
