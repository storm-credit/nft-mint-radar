# Harness Typed Schemas

## Purpose
Machine-checkable logical contracts for agent inputs/outputs. Implementation may use JSON Schema/Pydantic/TypeScript, but field names/semantics below are authoritative until versioned.

## Common envelope
```yaml
AgentEnvelope:
  schema_version: "1.0"
  correlation_id: string
  run_id: string
  agent: string
  observed_at: datetime_utc
  input_refs: [string]
  assumptions: [string]
  warnings: [string]
```

## Confidence / evidence enums
```yaml
Confidence: LOW|MEDIUM|HIGH
VerificationState: UNVERIFIED|CORROBORATED|OFFICIAL|CONFLICTED|REVOKED|STALE
ActionClass: WATCH|APPLY_WL|PREPARE|MINT_RECHECK|AVOID|NO_ALERT
```

## Discovery Agent
### Input
```yaml
DiscoveryInput:
  envelope: AgentEnvelope
  raw_event: RawEvent
  known_project_candidates: [ProjectRef]
```
### Output
```yaml
DiscoveryOutput:
  envelope: AgentEnvelope
  disposition: CANDIDATE|IGNORE|DUPLICATE|NEEDS_IDENTITY_RESOLUTION
  project_candidate:
    name: string|null
    project_id: string|null
    confidence: Confidence
  candidate_types: [PROJECT_SIGNAL|ALLOWLIST|MINT|AIRDROP|WALLET_SIGNAL|RISK_SIGNAL|OTHER]
  extracted_links: [string]
  extracted_claims: [NormalizedClaim]
  discovery_reason: [string]
  required_verification: [string]
```
Forbidden:
- verified CTA from T3/T4 only;
- investment/profit guarantee language.

## Verification Agent
### Input
```yaml
VerificationInput:
  envelope: AgentEnvelope
  project: Project|null
  claims: [NormalizedClaim]
  evidence: [Evidence]
  links: [VerifiedLink]
```
### Output
```yaml
VerificationOutput:
  envelope: AgentEnvelope
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
  hard_blocks: [UNVERIFIED_LINK|IDENTITY_UNCERTAIN|CONFLICTING_OFFICIAL_SOURCES|PHISHING_SUSPECTED|NONE]
  recheck_at: datetime_utc|null
```

## Entity Resolution Agent
### Input
```yaml
EntityResolutionInput:
  envelope: AgentEnvelope
  candidate_name: string
  links: [string]
  contract_addresses: [string]
  candidate_projects: [Project]
  evidence: [Evidence]
```
### Output
```yaml
EntityResolutionOutput:
  envelope: AgentEnvelope
  decision: MATCH_EXISTING|CREATE_NEW|SPLIT_REQUIRED|UNRESOLVED
  project_id: string|null
  confidence: Confidence
  matching_evidence_ids: [string]
  rejected_matches:
    - project_id: string
      reason: string
```

## Opportunity State Agent
### Input
```yaml
OpportunityStateInput:
  envelope: AgentEnvelope
  opportunity: Opportunity|null
  verified_claims: [VerifiedClaim]
  current_time: datetime_utc
```
### Output
```yaml
OpportunityStateOutput:
  envelope: AgentEnvelope
  previous_state: string|null
  proposed_state: string
  transition: ACCEPT|REJECT|NO_CHANGE|CORRECTION
  changed_fields: [string]
  evidence_ids: [string]
  error_code: string|null
  reason: string
```

## Scoring Agent
### Input
```yaml
ScoringInput:
  envelope: AgentEnvelope
  project: Project
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
  envelope: AgentEnvelope
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

## Wallet Intelligence Agent
### Input
```yaml
WalletIntelInput:
  envelope: AgentEnvelope
  wallet_events: [WalletEvent]
  wallet_entities: [WalletEntity]
  benchmark_context: object|null
```
### Output
```yaml
WalletIntelOutput:
  envelope: AgentEnvelope
  signals:
    - wallet_entity_id: string
      project_id: string|null
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

## Quest Parser Agent
### Input
```yaml
QuestParserInput:
  envelope: AgentEnvelope
  opportunity: Opportunity
  source_texts: [SourceText]
  structured_campaign_payloads: [object]
```
### Output
```yaml
QuestParserOutput:
  envelope: AgentEnvelope
  allocation_type: FCFS|RAFFLE|GUARANTEED|HOLDER|PUBLIC|UNKNOWN
  quests: [Quest]
  registration_open_at: datetime_utc|null
  registration_close_at: datetime_utc|null
  unresolved_requirements: [string]
  manual_actions_required: boolean
  wallet_signature_or_transaction_possible: boolean
  forbidden_auto_actions: [string]
```

## User Progress Agent
### Input
```yaml
UserProgressInput:
  envelope: AgentEnvelope
  opportunity: Opportunity
  quests: [Quest]
  external_verification_results: [object]
  prior_progress: [UserProgress]
```
### Output
```yaml
UserProgressOutput:
  envelope: AgentEnvelope
  progress: [UserProgress]
  eligibility: UNKNOWN|NOT_READY|READY_TO_REGISTER|REGISTERED|WON|WAITLISTED|LOST|READY_TO_MINT
  missing_required_tasks: [string]
  next_manual_action: string|null
```

## Decision Agent
### Input
```yaml
DecisionInput:
  envelope: AgentEnvelope
  project: Project
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
  envelope: AgentEnvelope
  action: ActionClass
  severity: INFO|WATCH|ACTION|URGENT|WARNING
  should_notify: boolean
  urgency_reason: string|null
  next_user_action: string|null
  missing_information: [string]
  material_change_keys: [string]
  cta_link: VerifiedLink|null
  recheck_at: datetime_utc|null
  reasons: [string]
```
Hard rules:
- `cta_link` must be null if not OFFICIAL/CORROBORATED according to claim class.
- Risk >=70 => action cannot be APPLY_WL/PREPARE/MINT_RECHECK.
- LOW evidence => action cannot exceed WATCH.

## Telegram Renderer
### Input
```yaml
TelegramRenderInput:
  envelope: AgentEnvelope
  project: Project
  opportunity: Opportunity|null
  scoring: ScoringOutput
  decision: DecisionOutput
  top_evidence: [Evidence]
```
### Output
```yaml
TelegramRenderOutput:
  envelope: AgentEnvelope
  text: string              # <=4096 chars
  parse_mode: string|null
  fingerprint: string
  contains_cta: boolean
  cta_verification_state: OFFICIAL|CORROBORATED|NONE
```
Forbidden:
- unverified URLs rendered as action CTA;
- secrets/raw auth tokens;
- automatic transaction/signature instructions represented as completed actions.

## Validation Result
Every feature/spike/eval reports:
```yaml
ValidationResult:
  schema_version: "1.0"
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

## Error taxonomy v1
- SOURCE_UNAVAILABLE
- AUTH_REQUIRED
- PERMISSION_REQUIRED
- RATE_LIMITED
- STALE_EVIDENCE
- IDENTITY_UNCERTAIN
- CONFLICTING_OFFICIAL_SOURCES
- UNVERIFIED_LINK
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
