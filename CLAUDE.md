# NFT Mint Radar — AI Development Harness

## Mission
Build a personal NFT alpha assistant that discovers promising NFT opportunities before or during allowlist/mint preparation, verifies evidence, prioritizes what is worth the user's time, tracks required actions, and notifies through Telegram without ever signing transactions or impersonating the user.

This file is the **project operating constitution**. Domain schemas, scoring details, source-specific behavior, and current state belong in their own authorities below; do not duplicate them here.

---

## 0. Authority recovery — always first
Before proposing, redesigning, spiking, or implementing anything, recover the current repository state.

Read in this order when relevant:
1. `CLAUDE.md`
2. `docs/PROJECT_STATUS.md`
3. `docs/PRODUCTION_CODING_START_GATE.md`
4. `docs/DEEP_DESIGN.md`
5. `docs/ARCHITECTURE.md`
6. `docs/SOURCE_STRATEGY.md`
7. `docs/HARNESS_SPEC.md`
8. `docs/HARNESS_SCHEMAS.md`
9. `docs/EVAL_FIXTURES.md`
10. `docs/MINIMUM_ACTION_ADOPTION.md`
11. relevant `docs/spikes/*-RESULT.md`
12. relevant ADRs under `docs/decisions/`
13. `docs/deviations/CHANGELOG_DECISIONS.md`

Then determine:
- authoritative current phase and gate state;
- what is complete;
- what is incomplete;
- what is blocked by design;
- what is blocked by operational evidence;
- what may be spiked;
- what may be implemented.

Do not restart broad design because a new session starts. Continue from the first incomplete authoritative gate.

Never:
- reset completed Deep Design without a documented P0 defect;
- overwrite an ADR silently;
- treat paper/provider documentation as observed provider reality;
- treat spike artifacts as production code;
- widen the current phase without an explicit decision record;
- maintain a second hand-written source of truth when an authority already exists.

---

## 1. Gate hierarchy

```text
CURRENT-STATE RECOVERY
    -> DEEP DESIGN
    -> EXECUTABLE HARNESS DESIGN
    -> BLIND-SPOT / RED TEAM
    -> TECHNICAL SPIKES / PILOTS
    -> OBSERVED-EVIDENCE RECONCILIATION
    -> ARCHITECTURE / SCHEMA FREEZE
    -> PRODUCTION CODING START GATE
    -> PHASE IMPLEMENTATION
    -> INTEGRATION / EVAL
    -> OPERATIONS
```

The purpose is not document volume. The purpose is to prevent production code from becoming the place where unresolved product, provider, safety, cost, and data-contract decisions are accidentally made.

### Validation-state separation
Keep these distinct:
- `DESIGNED`
- `PAPER_VALIDATED`
- `SPIKE_VALIDATED`
- `PRODUCTION_VALIDATED`

A lower state is never silently promoted to a higher one.

### Freeze rule
Once a design area passes its gate, prefer `KEEP`, `PATCH`, or `CUT`.
Use `NEW DESIGN` only when evidence reveals a real P0 structural hole.

Upstream changes that invalidate downstream contracts must mark affected artifacts `STALE` and trigger targeted revalidation, not a full-project reset.

---

## 2. Minimum Necessary Agency
`docs/MINIMUM_ACTION_ADOPTION.md` is the authority for the project's adaptation of `minimum-action-agent-os`.

Core rules:
- **Least Tool** — expose only tools needed at the current node.
- **Least Context** — pass only the smallest relevant source-of-truth/evidence bundle.
- **Least Authority** — grant only required read/write/execute permission.
- **Deterministic first** — routine routing, state transitions, scoring math, safety gates, dedup, budgeting and notification transport should be programmatic where possible.
- **Real boundaries only** — create an Agent only for a real context/tool/permission/evidence/failure/independent-judgment boundary; persona alone is not enough.
- **Local action space** — project-designed model-driven nodes should expose at most five meaningful peer choices by default. Deterministic routing enforced outside the model is not model choice.
- **No choice laundering** — do not hide many peer decisions behind a generic shell/router/open prompt and call the action space reduced.

`HARNESS_SPEC.md` role names are logical execution contracts; they do not imply one autonomous agent per role.

---

## 3. Non-negotiable workflow
For non-trivial work, use only the stages needed, in this order where applicable:
1. Current-state recovery.
2. Intent / missing-context check.
3. Blind-spot sweep.
4. Preflight trap check.
5. Four materially different alternatives only when design space is genuinely open.
6. Exemplar/official-source research only when findings can change the design.
7. Meta-prompt compilation when another AI/tool is the executor.
8. Execute only the work type allowed by the current gate.
9. Independent evaluation when warranted.
10. Acceptance/harness verification.
11. Update state/canon/change log.
12. Record plan drift when actual execution diverged.

Do not mechanically run every stage for simple work.

### Engineering principles
- State material assumptions before coding.
- Prefer the smallest correct and reversible change.
- Do not invent requirements or silently widen scope.
- Define success/stop conditions before execution.
- Surface uncertainty in evidence/confidence instead of guessing.
- A technical spike answers one uncertainty and must not grow into a production subsystem.

---

## 4. Phase boundary
Design interfaces for later phases, but do not implement later-phase behavior unless the current phase requires it.

Current phases:
- Phase 1: discovery + verification + scoring + Telegram notification.
- Phase 2: allowlist/quest parsing + effort score + task tracking.
- Phase 3: permitted Discord intelligence/read-side progress tracking.
- Phase 4: personalized alpha agent using wallet eligibility and user progress.

Future-phase awareness is allowed. Future-phase implementation is not.

---

## 5. Production Coding Start Gate
Production feature code is forbidden until `docs/PRODUCTION_CODING_START_GATE.md` passes or an explicit ADR waives a named criterion.

A feature is not `CODING_READY` because interfaces are designed.
If a provider/API uncertainty can materially change architecture, cost, latency, coverage, or safety, resolve it through a bounded technical spike first.

### Spike contract
Every spike has:
- one question;
- hypothesis;
- method;
- success condition;
- failure condition;
- time/cost cap;
- disposable boundary;
- retained result evidence;
- architectural decision unlocked by the result.

Spike code stays isolated from production code.

---

## 6. Domain authorities
Do not restate these contracts here.

- Domain model / event / campaign / stage / evidence semantics: `docs/DEEP_DESIGN.md` plus Accepted ADRs.
- Source hierarchy and discovery-vs-verification roles: `docs/SOURCE_STRATEGY.md`.
- Scoring and hard safety gates: `docs/DEEP_DESIGN.md` + scoring ADRs.
- Harness roles/stages: `docs/HARNESS_SPEC.md`.
- Typed role I/O: `docs/HARNESS_SCHEMAS.md`.
- Golden expected behavior: `docs/EVAL_FIXTURES.md`.
- Current truth/blockers/next action: `docs/PROJECT_STATUS.md`.

If an Accepted ADR conflicts with an older document section, the ADR governs until the canonical document is synchronized; the affected document must be marked/fixed as stale before freeze.

---

## 7. Automation safety boundary
Allowed:
- discover information;
- parse tasks;
- verify official links/evidence;
- track public wallet/on-chain activity;
- score/prioritize projects and opportunities;
- create reminders/Telegram alerts;
- read Discord data only through permitted bot/API access.

Never automate:
- wallet signatures;
- token/NFT approvals;
- transaction submission or minting;
- seed/private-key handling;
- Discord user self-bots;
- fake engagement, automated chat, spam, fake referrals, or impersonation.

Hard safety guarantees belong in deterministic code/schema/CI/runtime, not only natural-language prompts.

---

## 8. Secrets and authority
API keys, Telegram bot tokens, Discord/X/Dune/OpenSea/provider tokens and wallet-related secrets must be environment/runtime/GitHub Secrets only. Never commit them.

Do not infer secret presence when the current integration cannot enumerate secrets. Treat availability as `UNKNOWN` until the relevant spike proves access.

---

## 9. Meta-prompting and context
When another AI/tool executes the task:
1. dump raw context into prompt-design stage;
2. identify material missing context;
3. define success and stop conditions;
4. translate to target execution environment;
5. shave redundant context/instructions;
6. expose only necessary tools/actions/context;
7. execute;
8. independently check result;
9. revise on observed failure, not speculation alone.

Prompts consume the smallest sufficient evidence bundle. Deep repository structure is retrieval infrastructure, not permission to dump everything into one prompt.

---

## 10. Cross-system Red Team
Before freeze or production-coding gate, check at minimum:
- source coverage gaps;
- identity/official-channel confusion;
- phishing/link substitution and compromised official accounts;
- stale/edited announcements;
- timezone/deadline errors;
- duplicate/repeated alerts;
- influencer/shill manipulation;
- whale/wash/sybil manipulation;
- source outage/degradation;
- provider cost/rate-limit blow-up;
- hidden later-phase dependency;
- accidental wallet/social action;
- false certainty from LLM extraction;
- illegal state transitions;
- optional-source failure without graceful degradation;
- God Agent / Tool Swamp / Agent Explosion;
- Shadow Authority / Stale Derived Artifact.

Classify findings P0/P1/P2. Production coding cannot start with unresolved P0.

---

## 11. Independent critique
When independent critique is warranted, default reviewer input is:
- artifact;
- requirements;
- constraints;
- acceptance criteria;
- evidence required for verification.

Do not preload the builder's full rationale/self-justification. For permission/forbidden clauses, reviewers should identify undefined terms and test whether a weaker reading hollows the rule.

---

## 12. Validation and stale propagation
No feature is complete because code exists. Completion requires an observable validation path appropriate to the feature.

No design is complete because a document exists. Completion requires its gate/checklist and material provider uncertainties to be resolved or explicitly waived.

When an authority changes, search/update its derived artifacts in the same change. Typical chain:

```text
ADR / DEEP_DESIGN
 -> HARNESS_SCHEMAS
 -> EVAL_FIXTURES
 -> PROMPT_CONTRACTS
 -> SPIKE MAPPINGS
 -> PROJECT_STATUS
```

If synchronization cannot be completed, mark the derived artifact `STALE` and block the affected gate.

---

## 13. Continue-from-current-state
At the end of meaningful work, update authoritative project state so another session can continue without reconstructing the conversation.

When starting a new session:
- do not ask the user to restate history recoverable from the repository;
- do not repeat completed design;
- do not reopen frozen decisions without new evidence;
- proceed from the first incomplete gate.
