# ADR-009 — Minimum-Action Orchestration

## Status
Accepted — 2026-08-28

## Context
The harness currently describes Discovery, Verification, Scoring, Wallet Intelligence, Quest Parser, Decision, and Telegram Reporter as separate logical roles. If implemented literally as peer autonomous agents, this would create unnecessary agent/tool choice, duplicate context, permission sprawl, and weak independent verification.

The reference operating standard in `storm-credit/minimum-action-agent-os` favors minimum necessary agency, bounded local action space, agent creation only across real boundaries, deterministic enforcement for hard guarantees, and stale-derived-artifact control.

## Decision

### 1. Logical role != autonomous agent
`HARNESS_SPEC.md` role names are contracts. They do not imply one process/model agent per role.

### 2. Deterministic-first production pipeline
Phase 1 hot path defaults to deterministic orchestration:

```text
Source adapters
 -> normalization
 -> evidence/verification rules
 -> campaign/stage state
 -> scoring
 -> decision gates
 -> transactional outbox
 -> Telegram template
```

No central LLM chooses among all pipeline components.

### 3. LLM use is narrow and conditional
Initial model-driven capabilities are limited to bounded tasks where language ambiguity materially benefits from a model:
- unstructured signal/claim extraction;
- ambiguous entity resolution after deterministic rules fail;
- Phase 2 quest parsing;
- independent critique/eval.

Scoring formulas, hard safety gates, state transitions, deduplication, budgeting, source scheduler behavior, and Telegram rendering are deterministic by default.

### 4. Local action-space policy
At project-designed model-driven nodes, expose no more than five meaningful peer choices by default.

This is a local bound, not a limit on total sources/roles. Deterministic dispatch enforced outside the model does not count as model choice.

If a designed model node genuinely requires more, it needs an explicit measured waiver. Do not hide choices behind a generic shell/router.

### 5. Minimum context
Each LLM invocation receives only the task artifact plus the smallest relevant authority/evidence bundle, constraints, schema, acceptance criteria, and stop conditions.

### 6. Independent critique
Important design/prompt/schema changes may use a separate critic. Default critic input excludes builder rationale/self-justification and includes artifact, requirements, constraints, acceptance criteria, and verification evidence.

### 7. Stale propagation is mandatory
When canonical design/ADR changes invalidate schemas, fixtures, prompts, or spike mappings, affected derived artifacts must be updated in the same change or explicitly marked `STALE` and block the relevant gate.

## Consequences
- avoids God Agent / Agent Explosion / Tool Swamp architecture;
- reduces runtime token/context cost and accidental authority;
- makes safety, cost, state and dedup guarantees testable in code;
- keeps LLM use focused on language ambiguity rather than routine deterministic work;
- requires current ADR-007/008-derived stale schema documents to be synchronized before freeze.

## Rejected alternatives

### One autonomous agent per logical role
Rejected because most roles do not have distinct context/permission/evidence boundaries and deterministic code is more reliable for their hard rules.

### One all-powerful NFT agent
Rejected due to mixed evidence regimes, excess tools/authority/context, and weak independent review.

### Build a generic Agent OS runtime now
Rejected as premature runtime. The project adopts operating rules without adding a new orchestration product.

## Revalidation trigger
Revisit only if production evidence shows a deterministic component cannot meet accuracy/maintenance requirements and a model-driven decision node is materially better. Any new node must be re-measured for local action space and permissions.
