# Harness Typed Schemas

## Purpose
Machine-checkable **logical role** contracts. A schema section does not imply a separate autonomous agent.
Implementation mechanism is governed by `HARNESS_SPEC.md`, `MINIMUM_ACTION_ADOPTION.md`, and ADR-009.

Domain types such as `Project`, `Evidence`, `Opportunity`, `MintCampaign`, `MintStage`, `AssetAmount`, `VerifiedLink`, `Quest`, and `UserProgress` come from `DEEP_DESIGN.md` plus Accepted ADRs. Do not create divergent domain copies here.

## Common envelope
```yaml
ExecutionEnvelope:
  schema_version: "1.1"
  correlation_id: string
  run_id: string
  role: string
  observed_at: datetime_utc
  input_refs: [string]
  assumptions: [string]
  warnings: [string]
```

## Shared enums
```yaml
Confidence: LOW|MEDIUM|HIGH
VerificationState: UNVERIFIED|CORROBORATED|OFFICIAL|CONFLICTED|REVOKED|STALE
CTASafetyState: UNVERIFIED|CONSISTENT|QUARANTINED|REVOKED
ActionClass: WATCH|APPLY_WL|PREPARE|MINT_RECHECK|AVOID|NO_ALERT
```

---

## Discovery Extraction
### Input
```yaml
DiscoveryInput:
  envelope: ExecutionEnvelope
  raw_event: RawEvent
  known_project_candidates: [ProjectRef]
  source_identity: SourceRef
```

### Output
```yaml
DiscoveryOutput:
  envelope: ExecutionEnvelope
  disposition: CANDIDATE|IGNORE|DUPLICATE|NEEDS_IDENTITY_RESOLUTION
  project_candidate:
    name: string|null
    project_id: string|null
    confidence: Confidence
  candidate_types:
    - PROJECT_SIGNAL
    - PROJECT_REACTIVATED
    - CHAIN_MIGRATION
    - LEGACY_HOLDER_ACCESS
    - ALLOWLIST
    - MINT
    - AIRDROP
    - WALLET_SIGNAL
    - RISK_SIGNAL
    - OTHER
  extracted_links: [string]
  extracted_claims: [NormalizedClaim]
  discovery_reason: [string]
  required_verification: [string]
```

Forbidden:
- verified CTA from T3/T4 alone;
- profit/investment guarantee;
- silently upgrading an extracted link to safe action link.

---

## Verification
### Input
```yaml
VerificationInput:
  envelope: ExecutionEnvelope
  project: Project|null
  campaign: MintCampaign|null
  stage: MintStage|null
  claims: [NormalizedClaim]
  evidence: [Evidence]
  links: [VerifiedLink]
```

### Output
```yaml
VerificationOutput:
  envelope: ExecutionEnvelope
  claims:
    - claim_key: string
      normalized_value: any
      state: VerificationState
      confidence: Confidence
      supporting_evidence_ids: [string]
      conflicting_evidence_ids: [string]
      valid_until: datetime_utc|null
      reason: string
  verified_links: [VerifiedLink]
  cta_safety:
    state: CTASafetyState
    checked_url: string|null
    checked_host: string|null
    contract_address: string|null
    evidence_ids: [string]
    reason: string|null
  hard_blocks:
    - UNVERIFIED_LINK
    - IDENTITY_UNCERTAIN
    - CONFLICTING_OFFICIAL_SOURCES
    - CTA_QUARANTINED
    - PHISHING_SUSPECTED
    - NONE
  recheck_at: datetime_utc|null
```

Hard rule: T1 source identity alone cannot set CTA safety to `CONSISTENT` when a wallet-impacting action link is new/changed.

---

## Entity Resolution
### Input
```yaml
EntityResolutionInput:
  envelope: ExecutionEnvelope
  candidate_name: string
  links: [string]
  contract_addresses: [string]
  candidate_projects: [Project]
  evidence: [Evidence]
```

### Output
```yaml
EntityResolutionOutput:
  envelope: ExecutionEnvelope
  decision: MATCH_EXISTING|CREATE_NEW|SPLIT_REQUIRED|UNRESOLVED
  project_id: string|null
  confidence: Confidence
  matching_evidence_ids: [string]
  rejected_matches:
    - project_id: string
      reason: string
```

---

## Campaign / Stage / Opportunity State
### Input
```yaml
CampaignStageStateInput:
  envelope: ExecutionEnvelope
  campaign: MintCampaign|null
  stage: MintStage|null
  opportunity: Opportunity|null
  verified_claims: [VerifiedClaim]
  current_time: datetime_utc
```

### Output
```yaml
CampaignStageStateOutput:
  envelope: ExecutionEnvelope
  campaign_state:
    previous: string|null
    proposed: string|null
  stage_state:
    previous: string|null
    proposed: string|null
  opportunity_state:
    previous: string|null
    proposed: string|null
  transition: ACCEPT|REJECT|NO_CHANGE|CORRECTION
  changed_fields: [string]
  evidence_ids: [string]
  error_code: string|null
  reason: string
```

Hard rule: stage price/time/max-per-wallet facts remain stage-specific and must not be collapsed into one campaign-wide value when they differ.

---

## Scoring
### Input
```yaml
ScoringInput:
  envelope: ExecutionEnvelope
  project: Project
  campaign: MintCampaign|null
  stage: MintStage|null
  opportunity: Opportunity|null
  verified_claims: [VerifiedClaim]
  wallet_signals: [WalletSignal]
  influencer_signals: [InfluencerSignal]
  effort_features: [EffortFeature]
  risk_features: [RiskFeature]
```

### Output
```yaml
ScoringOutput:
  envelope: ExecutionEnvelope
  score_version: "v1"
  quality_score: number_0_100
  alpha_score: number_0_100
  effort_score: number_0_100
  risk_score: number_0_100
  evidence_confidence: Confidence
  action_score: number_0_100
  grade: S|A|B|C|D
  hard_gate: NONE|WATCH_ONLY|AVOID
  components:
    - name: string
      points: number
      evidence_ids: [string]
      reason: string
  unsupported_assumptions: [string]
```

Scoring calculation and hard gates are deterministic/versioned by default.

---

## Wallet Intelligence
### Input
```yaml
WalletIntelInput:
  envelope: ExecutionEnvelope
  wallet_events: [WalletEvent]
  wallet_entities: [WalletEntity]
  benchmark_context: object|null
```

### Output
```yaml
WalletIntelOutput:
  envelope: ExecutionEnvelope
  signals:
    - wallet_entity_id: string
      project_id: string|null
      campaign_id: string|null
      stage_id: string|null
      opportunity_id: string|null
      signal_type: MINT|BUY|TRANSFER|CONTRACT_INTERACTION|COHORT_HIT|OTHER
      entry_percentile: number|null
      identity_confidence: Confidence
      independence_group: string|null
      wash_sybil_risk: number_0_100|null
      strength: WEAK|MEDIUM|STRONG
      evidence_ids: [string]
  cohort:
    independent_wallet_count: integer
    correlated_wallet_count: integer
    strength: NONE|WEAK|MEDIUM|STRONG
```

---

## Quest Parser — Phase 2
### Input
```yaml
QuestParserInput:
  envelope: ExecutionEnvelope
  project: Project
  campaign: MintCampaign|null
  stage: MintStage|null
  opportunity: Opportunity
  source_texts: [SourceText]
  structured_campaign_payloads: [object]
```

### Output
```yaml
QuestParserOutput:
  envelope: ExecutionEnvelope
  campaign_id: string|null
  stage_id: string|null
  allocation_type: FCFS|RAFFLE|GUARANTEED|HOLDER|PUBLIC|UNKNOWN
  quests: [Quest]
  registration_open_at: datetime_utc|null
  registration_close_at: datetime_utc|null
  unresolved_requirements: [string]
  manual_actions_required: boolean
  wallet_signature_or_transaction_possible: boolean
  forbidden_auto_actions: [string]
```

---

## User Progress — Phase 2+
### Input
```yaml
UserProgressInput:
  envelope: ExecutionEnvelope
  opportunity: Opportunity
  campaign: MintCampaign|null
  stage: MintStage|null
  quests: [Quest]
  external_verification_results: [object]
  prior_progress: [UserProgress]
  user_confirmed_actions: [object]
```

### Output
```yaml
UserProgressOutput:
  envelope: ExecutionEnvelope
  progress: [UserProgress]
  eligibility: UNKNOWN|NOT_READY|READY_TO_REGISTER|REGISTERED|WON|WAITLISTED|LOST|READY_TO_MINT
  missing_required_tasks: [string]
  next_manual_action: string|null
  inferred_completion_count: 0
```

Hard rule: planned/recommended work is not completion. Manual progress requires user/provider evidence.

---

## Decision
### Input
```yaml
DecisionInput:
  envelope: ExecutionEnvelope
  project: Project
  campaign: MintCampaign|null
  stage: MintStage|null
  opportunity: Opportunity|null
  scoring: ScoringOutput
  verification: VerificationOutput
  previous_notification: Notification|null
  user_progress: UserProgressOutput|null
  current_time: datetime_utc
```

### Output
```yaml
DecisionOutput:
  envelope: ExecutionEnvelope
  action: ActionClass
  severity: INFO|WATCH|ACTION|URGENT|WARNING
  should_notify: boolean
  urgency_reason: string|null
  next_user_action: string|null
  missing_information: [string]
  material_change_keys: [string]
  cta_link: VerifiedLink|null
  cta_safety_state: CTASafetyState
  recheck_at: datetime_utc|null
  reasons: [string]
```

Hard rules:
- `cta_link` must be null unless wallet-impacting CTA safety is `CONSISTENT`;
- `QUARANTINED`/`REVOKED` => no APPLY_WL/PREPARE/MINT_RECHECK CTA;
- Risk >=70 => action cannot be APPLY_WL/PREPARE/MINT_RECHECK;
- LOW evidence => action cannot exceed WATCH.

---

## Telegram Renderer
### Input
```yaml
TelegramRenderInput:
  envelope: ExecutionEnvelope
  project: Project
  campaign: MintCampaign|null
  stage: MintStage|null
  opportunity: Opportunity|null
  scoring: ScoringOutput
  decision: DecisionOutput
  top_evidence: [Evidence]
```

### Output
```yaml
TelegramRenderOutput:
  envelope: ExecutionEnvelope
  text: string
  parse_mode: string|null
  fingerprint: string
  contains_cta: boolean
  cta_safety_state: CONSISTENT|NONE
```

Forbidden:
- unverified/quarantined/revoked wallet-impacting URL as CTA;
- secrets/raw auth token;
- auto transaction/signature/social action represented as completed.

---

## Independent Critic
### Input
```yaml
CriticInput:
  envelope: ExecutionEnvelope
  artifact_ref: string
  artifact: object|string
  requirements: [string]
  constraints: [string]
  acceptance_criteria: [string]
  verification_evidence: [string]
```

Builder rationale is intentionally absent by default.

### Output
```yaml
CriticOutput:
  envelope: ExecutionEnvelope
  verdict: PASS|PATCH|CUT|BLOCK
  findings:
    - severity: P0|P1|P2
      clause_or_area: string
      issue: string
      undefined_terms: [string]
      weakest_reading: string|null
      evidence_refs: [string]
      required_change: string|null
  residual_risks: [string]
```

---

## Local Action Space Audit
```yaml
LocalActionSpaceAudit:
  node: string
  model_driven: boolean
  meaningful_peer_choices: integer
  deterministic_choices_excluded:
    - choice: string
      enforcing_mechanism: string
  open_argument_callables: [string]
  status: PASS|WAIVER_REQUIRED|SCOPE_LIMIT_REQUIRED|NOT_APPLICABLE
  record_ref: string|null
```

A generic router/shell does not reduce count when the model still chooses the underlying means.

---

## Validation Result
```yaml
ValidationResult:
  schema_version: "1.1"
  subject: string
  status: PASS|FAIL|PARTIAL|BLOCKED
  checks:
    - name: string
      expected: string
      actual: string
      status: PASS|FAIL
  errors: [string]
  residual_risks: [string]
  evidence_refs: [string]
  next_gate: string|null
```

## Error taxonomy v1.1
- SOURCE_UNAVAILABLE
- AUTH_REQUIRED
- PERMISSION_REQUIRED
- RATE_LIMITED
- STALE_EVIDENCE
- STALE_DERIVED_ARTIFACT
- IDENTITY_UNCERTAIN
- CONFLICTING_OFFICIAL_SOURCES
- UNVERIFIED_LINK
- CTA_QUARANTINED
- PHISHING_SUSPECTED
- SCHEMA_PARSE_FAILED
- DUPLICATE_EVENT
- STATE_TRANSITION_REJECTED
- COST_BUDGET_EXCEEDED
- BLOCKED_BY_DESIGN
- BLOCKED_BY_SPIKE
- SAFETY_BOUNDARY
- TELEGRAM_DELIVERY_FAILED
- PROVIDER_DEGRADED
