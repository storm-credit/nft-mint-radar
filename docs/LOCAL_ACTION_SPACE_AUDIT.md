# Local Action Space Audit

## Purpose
Measure only **project-designed model-driven reasoning nodes** under ADR-009 / `MINIMUM_ACTION_ADOPTION.md`.

This is not a global limit on sources, adapters, services, or total agents. Deterministic routing owned by code is outside model choice, provided the model is not secretly choosing the dispatch key.

## Audit rule
For each node record:
- whether the model has callable/tool choices;
- whether its output directly chooses among downstream callables/branches;
- measured meaningful peer choice count;
- deterministic enforcement that prevents hidden expansion;
- recheck trigger.

Target: <=5 meaningful peer choices per designed model-driven node.

---

## Node 1 — UNSTRUCTURED_SIGNAL_EXTRACT

### Purpose
Extract claims, links, dates, event labels, and project hints from one unstructured source event.

### Context
Only:
- one RawEvent;
- source identity/tier;
- small candidate identity set;
- extraction schema;
- forbidden inference rules.

### Tools/callables exposed
**0**.

The model returns structured data only. It does not select source adapters, fetch tools, verification tools, database actions, or notification actions.

### Downstream routing
The same deterministic verification pipeline receives the output regardless of extracted event label. Event labels are data, not callable selectors.

### Count
**0 — PASS**.

### Recheck trigger
If the extractor receives search/browse/tool access, or its label begins dispatching different callable pipelines.

---

## Node 2 — AMBIGUOUS_ENTITY_RESOLVE

### Purpose
Resolve identity only after deterministic official-link/contract/exact-match rules remain ambiguous.

### Context
- one candidate identity;
- directly relevant candidate Projects;
- matching links/contracts;
- supporting/conflicting Evidence.

### Tools/callables exposed
**0** external callables.

### Decision outcomes
Structured outcome enum:
1. MATCH_EXISTING
2. CREATE_NEW
3. SPLIT_REQUIRED
4. UNRESOLVED

These outcomes are validated by deterministic evidence gates before mutation. The model cannot write state directly.

### Count
Conservative branch count: **4 — PASS**.

### Recheck trigger
If more mutation branches are added or direct database/write tools are exposed.

---

## Node 3 — QUEST_PARSE (Phase 2)

### Purpose
Convert one campaign/stage's unstructured qualification text into Quest records.

### Context
- one Project/Campaign/Stage;
- only source text/payload containing requirements;
- Quest schema;
- deadline/timezone context;
- manual-action/safety rules.

### Tools/callables exposed
**0**.

The model emits Quest data only. It cannot follow/repost/join/chat/sign/submit/register.

### Downstream routing
Schema validation and UserProgress handling are deterministic and always run.

### Count
**0 — PASS**.

### Recheck trigger
If the parser gains browser/social/wallet tools or provider write actions.

---

## Node 4 — INDEPENDENT_CRITIC

### Purpose
Evaluate a design/prompt/schema/fixture change independently of builder rationale.

### Context
- artifact;
- requirements;
- constraints;
- acceptance criteria;
- verification evidence.

### Tools/callables exposed
**0** by default.

### Verdict branches
1. PASS
2. PATCH
3. CUT
4. BLOCK

The critic cannot directly edit or merge; its verdict is evidence for the governing gate.

### Count
Conservative branch count: **4 — PASS**.

### Recheck trigger
If critic receives edit/merge/deploy capabilities or additional direct action branches.

---

# Deterministic Runtime Nodes — Not Model-Driven

The following are explicitly **not** LLM action-selection nodes in Phase 1:
- source scheduler/adapter dispatch;
- normalization worker orchestration;
- evidence persistence;
- campaign/stage state transition;
- scoring formula;
- hard risk/CTA gate;
- dedup/fingerprint;
- cost budget enforcement;
- outbox processing;
- Telegram rendering/sending.

They must remain deterministic unless a future ADR changes their mechanism. If a model is inserted, this audit becomes stale for that node and must be re-derived before the change passes Gate.

# Waivers / scope limits

- Designed model-node waivers: **0**.
- Designed model-node scope limits: **0**.

No generic shell/router/open-ended tool is used to hide a wider callable set.

# Verdict

**PASS — current planned model-driven nodes are within the local-action-space bound.**

This verdict is design-time only. Production implementation must verify the actual tool exposure matches this audit.
