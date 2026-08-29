# Credential Readiness

## Purpose
List the minimum user-owned credentials/configuration still required to finish Phase 1 operational validation.

## Current blocker count
Only **two** Phase 1 provider validations remain:
1. Telegram real delivery
2. X credentialed bounded trial

OpenSea is closed and requires no current user setup.

---

## 1. Telegram — do this first

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
Guarded GitHub Actions smoke reobserved on 2026-08-29 (run `33252936929`, earlier run `33172110528`):
- `TELEGRAM_BOT_TOKEN`: absent
- delivery step: skipped
- network send attempted: false

Repository Actions-secret enumeration on 2026-08-29 returned zero secrets and zero environments.

See `docs/spikes/SPIKE-TG-001-RESULT.md`.

---

## 2. X — do after Telegram

### Current public contract already resolved
Current official X documentation observed 2026-08-29 states:
- public Post read: `$0.005/resource`;
- Pay-per-use Filtered Stream available;
- Filtered Stream: 1,000 rules/project, 1 connection;
- approximate 6–7 second P99 delivery;
- pay-per-use monthly cap: 2,000,000 Post reads;
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

### Current observed state
No-cost GitHub Actions preflight on 2026-08-29 (runs `33245992097` and `33252938234`) observed:
- `spikes/x_probe.py`: compile PASS
- `X_BEARER_TOKEN`: absent
- paid API call attempted: false

Repository Actions-secret enumeration on 2026-08-29 returned zero secrets and zero environments.

See `docs/spikes/SPIKE-X-001-RESULT.md`.

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
