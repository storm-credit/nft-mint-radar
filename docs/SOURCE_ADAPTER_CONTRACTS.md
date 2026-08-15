# Source Adapter Contracts

## Common adapter interface
Every source adapter implements the logical contract below.

```yaml
SourceAdapter:
  adapter_name: string
  source_type: enum
  trust_tier_default: T0|T1|T2|T3|T4
  roles: [enum]
  auth_mode: NONE|API_KEY|OAUTH|BOT_TOKEN|PARTNER_KEY|RPC_KEY|OTHER
  mode: POLL|STREAM|QUERY|WEBHOOK|MANUAL_REFERENCE

poll_or_receive:
  input:
    cursor: string|null
    since: datetime_utc|null
    limit: integer
  output:
    raw_events: [RawEvent]
    next_cursor: string|null
    provider_usage: ProviderUsage
    health: HEALTHY|DEGRADED|DISABLED

ProviderUsage:
  request_count: integer
  returned_records: integer
  rate_limit_remaining: integer|null
  rate_limit_reset_at: datetime_utc|null
  cost_units: number|null
  cost_currency: string|null
  actual_cost: number|null
```

Hard adapter rules:
- do not emit user-facing claims; only RawEvents/Evidence candidates;
- preserve provider-native ids/cursors when available;
- return explicit AUTH_REQUIRED/RATE_LIMITED rather than silently dropping data;
- never log secrets;
- every paid adapter receives a configurable hard budget;
- provider failure cannot stop unrelated adapters.

## XAdapter

### Role
P0 discovery + T1 verification when account identity is verified official.

### Supported modes under consideration
- filtered stream primary
- recent-search polling
- hybrid stream + catch-up search

Final selection waits for `SPIKE-X-001`.

### Auth
X API credentials through environment/secret manager.

### Query policy
Rules should favor:
- verified watched project accounts;
- narrow NFT/WL keywords;
- account-specific rules over global broad keywords where cost/noise matters.

### Native identity
Post id is source_native_id. Edited/deleted handling records content/version evidence where provider data exposes it.

### Error handling
- 429 -> honor rate-limit reset; DEGRADED
- billing/credit exhausted -> COST_BUDGET_EXCEEDED; DEGRADED/DISABLED
- stream disconnect -> reconnect with bounded backoff; use catch-up mode if selected by ADR

### Current design facts
Filtered stream and recent search exist, but pricing is account/console dependent. Never hard-code an assumed per-post price.

## OfficialWebsiteAdapter

### Role
T1 verification, official link/domain discovery, schedule/contract/correction evidence.

### Ingest policy
Only crawl pages that are:
- already linked from verified project identity; or
- discovered through a trusted marketplace/campaign platform and subsequently corroborated.

### Fetch behavior
- conditional HTTP requests where supported (ETag/Last-Modified)
- canonical URL normalization
- bounded page size/depth
- content hash for edits

### Safety
Never automatically follow arbitrary redirects from T3/T4 into CTA trust. Redirect chain is evidence and requires host verification.

## OpenSeaAdapter

### Role
T2 structured discovery/verification for drops and marketplace event context.

### Phase 1 endpoints
- upcoming drops
- drop detail/stages
- collection/NFT/account events when needed for evidence

### Auth
`OPENSEA_API_KEY`.

### Mapping
Upcoming drop -> Project candidate + Opportunity candidate.
Drop stage fields -> allocation/mint price/start/end/max-per-wallet/supply where provided.

### Constraints
OpenSea is not universal NFT coverage. Source ROI metrics decide whether another marketplace is added.

### Excluded API usage
Transaction-building/mint endpoints are out of scope even if provider exposes them.

## GalxeAdapter

### Role
T2 structured quest/eligibility intelligence.

### Auth
`GALXE_ACCESS_TOKEN` where required.

### Phase 1/2 reads
- quest details
- quest status/start/end/cap/participants
- credential groups/condition relations
- wallet-specific eligibility only in later personal phase when the user explicitly configures an address

### Mapping
Quest -> Opportunity and/or Quest records.
Condition relation ALL/ANY must be preserved; do not flatten it into an inaccurate simple list.

### Cache
Quest metadata soft cache 1–5 minutes near deadlines; longer when inactive, subject to rate-limit spike evidence.

### Safety
Claim/participation mutations are not part of the radar.

## PREMINTAdapter

### Role
T2 allowlist registration/list status when supported access exists.

### Preferred mode
PREMINT Connect partner API if approved for this use case.

### Supported metadata targets
- project info
- registration start/end
- eligibility requirements
- winner/waitlist/list status where user-specific functionality is later configured

### Fallback
If partner API access is unavailable:
- store official PREMINT registration URL as verified T2 reference when linked from official project sources;
- parse only content accessible through permitted public mechanisms;
- no protected-page scraping/circumvention.

### Mandatory status
OPTIONAL until `SPIKE-CAMPAIGN-001` resolves access.

## GuildAdapter

### Role
T2 requirement/role intelligence when a supported public/programmatic access path is confirmed.

### Requirement model
Must preserve:
- ALL
- ANY/meet 1
- X of Y
- negative/"should not satisfy" requirements
- on-chain/social/Discord/time-based requirements

### Fallback
Official Guild page may be a verified external reference; if no stable supported data API is available, adapter stays PUBLIC_REFERENCE_ONLY.

## OnChainAdapter

### Role
T0 objective contract/deployer/wallet evidence.

### Initial chain scope
Ethereum + Base (EVM).

### Required functions
- contract existence/deployment block/time
- transaction/log lookup
- ERC721/ERC1155 mint/transfer evidence where standards permit
- deployer/funder relation inputs
- watched-wallet contract/NFT interactions

### Provider strategy
RPC/indexer provider is replaceable. Domain schema may not depend on provider-specific types.

### Reorg/finality
Store block number/hash for chain evidence. For very fresh events, mark confirmation status; recheck before irreversible/action-critical conclusions.

## DuneAdapter

### Role
T0/T3 analytics layer depending on query provenance: objective rows derived from chain data but analytical interpretation/query logic is treated separately.

### Preferred frequent-read mode
Fetch latest saved-query results rather than executing fresh query every poll where freshness permits.

### Fresh execution
Scheduled/batched according to `SPIKE-DUNE-001` cost/freshness result.

### Required usage metadata
- query id/version
- latest execution id
- execution timestamp
- execution cost credits when exposed
- result row/byte counts

### Result optimization
Use server-side filtering/column selection/pagination to reduce result size and credit use.

### Fallback
Dune unavailable -> wallet cohort features UNKNOWN; no core outage.

## RedditAdapter

### Role
T4 discovery/sentiment only.

### Policy
Never creates direct ACTION/URGENT alert without corroboration. Useful signals become internal candidates/verification tasks.

## TelegramSourceAdapter

### Role
- official project announcement channel: potentially T1 after identity verification
- public alpha group: T4

### Policy
Forwarded messages and links inherit no trust. Verify against source project identities.

### Implementation gate
Public/source access mechanism must be separately reviewed; notification bot credentials do not automatically grant arbitrary source-channel read access.

## TelegramNotifier

### Role
P0 destination, not a discovery source.

### Auth
`TELEGRAM_BOT_TOKEN`; target configured separately.

### Operation
`sendMessage` for MVP.

### Payload
<=4096 rendered characters. Message includes correlation/fingerprint only in logs, not necessarily visible.

### Delivery semantics
Use transactional outbox. Mark SENT only after successful provider response. Ambiguous timeout is reconciled conservatively to avoid notification storms.

## DiscordAdapter — Phase 3

### Role
Permitted T1 announcement read + user role/progress verification only in servers where app is installed/authorized.

### Auth
Bot/app credentials only; never user token.

### Access facts
- Gateway/REST are official paths.
- MESSAGE_CONTENT is privileged for message content.
- GUILD_MEMBERS is privileged for broad member-related access.
- server installation and permissions are prerequisites.

### Product consequence
Discord adapter is `SERVER_OPT_IN`; the product must not assume arbitrary NFT servers will install our bot.

### Fallback
Official website/X-disclosed Discord requirements remain Quest evidence even when live Discord progress cannot be read.

## Adapter source-health policy

### HEALTHY
Last expected fetch/stream heartbeat succeeded and data contract parsed.

### DEGRADED
- rate limited
- cost budget near/exceeded
- transient provider issues
- stale cursor/backfill gap
- partial permissions

### DISABLED
- credentials absent for optional adapter
- access revoked
- provider contract changed and parser quarantined
- manual operator disabled source

### Critical blind-spot behavior
If an ACTION alert requires a source currently unavailable for mandatory verification, fail closed: downgrade/suppress action and schedule recheck rather than infer.
