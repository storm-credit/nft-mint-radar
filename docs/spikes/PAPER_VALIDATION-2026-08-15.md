# Provider Paper Validation — 2026-08-15

## Purpose
Record facts verified from current first-party documentation before credentialed spikes. This is **not** a substitute for operational spikes because pricing, account access, latency and permissions must be tested in the actual environment.

## X API
Official docs reviewed:
- https://docs.x.com/x-api/fundamentals/rate-limits
- https://docs.x.com/x-api/posts/filtered-stream/introduction
- https://docs.x.com/x-api/fundamentals/post-cap

Confirmed:
- recent search exists;
- filtered stream exists and delivers matching posts near real time;
- current docs list one pay-per-use stream connection and up to 1,000 rules;
- rate limits and billing are separate;
- pricing can vary by endpoint/operation and current price must be checked in Developer Console;
- spending limits/budget controls are part of the current usage model.

Design implication:
Do not hard-code X pricing or assume streaming is affordable. `SPIKE-X-001` remains mandatory.

## OpenSea
Official docs reviewed:
- https://docs.opensea.io/reference/get_drops
- https://docs.opensea.io/docs/mint-from-a-drop
- https://docs.opensea.io/reference/api-overview

Confirmed:
- `GET /api/v2/drops` can query `upcoming` drops and filter chains;
- drop details can include stages, price, start/end, supply/max-per-wallet information;
- API-key auth is supported;
- marketplace/event APIs exist;
- provider also exposes transaction-building endpoints, which are explicitly out of project scope.

Design implication:
OpenSea is a supported Phase 1 structured discovery adapter for Ethereum/Base, subject to coverage spike.

## Galxe
Official docs reviewed:
- https://docs.galxe.com/galxe-integration/api-reference/quest
- https://docs.galxe.com/galxe-integration/getting-started/quick-start
- https://docs.galxe.com/quest/graphql-api/overview/authentication

Confirmed:
- GraphQL Quest API exposes quest metadata/status/start/end/cap/participants;
- credential groups can represent eligibility/condition relations;
- user-specific eligibility can be queried when address/context is supplied;
- API access token is generated in Galxe settings and must be stored as secret;
- docs recommend caching and handling rate limits.

Design implication:
Galxe is a strong structured Phase 1/2 source. Claim/mutation flows are excluded from this radar.

## PREMINT
Official pages reviewed:
- https://www.premint.xyz/connect/
- https://creators.premint.xyz/

Confirmed:
- PREMINT Connect advertises programmatic endpoints such as project info, list and wallet status;
- Connect partner API key access requires an application/onboarding process;
- project creators can enforce NFT ownership, X follow, ETH balance, Discord membership/role/join-date, reCAPTCHA, raffle and custom-field requirements.

Design implication:
PREMINT is valuable but must remain optional until access is validated. No protected scraping fallback.

## Guild
Official docs reviewed:
- https://docs.guild.xyz/guild/how-to-setup-requirements
- https://docs.guild.xyz/guild/how-guild-works

Confirmed:
- Guild requirements support ALL, meet-one and X-of-Y logic;
- requirement classes include on-chain, X/social, Discord role, Guild activity and time-based conditions;
- roles/rewards depend on those requirements.

Design implication:
Canonical Quest schema must preserve logical condition trees. Exact supported programmatic read surface remains for `SPIKE-CAMPAIGN-001`.

## Dune
Official docs reviewed:
- https://docs.dune.com/api-reference/executions/endpoint/get-query-result
- https://docs.dune.com/api-reference/executions/endpoint/execute-query
- https://docs.dune.com/api-reference/executions/filtering
- https://docs.dune.com/api-reference/overview/getting-started

Confirmed:
- saved queries/SQL can be executed asynchronously;
- latest query results can be fetched without executing a new query;
- latest-result retrieval still consumes credits based on result size;
- execution consumes credits based on actual compute resources;
- server-side result filtering/column selection/pagination are available;
- execution status can expose execution cost credits.

Design implication:
Use cached/latest results for frequent reads when freshness allows and reserve fresh executions for scheduled/on-demand analytics. Final cadence/cost remains `SPIKE-DUNE-001`.

## Discord
Official docs reviewed:
- https://docs.discord.com/developers/events/gateway
- https://docs.discord.com/developers/resources/message
- https://docs.discord.com/developers/platform/bots

Confirmed:
- official bots use Gateway and/or REST;
- MESSAGE_CONTENT is a privileged intent for message contents;
- GUILD_MEMBERS is privileged for member-related access;
- bot/app installation in a server and permissions are required;
- arbitrary third-party server read access cannot be assumed.

Design implication:
Phase 3 Discord intelligence is SERVER_OPT_IN with manual/official-source fallback. No self-bot/user-token path.

## Telegram Bot API
Official docs reviewed:
- https://core.telegram.org/bots/api

Confirmed:
- `sendMessage` sends text to a target chat and returns a Message on success;
- text is limited to 1–4096 characters after entity parsing.

Design implication:
MVP notifier can use `sendMessage`; actual bot/chat setup and ambiguous network retry behavior remain `SPIKE-TG-001`.

## Paper validation verdict
No first-party documentation finding invalidates the current provider-neutral architecture.

The strongest design adjustments confirmed are:
1. OpenSea upcoming-drop API can be a real structured P0 source.
2. Galxe can provide structured Quest/eligibility data.
3. PREMINT cannot be assumed freely accessible programmatically.
4. Discord cannot be treated as universally readable.
5. X cost must be measured rather than assumed.
6. Dune should favor cached/latest reads plus targeted executions.
