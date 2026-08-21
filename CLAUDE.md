# NFT Mint Radar — AI Development Harness

## Mission
Build a personal NFT alpha assistant that discovers promising NFT opportunities before or during allowlist/mint preparation, verifies evidence, scores opportunity quality, tracks required actions, and notifies the user through Telegram without ever signing transactions or impersonating the user.

## 0. Authority recovery — always first
Before proposing, redesigning, spiking, or implementing anything, recover the current repository state.

Read in this order when present:
1. `CLAUDE.md`
2. `docs/PROJECT_STATUS.md`
3. `docs/DEEP_DESIGN.md`
4. `docs/ARCHITECTURE.md`
5. `docs/SOURCE_STRATEGY.md`
6. `docs/HARNESS_SPEC.md`
7. `docs/HARNESS_SCHEMAS.md`
8. `docs/EVAL_FIXTURES.md`
9. `docs/SPIKE_PLAN.md`
10. relevant `docs/spikes/*-RESULT.md`
11. relevant ADRs under `docs/decisions/`
12. `docs/deviations/CHANGELOG_DECISIONS.md`
13. recent repository changes/status when available

Then explicitly determine:
- authoritative current phase and gate state;
- what is complete;
- what is incomplete;
- what is blocked by design;
- what is blocked by operational evidence;
- what may be spiked;
- what may be implemented.

Do not restart broad design merely because a new session starts. Continue from the first incomplete authoritative gate.

Never:
- reset a completed Deep Design without a documented P0 defect;
- overwrite an ADR silently;
- treat a paper assumption as observed provider reality;
- treat a spike artifact as production code;
- widen the current phase without an explicit decision record.

## 1. Gate hierarchy
The project uses a strict staged authority model:

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

The purpose is not to maximize documents. The purpose is to prevent production code from becoming the place where unresolved product, provider, safety, and data-contract decisions are accidentally made.

### Design vs observed state
Keep these separate:
- `DESIGNED`: specified in canonical design documents.
- `PAPER_VALIDATED`: supported by current provider documentation.
- `SPIKE_VALIDATED`: observed through an isolated real test.
- `PRODUCTION_VALIDATED`: observed in the deployed production path.

A lower state must never be silently promoted to a higher state.

### Freeze rule
Once a design area has passed its gate, prefer `KEEP`, `PATCH`, or `CUT` over reopening broad brainstorming.
Use `NEW DESIGN` only when evidence reveals a real P0 architectural hole.

Upstream changes that invalidate downstream contracts must mark affected artifacts `STALE` and trigger targeted revalidation rather than a full-project reset.

## 2. Non-negotiable workflow
Before implementation work, follow this order:
1. Current-state recovery — identify the authoritative incomplete gate.
2. Intent check — restate user intent, primary user, and success condition.
3. Blind-spot sweep — identify missing sources, data, timing, safety, cost, and operational risks.
4. Trap check — identify API limits, auth requirements, scraping fragility, ToS/automation boundaries, duplicate alerts, phishing, stale evidence, and time-zone errors.
5. Four-option design — provide four materially different implementation/design approaches when making a significant architecture/product decision.
6. Decision record — record chosen option and why in `docs/decisions/`.
7. Implementation/spike plan — smallest working slice first.
8. Execute only the work type allowed by the current gate.
9. Verify against explicit success conditions with tests or observable evidence.
10. Reconcile observed results back into design/freeze state.
11. Record deviations — if execution differs from the plan, record what changed, why, and impact in `docs/deviations/CHANGELOG_DECISIONS.md`.

## 3. Karpathy-style engineering principles
- State assumptions before coding when they materially affect the result.
- Prefer the smallest correct change over speculative architecture.
- Do not invent requirements.
- Do not silently widen scope.
- Keep changes local and reversible.
- Define how success will be verified before implementation.
- If uncertainty affects correctness, surface it in evidence/confidence rather than guessing.
- A technical spike must answer one uncertainty and must not grow into a product subsystem.

## 4. Phase boundary rule
Design interfaces for later phases, but do not implement later-phase behavior unless the current phase requires it.

Current planned phases:
- Phase 1: discovery + verification + scoring + Telegram notification.
- Phase 2: allowlist/quest parsing + effort score + task tracking.
- Phase 3: Discord intelligence/read-side progress tracking where permitted.
- Phase 4: personalized alpha agent using wallet eligibility and user progress.

Future-phase awareness is allowed. Future-phase implementation is not.

## 5. Production Coding Start Gate
Production feature code is forbidden until `docs/PRODUCTION_CODING_START_GATE.md` passes or an explicit ADR waives a named criterion.

The gate must distinguish:
- design completeness;
- harness completeness;
- credential-free dry-run completeness;
- provider paper validation;
- provider operational validation;
- unresolved P0 risks.

A feature is not `CODING_READY` merely because its interfaces are designed.
If a provider/API uncertainty could materially change architecture, cost, latency, coverage, or safety, resolve it with a technical spike first.

### Spike rule
A spike must have:
- one question;
- one hypothesis;
- method;
- success condition;
- failure condition;
- time/cost cap;
- disposable implementation boundary;
- retained `RESULT.md` evidence;
- architectural decision unlocked by the result.

Spike code must stay isolated from production code and may be discarded after the result is recorded.

## 6. Product model
The system must preserve these separate concepts:
- `Project`: the NFT/project identity.
- `Source`: where a signal came from.
- `Evidence`: immutable captured support for a claim.
- `Opportunity`: allowlist, raffle, holder mint, free mint, public mint, airdrop, etc.
- `Quest`: a required user action for eligibility.
- `UserProgress`: the user's completion/eligibility state.
- `WalletEntity`: a public wallet or entity being watched as a signal source.
- `InfluencerEntity`: an account/person watched as a weak discovery signal.
- `Notification`: deduplicated action-oriented alert.

## 7. Source trust policy
Discovery source and verification source are different roles.

Trust tiers:
- T0: on-chain contract/deployer/wallet evidence.
- T1: official project website, official X, official Discord announcements, official Telegram, official docs.
- T2: PREMINT, Galxe, Guild, marketplace launchpads, verified analytics platforms.
- T3: known collectors, smart-money wallets, established analysts/influencers, Dune community dashboards.
- T4: Reddit posts, public Telegram alpha groups, generic X posts, other community chatter.

T3/T4 may discover a project but may not by themselves establish mint/WL instructions. High-impact actions require T0/T1/T2 corroboration.

## 8. Scoring
Do not collapse everything into one opaque score. Track at least:
- `quality_score`: project/team/community/fundamental quality.
- `alpha_score`: how early/under-discovered the opportunity appears.
- `effort_score`: time/complexity/cost of obtaining eligibility; lower is better.
- `risk_score`: phishing, contract, team, concentration, wash-trading and manipulation risk; lower is better.
- `action_score`: decision score derived transparently from the above and evidence confidence.

Influencer popularity, follower count, raw transaction volume, and whale activity are signals only, never automatic positive scoring inputs.

## 9. Evidence rules
Every material claim used in scoring should keep:
- source URL or source identifier
- source tier
- captured timestamp
- claim text/normalized value
- confidence
- verification status

Deleted/changed announcements must remain auditable through prior evidence records.

Projected/provider-documented behavior and actually observed provider behavior must remain distinguishable in evidence.

## 10. Time rules
Store timestamps in UTC; present alerts in Asia/Seoul (KST).
Track when known:
- discovered_at
- registration_open_at
- registration_close_at
- snapshot_at
- allowlist_result_at
- allowlist_mint_at
- public_mint_at

## 11. Automation safety boundary
Allowed:
- discover information
- parse tasks
- verify official links
- track public wallet/on-chain activity
- score projects/opportunities
- create reminders/Telegram alerts
- read Discord data only through permitted bot/API access

Never automate:
- wallet signatures
- token/NFT approvals
- transaction submission or minting
- seed/private-key handling
- Discord user self-bots
- fake engagement, automated chat, spam, fake referrals, or impersonation

## 12. Secrets
API keys, Telegram bot tokens, Discord tokens, X tokens, Dune keys and wallet-related secrets must be environment variables/GitHub Secrets only. Never commit them.

Do not infer secret presence when the current integration cannot enumerate secrets. Treat secret availability as `UNKNOWN` until the relevant spike proves access.

## 13. Meta-prompting process
For every important LLM role:
1. Context dump.
2. Ask what additional context is required for reliable output.
3. Remove ambiguity/redundancy from the prompt.
4. Add explicit success conditions, failure conditions and stop conditions.
5. Evaluate against a fixture set before trusting production output.

Prompts must consume the smallest sufficient evidence bundle. Deep repository structure is for retrieval; it is not permission to stuff every source into one prompt.

## 14. Cross-system Red Team
Before a freeze or production-coding gate, attack the whole system, not only each component.

At minimum check:
- source coverage gaps;
- official-vs-community identity confusion;
- phishing/link substitution;
- stale or edited announcements;
- timezone/deadline errors;
- duplicate/repeated alerts;
- influencer/shill manipulation;
- whale/wash/sybil manipulation;
- source outage/degradation;
- provider cost blow-up;
- rate-limit failure;
- hidden dependency on a later phase;
- accidental wallet/social-account action;
- false certainty from LLM extraction;
- state-machine illegal transitions;
- architecture that cannot degrade when optional sources fail.

Classify findings P0/P1/P2. Production coding cannot start with unresolved P0 findings.

## 15. Validation rule
No feature is complete because code exists. Completion requires a real validation path: unit test, integration fixture, dry-run event, API response, or observable Telegram test where applicable.

No design is complete merely because a document exists. Completion requires its checklist/gate to be satisfied and any material provider uncertainty to be either spike-validated or explicitly waived by ADR.

## 16. Continue-from-current-state rule
At the end of every work session, update the authoritative status/handoff so the next agent can continue without repeating completed work.

When starting a new session:
- do not ask the user to restate repository history that can be recovered from the repository;
- do not repeat completed design;
- do not reopen frozen decisions without new evidence;
- proceed from the first incomplete gate.
