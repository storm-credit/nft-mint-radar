# Harness Credential-Free Dry Run

## Purpose
Demonstrate that the design contracts can carry one event end-to-end without production credentials. This is a design-level dry run, not proof that provider adapters work.

## Scenario DR-001 — phishing reply on an official project post
Derived from fixture F05.

### H0 Context
- Phase: pre-implementation design/spike stage
- Production writes: blocked
- Safety rule: T3/T4 cannot establish mint CTA

### RawEvent
```yaml
event_id: raw-001
source_id: x-unverified-reply-account
source_native_id: "reply-123"
fetched_at: 2026-08-15T08:00:00Z
published_at: 2026-08-15T07:59:30Z
event_kind: POST
canonical_url: https://x.example/reply-123
author_identity: TheSaud1sNFT
text: "MINT LIVE NOW https://thesaudis-m1nt.example"
content_hash: sha256:example
```

### DiscoveryOutput
```yaml
disposition: CANDIDATE
project_candidate:
  name: The Saudis
  project_id: known-project-001
  confidence: LOW
candidate_types: [MINT, RISK_SIGNAL]
extracted_links:
  - https://thesaudis-m1nt.example
required_verification:
  - author identity
  - official link relationship
```

### VerificationInput context
Known Project official links do not contain the reply handle/domain. Official site and official X contain no mint-live claim.

### VerificationOutput
```yaml
claims:
  - claim_key: mint_open
    normalized_value: true
    state: UNVERIFIED
    confidence: LOW
    supporting_evidence_ids: [ev-reply]
    conflicting_evidence_ids: []
verified_links:
  - url: https://thesaudis-m1nt.example
    verification_state: SUSPICIOUS
hard_blocks: [UNVERIFIED_LINK, PHISHING_SUSPECTED]
```

### ScoringOutput
```yaml
quality_score: 80
alpha_score: 70
effort_score: 10
risk_score: 95
evidence_confidence: LOW
action_score: 0
grade: D
hard_gate: AVOID
```
Risk/hard gate overrides any existing positive Project score.

### DecisionOutput
```yaml
action: AVOID
severity: WARNING
should_notify: true
next_user_action: "공식 사이트/X에서 민트 공지를 다시 확인하고 이 링크는 사용하지 않기"
material_change_keys: [risk, suspicious_link]
cta_link: null
```

### TelegramRenderOutput
```text
⚠️ The Saudis — 비공식 민트 링크 경고

공식 채널에서 확인되지 않은 민트 링크가 발견됐습니다.
현재 링크는 사용하지 마세요.

Risk 95/100 · Evidence LOW
다음 행동: 공식 사이트/X에서 민트 공지 재확인
```

### Assertions
- PASS: no suspicious URL appears as CTA.
- PASS: famous/project historical Quality cannot override phishing hard gate.
- PASS: no transaction/signature action exists.
- PASS: warning is allowed despite normal S/A alert threshold because safety event is material.

---

## Scenario DR-002 — verified allowlist opening

### Raw inputs
- verified official X announces WL registration URL/deadline;
- official website links same X account and registration host;
- no conflicting source.

### Expected trace
1. Discovery -> `ALLOWLIST` candidate.
2. Verification -> deadline/link HIGH + OFFICIAL/CORROBORATED.
3. Opportunity -> `REGISTRATION_OPEN` if current time in window.
4. Scoring -> component scores from evidence, no unsupported assumptions.
5. Decision -> APPLY_WL only if score/risk thresholds pass.
6. Telegram -> KST deadline + manual next action + verified link.

### Key invariant
If step 2 fails, steps 5–6 automatically fall back to WATCH/no CTA. No later agent may reconstruct trust.

## Dry-run verdict
**PASS at design-contract level.**
The schemas, hard gates, decision precedence and renderer constraints are sufficient to trace an event end-to-end without provider credentials.

This does not prove:
- X API access;
- provider latency/cost;
- Telegram network delivery;
- actual parser/model accuracy.

Those remain Spike/implementation validations.
