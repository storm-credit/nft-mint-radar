# Source Adapter Contracts

## Common adapter interface
Every source adapter emits source data only; no adapter decides the final user action.

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
```

Hard rules:
- emit RawEvents/Evidence candidates, not user recommendations;
- preserve provider ids/cursors;
- explicit AUTH_REQUIRED/RATE_LIMITED/PROVIDER_DEGRADED;
- never log secrets;
- every paid adapter has a configurable hard budget;
- failure of one adapter does not stop unrelated adapters;
- adapters never construct/sign/submit transactions.

## XAdapter
Role: P0 discovery + T1 identity/claim source when the account relation is verified.

Modes under operational validation:
- filtered stream
- recent-search polling
- hybrid

Final mode waits for `SPIKE-X-001`.

Use narrow project-account/keyword rules. A post from a verified official identity is not by itself proof that a newly introduced wallet-impacting CTA is safe.

## OfficialWebsiteAdapter
Role: T1 identity/link/domain/schedule/contract/correction source.

Policy:
- crawl only verified/corroborated project surfaces;
- bounded depth/size;
- conditional HTTP where possible;
- content hash for edits;
- arbitrary T3/T4 redirect chains never inherit CTA trust.

## OpenSeaAdapter
Role: T2 structured listed-drop discovery and campaign/stage verification support.

Phase 1 chains:
- Ethereum
- Base
- Robinhood Chain

Auth: `OPENSEA_API_KEY`.

Mapping:
```text
OpenSea drop -> Project candidate + MintCampaign candidate
OpenSea stage -> MintStage
stage allocation/time/price/max -> stage-specific fields
relevant user action -> Opportunity referencing campaign/stage
```

Price mapping preserves FREE/KNOWN/UNKNOWN/VARIABLE and canonical payment asset (`NATIVE|ERC20|OTHER`).

Constraints:
- OpenSea calendar/listing is not complete market coverage;
- absence is not negative evidence;
- transaction-building/mint endpoints remain out of scope.

## GalxeAdapter
Role: T2 quest/eligibility intelligence.

Auth: `GALXE_ACCESS_TOKEN` when required.

Reads may include quest details, status, start/end/cap, credential groups and condition relations. ALL/ANY/X-of-Y semantics must not be flattened inaccurately. Claim/participation mutations are out of scope.

## PREMINTAdapter
Role: T2 allowlist project/registration/list status where supported access exists.

Preferred: PREMINT Connect partner API when approved.
Fallback: verified official PREMINT reference + permitted public/manual ingest; no protected scraping/circumvention.

Optional until access is operationally validated.

## GuildAdapter
Role: T2 requirement/role intelligence when supported public/programmatic access is confirmed.

Must preserve ALL/ANY/X-of-Y/negative and on-chain/social/Discord/time requirements. Otherwise PUBLIC_REFERENCE_ONLY.

## OnChainAdapter
Role: T0 contract/wallet/transaction evidence.

Phase 1 EVM scope:
- Ethereum
- Base
- Robinhood Chain

Provider is replaceable; core schema does not depend on provider-native types.

Functions as supported by each provider/chain:
- contract existence/deployment block/time;
- transaction/log lookup;
- ERC721/ERC1155 mint/transfer evidence where applicable;
- factory/deployer/creator/admin/funder relation inputs;
- watched-wallet interactions.

Store block/hash for fresh evidence and represent confirmation/finality when relevant. A shared factory/deployer is not project creator identity by itself.

## DuneAdapter
Role: optional analytics layer for wallet/cohort evidence.

Prefer cached/latest saved-query results for frequent reads; fresh execution is bounded by `SPIKE-DUNE-001` cost/freshness results. Query version/execution timestamp/usage metadata are retained.

Unavailable Dune => cohort feature UNKNOWN; core radar continues.

## RedditAdapter
T4 discovery/sentiment only. Never creates direct ACTION/URGENT without corroboration.

## TelegramSourceAdapter
Official project channel may become T1 only after identity relation verification. Public alpha group is T4. Forwarded content/links inherit no trust.

## TelegramNotifier
P0 destination.

Auth: `TELEGRAM_BOT_TOKEN`; target separately configured.

MVP uses Bot API sendMessage through transactional outbox. Renderer only receives a CTA already assessed `CONSISTENT`; notifier does not perform independent discovery/trust decisions.

## DiscordAdapter — Phase 3
Server-opt-in only. Bot/app credentials, never user token. Use official REST/Gateway within installed permissions/intents. No automated user chat/activity.

Fallback: official outside-channel requirements remain Quest evidence even without live Discord progress.

## Source health

### HEALTHY
Expected fetch/heartbeat works and contract parses.

### DEGRADED
Rate limit, near/exceeded budget, transient provider issue, stale cursor/backfill gap, partial permission.

### DISABLED
Optional credentials absent, access revoked, parser quarantined after provider drift, or operator disabled.

### Fail-closed rule
If an ACTION requires currently unavailable mandatory verification/CTA evidence, suppress/downgrade action and schedule recheck rather than infer.

## Minimum-action rule
Adapter selection/cadence is deterministic scheduler configuration, not an LLM tool menu. Do not expose every adapter as peer callable to a central model.
