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

Current official pay-per-use contract observed 2026-08-29:
- public Post reads: `$0.005/resource` at the observed documentation revision;
- Pay-per-use Filtered Stream: available;
- Filtered Stream: up to 1,000 rules/project, 1 connection, core operators;
- official docs describe about 6–7 second P99 stream delivery;
- pay-per-use Post reads capped at 3,000,000/month before Enterprise (rechecked 2026-08-29);
- Bearer Token is sufficient for app-only public-data reads;
- prices remain revalidated against Developer Console before production budget decisions.

Operational mode **FROZEN** by `ADR-010` on measured evidence:

`STREAM_PRIMARY_WITH_SEARCH_RECOVERY`

Measured 2026-08-29 (`SPIKE-X-001`, total spend `$0.055`):
- Free-plan project returns 403 on both endpoints; Pay Per Use is required;
- Recent Search: HTTP 200 at 225.9 ms;
- Filtered Stream: 10 Posts in 16.9 s, delivery lag 4.3–5.1 s (mean ≈ 4.8 s), better than
  the documented ~6–7 s P99;
- temporary rule create/delete lifecycle succeeded with `cleanup_status: 200`.

Mandatory rule discipline, from `ADR-010`:
- production stream rules are **author-scoped** `from:` clauses over verified official accounts,
  with `-is:retweet -is:reply`;
- **broad keyword-only rules are forbidden**, including temporarily. Measured: a broad rule
  delivered ~35 Posts/min ≈ $250/day with useful 0 / noise 10;
- Recent Search is recovery/backfill advanced by `since_id`, never a polling discovery loop.

Signal ROI is **not** proven. Neither tested query shape produced an actionable mint signal.
If the author-scoped watchlist's measured useful/noise stays poor, the adapter degrades to
`X_OPTIONAL` under ADR-002 with no architecture change.

Budget rules:
- paid Post reads are counted from provider usage;
- hard daily/monthly source budget is deterministic configuration;
- budget exhaustion => `DEGRADED`, never surprise overspend;
- first operational spike was bounded to <=10 search Posts plus <=10 stream Posts and actually spent `$0.055` of a `$0.10` ceiling on 2026-08-29.

Use author-scoped verified-project-account rules in production; keyword-only rules are forbidden. A post from a verified official identity is not by itself proof that a newly introduced wallet-impacting CTA is safe.

Recent Search is the recovery/catch-up path for reconnect/backfill; it is not justification for broad repeated polling when Filtered Stream has better measured source ROI.

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

Credential model:
- disposable feasibility probe may use OpenSea instant free-tier key issuance;
- longer-lived production use may configure `OPENSEA_API_KEY`;
- no key is committed.

Mapping:
```text
OpenSea drop -> Project candidate + MintCampaign candidate
OpenSea stage -> MintStage
stage allocation/time/price/max -> stage-specific fields
relevant user action -> Opportunity referencing campaign/stage
```

Price mapping preserves FREE/KNOWN/UNKNOWN/VARIABLE and canonical payment asset (`NATIVE|ERC20|OTHER`).

Operational finding:
- provider chain keys `ethereum`, `base`, `robinhood` resolved live;
- structured multi-stage mapping succeeded;
- Base returned zero `upcoming` rows during a period with active Base mint surfaces.

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

Auth: `TELEGRAM_BOT_TOKEN`; target may be explicit or resolved during the disposable clean-bot spike after `/start`.

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
