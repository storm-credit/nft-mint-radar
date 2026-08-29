# Credential Readiness

## Purpose
List the minimum user-owned credentials/configuration still required to finish Phase 1 operational validation.

## Current blocker count
**Zero.** No Phase 1 provider validation remains, and no user-owned credential is outstanding.

OpenSea, Telegram and X are all closed. Both configured secrets, `TELEGRAM_BOT_TOKEN` and
`X_BEARER_TOKEN`, have been exercised against live providers.

What remains below is optional/manual recheck material and later-phase credentials, not a blocker.

---

## 1. Telegram — CLOSED 2026-08-29

### Exact user action
1. In Telegram, create a bot with `@BotFather` using `/newbot`.
2. In repository `storm-credit/nft-mint-radar` add an Actions secret:
   - name: `TELEGRAM_BOT_TOKEN`
   - value: the BotFather token
3. Open the created bot and send `/start` once.

Do **not** paste the token into chat, issues, commits, files, or logs.

### What you do NOT need to do
- no OpenSea key;
- no Telegram chat-id lookup in the normal clean-bot case;
- no wallet connection;
- no Telegram webhook configuration.

### Why chat id is optional
If `TELEGRAM_CHAT_ID` is absent, the disposable probe:
1. verifies the bot has no conflicting webhook;
2. calls `getUpdates`;
3. selects the latest private chat created by `/start`;
4. sends one Korean dry-run.

If the bot already has a webhook, use a clean test bot or configure `TELEGRAM_CHAT_ID` explicitly; the spike will not silently remove a webhook.

### Current observed state
Run `33255435740` on 2026-08-29 delivered a real Korean dry-run to `@nftmr_bot`:
HTTP 200, `message_id 4`, 467.8 ms, chat auto-resolved, `chat_id_matches true`, no CTA.
No further Telegram setup is required.

See `docs/spikes/SPIKE-TG-001-RESULT.md`.

---

## 2. X — CLOSED 2026-08-29

### Current public contract already resolved
Current official X documentation observed 2026-08-29 states:
- public Post read: `$0.005/resource`;
- Pay-per-use Filtered Stream available;
- Filtered Stream: 1,000 rules/project, 1 connection;
- approximate 6–7 second P99 delivery;
- pay-per-use monthly cap: 3,000,000 Post reads (rechecked 2026-08-29);
- Bearer Token supports app-only public reads.

So the old paper-pricing ambiguity is closed.

### Exact user action
1. Sign in to the X Developer Console.
2. Create/enable a developer Project + App for read-only public-data use.
3. Ensure sufficient API credit for the bounded spike. The designed Post-read ceiling is **$0.10 at the currently documented rate**; the console remains the execution-time authority.
4. Generate/save the app Bearer Token.
5. Add repository Actions secret:
   - name: `X_BEARER_TOKEN`
   - value: the Bearer Token

Do not paste the Bearer Token into chat.

### What happens next
The manual `x` spike still refuses to run without the exact confirmation:

`I_UNDERSTAND_X_MAY_COST`

Bounded `both` mode:
- Recent Search <=10 Posts -> current read-cost ceiling `$0.05`;
- Filtered Stream <=10 Posts -> current read-cost ceiling `$0.05`;
- total Post-read ceiling `$0.10` at the current public rate.

The stream leg refuses to run if the project already has Filtered Stream rules, preventing unrelated rules from creating additional test reads.

### Final observed state — CLOSED
`X_BEARER_TOKEN` is configured and the App is attached to the `NFT Mint Radar` **Pay Per Use**
project. Run `33255955730` returned Recent Search HTTP 200 at 225.9 ms, and run `33256021263`
delivered 10 Filtered Stream Posts in 16.9 s with a clean rule create/delete cycle. Total actual
spend `$0.055` of a `$0.10` ceiling.

One measured constraint is permanent and worth keeping visible: the **Free plan returns 403
`client-not-enrolled` on both endpoints and cannot serve this product**. Run `33255336140` proved it
at `$0.00`, because a rejected call returns no Posts.

**No user action remains.** If the token is ever rotated, update the secret and rerun the bounded
spike; that is maintenance, not a blocker.

See `docs/spikes/SPIKE-X-001-RESULT.md` and `ADR-010`.

---

## OpenSea — CLOSED
No user setup required for Phase 1 feasibility.

Live GitHub Actions validation established:
- instant free key issuance;
- Ethereum/Base/Robinhood chain resolution;
- real drop/stage detail mapping;
- multi-stage GTD/FCFS/holder/free/public structures;
- OpenSea `upcoming` is incomplete coverage and cannot be the sole discovery authority.

A persistent `OPENSEA_API_KEY` may later be used in production, but it is not a current blocker.

---

## Optional/later credentials

### Galxe
- `GALXE_ACCESS_TOKEN`
- needed only before enabling the adapter in production.

### PREMINT
Partner/API access optional; do not block Phase 1.

### Guild
Keep public-reference/manual path until a supported read contract is operationally validated.

### Dune — Phase 1.5
- `DUNE_API_KEY`

### Discord — Phase 3
- `DISCORD_BOT_TOKEN`
- server installation + required permissions/intents

---

## Safety rules
- never paste secrets into chat/repository/issues/PRs/logs;
- never commit `.env`;
- rotate any accidentally exposed credential;
- spike artifacts retain measurements, not token values;
- credentials grant read-only/minimum authority required for each spike.
