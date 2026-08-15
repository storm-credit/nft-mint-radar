# ADR-004 — Explainable Scoring and Safety Gates

## Status
Accepted

## Context
A single opaque NFT score would mix project quality, earliness, effort, risk and evidence quality. That creates bad incentives and can let hype override verification.

## Options considered

### A. One LLM score
Simple but opaque and unstable.

### B. Pure rules, no aggregate score
Auditable but harder to prioritize across many candidates.

### C. Component scores + explainable aggregate + hard safety gates — CHOSEN
Track Quality, Alpha, Effort and Risk separately; compute Action Score only after evidence adjustment. Safety gates override numerical score.

### D. Historical ML return predictor
Premature, likely regime-sensitive, and risks implying profit prediction.

## Decision
- Quality, Alpha, Effort and Risk remain separate 0–100 components.
- Evidence confidence caps actionability.
- Influencers cannot directly raise Quality and have a small Alpha cap.
- One famous wallet provides at most a weak Alpha adjustment; independent validated cohorts can provide a larger Alpha adjustment.
- Unverified/suspicious CTA links always suppress action regardless of score.
- Risk >=70 prevents APPLY_WL/PREPARE/MINT_RECHECK.
- LOW evidence is WATCH-only.
- Scoring rules are versioned and regression-tested against positive and negative fixtures.

## Consequences
The system may intentionally withhold a high-hype opportunity when evidence is weak. This is desired behavior. Score calibration can evolve without changing the safety boundary.
