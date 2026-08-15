# Technical Spike Plan

## Purpose
Spikes answer architecture-threatening uncertainties without allowing disposable experiments to become production code by accident.

Rules:
- every spike answers one bounded question;
- no production feature code during spike work;
- credentials are never committed;
- each spike produces a written result and ADR impact;
- if a provider cannot be accessed without paid/partner credentials, that itself is a valid result;
- a failed spike must leave the core architecture operational through adapter degradation/fallback.

## SPIKE-X-001 — X discovery access/cost

### Question
Can official-project X posts and WL/giveaway signals be detected with acceptable latency and predictable spend for the expected watched-account/query count?

### Current documentation facts to validate operationally
- X supports recent search and filtered stream.
- Filtered Stream supports up to 1,000 rules and one pay-per-use connection according to current docs.
- Usage billing is separate from rate limits and current endpoint pricing is visible in the Developer Console.

### Hypotheses
H1: Filtered Stream is the best fit for a bounded watchlist of official accounts/keywords when spend is acceptable.
H2: Recent-search polling is a viable degraded mode for smaller watchlists or budget constraints.

### Method
1. Record current Developer Console pricing/budget options without exposing keys.
2. Build no production adapter; use curl/API explorer or disposable script outside production package.
3. Test 10 representative account rules + WL keywords.
4. Measure delivered-post count, false positives, detection latency, reconnect behavior, and estimated monthly spend.
5. Compare against recent-search polling at 5/10/15 minute cadence.

### Success
- p95 detection latency <= 10 minutes for official target posts;
- monthly cost can be bounded under the chosen user budget;
- no need for prohibited scraping;
- rule/watchlist capacity is sufficient for MVP.

### Failure
- required spend is materially higher than budget;
- access tier unavailable;
- false-positive retrieval makes spend unpredictable;
- latency cannot meet 15 minutes reliably.

### Cost/time cap
- no more than the smallest practical paid test budget without explicit user approval;
- 1 bounded experiment session.

### Artifact
`docs/spikes/SPIKE-X-001-RESULT.md`

### Decision unlocked
ADR chooses STREAM_PRIMARY, SEARCH_PRIMARY, HYBRID, or X_OPTIONAL.

---

## SPIKE-CAMPAIGN-001 — PREMINT / Galxe / Guild feasibility

### Question
Which allowlist/quest platforms provide stable programmatic data for discovery, requirements, deadlines, and eligibility without fragile scraping?

### Known starting facts
- Galxe exposes Quest/eligibility data via authenticated GraphQL API.
- PREMINT Connect exposes project info/list/wallet status to approved integration partners and requires an API key application.
- Guild exposes rich requirement/role concepts publicly; exact data access surface for our read-side use must be validated.

### Method
Galxe:
1. Test token acquisition requirements.
2. Query one public quest and capture status/start/end/cap/participant/credential structure.
3. Check whether task requirements can be normalized without user wallet.

PREMINT:
1. Determine whether project metadata can be accessed through PREMINT Connect for our use case.
2. If partner key is unavailable, document official/public fallback and do not scrape protected content.

Guild:
1. Determine whether public guild/role/requirement data has supported API/query endpoints or stable public representations permitted for access.
2. Capture one representative ALL/ANY requirement tree.

### Success
At least Galxe has a supported structured path; PREMINT/Guild each have either a supported adapter path or an explicit optional/manual fallback.

### Failure
Any provider is treated as mandatory despite inaccessible/unstable data.

### Cost/time cap
No paid partner plan purchase without user approval.

### Artifact
`docs/spikes/SPIKE-CAMPAIGN-001-RESULT.md`

### Decision unlocked
Per-platform source adapter mode: API, OPTIONAL_API, PUBLIC_REFERENCE_ONLY, or DISABLED.

---

## SPIKE-TG-001 — Telegram delivery

### Question
Can the notification outbox reliably deliver concise action alerts to the user's Telegram chat with dedup-safe observable success/failure?

### Known starting facts
Telegram Bot API `sendMessage` accepts text up to 4096 characters and returns the sent Message on success.

### Method
1. User creates bot/token and supplies it only through GitHub Secret/runtime environment.
2. Resolve a target chat id through a user-initiated bot conversation.
3. Send one dry-run message containing markdown-safe fields, KST deadline, verified-link placeholder, and correlation id.
4. Record HTTP/result semantics, retry behavior, and formatting constraints.

### Success
- dry-run delivered once;
- delivery response is observable;
- token is not logged;
- duplicate retry can be suppressed through outbox state.

### Failure
- credentials cannot be configured safely;
- delivery state cannot be observed/reconciled.

### Artifact
`docs/spikes/SPIKE-TG-001-RESULT.md`

### Decision unlocked
Telegram notifier implementation contract.

---

## SPIKE-DUNE-001 — Dune wallet-cohort analytics

### Question
Can Dune provide enough freshness, reproducibility and affordable query execution/result retrieval to support Alpha Wallet/cohort signals without becoming a hard dependency?

### Known starting facts
- Dune can execute saved/SQL queries asynchronously.
- latest query results can be fetched without triggering execution, but result retrieval consumes credits based on result size.
- execution costs depend on actual compute resources; result filtering/column selection can reduce transfer/cost.

### Method
Define two disposable queries:
1. recent NFT interactions for a small seed wallet list;
2. overlap of early minters across a small benchmark collection set.

Measure:
- execution time;
- execution credits;
- result retrieval credits/size;
- freshness when using latest cached result;
- benefit of server-side filters/columns;
- reproducibility across reruns.

### Success
- cached/latest result can support most frequent reads;
- fresh execution cadence can be bounded to a practical budget;
- query results can emit deterministic WalletSignal fixtures;
- core radar continues when Dune is unavailable.

### Failure
- freshness/cost unsuitable even at low cadence;
- query semantics too unstable for reproducible cohort signals.

### Artifact
`docs/spikes/SPIKE-DUNE-001-RESULT.md`

### Decision unlocked
Refresh cadence, cached-vs-execute policy, and whether Phase 1.5 is enabled.

---

## SPIKE-DISCORD-001 — permitted Discord intelligence

### Question
Can official Discord announcements and user role/progress state be read with server-approved bot/API access for enough projects to justify Phase 3?

### Known starting facts
- Discord bots use REST and/or Gateway.
- message content is a privileged intent.
- guild-member access is also privileged and relevant to role/member state.
- apps need to be installed/invited to a server with appropriate permissions; arbitrary third-party server access must not be assumed.

### Method
1. Use only a server where the bot is explicitly permitted.
2. Test reading a configured announcement channel.
3. Test member role data for the bot's authorized context.
4. Record required scopes/intents/permissions and what is unavailable when not installed.
5. Do not automate user messages/activity.

### Success
- supported read path works in authorized servers;
- missing access degrades to official-link/manual requirement tracking;
- no self-bot/user-token use.

### Failure
- useful coverage requires unauthorized user automation or widespread server-admin cooperation impossible for the product.

### Artifact
`docs/spikes/SPIKE-DISCORD-001-RESULT.md`

### Decision unlocked
Phase 3 becomes SERVER_OPT_IN only, PARTIAL, or DISABLED.

---

## SPIKE-MARKET-001 — Marketplace/drop coverage

### Question
Are OpenSea APIs sufficient for the MVP's Ethereum/Base upcoming-drop discovery and mint-stage metadata, and what additional marketplace is actually justified by unique lead value?

### Known starting facts
Current OpenSea API includes:
- `/api/v2/drops?type=upcoming`;
- drop details including stages, pricing and supply;
- collection/account/NFT event endpoints;
- API key authentication.

### Method
1. Fetch upcoming drops filtered to Ethereum/Base.
2. Fetch details for representative drops and map stages to Opportunity.
3. Compare returned projects against a small manual sample of known upcoming NFT activity.
4. Measure unique discovery value and missing coverage.
5. Evaluate Magic Eden/other adapter only if the gap is material.

### Success
- OpenSea maps cleanly into canonical schemas;
- missing coverage is measurable;
- no speculative multi-market implementation is required.

### Failure
- OpenSea's upcoming calendar misses too much of target NFT alpha to serve as a P0 structured source.

### Artifact
`docs/spikes/SPIKE-MARKET-001-RESULT.md`

### Decision unlocked
MVP marketplace source set.

---

## SPIKE-RUNTIME-001 — scheduler/runtime model

### Question
Can GitHub Actions satisfy Phase 1 polling/delivery latency and stateful reliability, or is a long-running/serverless worker required?

### Four candidate models
A. GitHub Actions cron only
B. Serverless scheduled functions
C. Long-running worker + PostgreSQL
D. Hybrid: Actions for batch/Dune, worker/serverless for low-latency feeds

### Method
Use expected source cadences after X/market spikes and compare:
- minimum/reliable schedule granularity;
- state/cursor handling;
- secret handling;
- concurrency/idempotency;
- always-on stream support;
- monthly operational cost.

### Success
Choose a model that can meet alert latency SLO without abusing a scheduler or losing event cursors.

### Failure
Selecting GitHub Actions simply because the repository is on GitHub despite incompatible streaming/state needs.

### Artifact
`docs/spikes/SPIKE-RUNTIME-001-RESULT.md`

### Decision unlocked
ADR for deployment/runtime topology.

---

## Spike order
1. `SPIKE-X-001`
2. `SPIKE-MARKET-001`
3. `SPIKE-CAMPAIGN-001`
4. `SPIKE-TG-001`
5. `SPIKE-DUNE-001`
6. `SPIKE-RUNTIME-001`
7. `SPIKE-DISCORD-001` (Phase 3 gate; not required to begin Phase 1 if designed as optional)

## Phase 1 coding gate
Required spike results before production Phase 1 code:
- X: resolved or explicitly optional
- Marketplace: resolved
- Campaign platforms: resolved enough to select adapters
- Telegram: delivery/config contract resolved
- Runtime: resolved

Dune may remain Phase 1.5 optional. Discord may remain Phase 3 optional.
