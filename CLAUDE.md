# NFT Mint Radar — AI Development Harness

## Mission
Build a personal NFT alpha assistant that discovers promising NFT opportunities before or during allowlist/mint preparation, verifies evidence, scores opportunity quality, tracks required actions, and notifies the user through Telegram without ever signing transactions or impersonating the user.

## Non-negotiable workflow
Before implementation work, follow this order:
1. Intent check — restate user intent, primary user, and success condition.
2. Blind-spot sweep — identify missing sources, data, timing, safety, cost, and operational risks.
3. Trap check — identify API limits, auth requirements, scraping fragility, ToS/automation boundaries, duplicate alerts, phishing, stale evidence, and time-zone errors.
4. Four-option design — provide four materially different implementation/design approaches when making a significant architecture/product decision.
5. Decision record — record chosen option and why in `docs/decisions/`.
6. Implementation plan — smallest working slice first.
7. Implement.
8. Verify against explicit success conditions with tests or observable evidence.
9. Record deviations — if the implementation differs from the plan, record what changed, why, and impact in `docs/deviations/CHANGELOG_DECISIONS.md`.

## Karpathy-style engineering principles
- State assumptions before coding when they materially affect the result.
- Prefer the smallest correct change over speculative architecture.
- Do not invent requirements.
- Do not silently widen scope.
- Keep changes local and reversible.
- Define how success will be verified before implementation.
- If uncertainty affects correctness, surface it in evidence/confidence rather than guessing.

## Phase boundary rule
Design interfaces for later phases, but do not implement later-phase behavior unless the current phase requires it.

Current planned phases:
- Phase 1: discovery + verification + scoring + Telegram notification.
- Phase 2: allowlist/quest parsing + effort score + task tracking.
- Phase 3: Discord intelligence/read-side progress tracking where permitted.
- Phase 4: personalized alpha agent using wallet eligibility and user progress.

## Product model
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

## Source trust policy
Discovery source and verification source are different roles.

Trust tiers:
- T0: on-chain contract/deployer/wallet evidence.
- T1: official project website, official X, official Discord announcements, official Telegram, official docs.
- T2: PREMINT, Galxe, Guild, marketplace launchpads, verified analytics platforms.
- T3: known collectors, smart-money wallets, established analysts/influencers, Dune community dashboards.
- T4: Reddit posts, public Telegram alpha groups, generic X posts, other community chatter.

T3/T4 may discover a project but may not by themselves establish mint/WL instructions. High-impact actions require T0/T1/T2 corroboration.

## Scoring
Do not collapse everything into one opaque score. Track at least:
- `quality_score`: project/team/community/fundamental quality.
- `alpha_score`: how early/under-discovered the opportunity appears.
- `effort_score`: time/complexity/cost of obtaining eligibility; lower is better.
- `risk_score`: phishing, contract, team, concentration, wash-trading and manipulation risk; lower is better.
- `action_score`: decision score derived transparently from the above and evidence confidence.

Influencer popularity, follower count, raw transaction volume, and whale activity are signals only, never automatic positive scoring inputs.

## Evidence rules
Every material claim used in scoring should keep:
- source URL or source identifier
- source tier
- captured timestamp
- claim text/normalized value
- confidence
- verification status

Deleted/changed announcements must remain auditable through prior evidence records.

## Time rules
Store timestamps in UTC; present alerts in Asia/Seoul (KST).
Track when known:
- discovered_at
- registration_open_at
- registration_close_at
- snapshot_at
- allowlist_result_at
- allowlist_mint_at
- public_mint_at

## Automation safety boundary
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

## Secrets
API keys, Telegram bot tokens, Discord tokens, X tokens, Dune keys and wallet-related secrets must be environment variables/GitHub Secrets only. Never commit them.

## Meta-prompting process
For every important LLM role:
1. Context dump.
2. Ask what additional context is required for reliable output.
3. Remove ambiguity/redundancy from the prompt.
4. Add explicit success conditions, failure conditions and stop conditions.
5. Evaluate against a fixture set before trusting production output.

## Validation rule
No feature is complete because code exists. Completion requires a real validation path: unit test, integration fixture, dry-run event, API response, or observable Telegram test where applicable.
