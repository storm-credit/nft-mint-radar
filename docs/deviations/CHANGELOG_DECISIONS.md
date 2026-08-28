# Plan Deviations / Decision Change Log

Use this file only when implementation/spike work materially differs from the accepted plan or ADR.

## Entry template

### YYYY-MM-DD — <short title>
- Original plan:
- Actual change:
- Why:
- Evidence:
- Impact:
- Compatibility/migration impact:
- Follow-up:
- ADR required: YES/NO

---

## Current entries

### 2026-08-28 — OpenSea spike no longer requires user API-key setup
- Original plan: obtain/configure `OPENSEA_API_KEY` before the live marketplace spike.
- Actual change: the disposable probe first checks for a configured key, then uses OpenSea's instant free-tier key issuance when absent. The key stays only in process memory and is never printed.
- Why: provider capability allowed a smaller user-action/credential surface and removed an unnecessary blocker.
- Evidence: GitHub Actions runs `33171614678` and `33171764870`; instant-key HTTP 201; live chain/drop/detail calls succeeded.
- Impact: `SPIKE-MARKET-001` was completed without user-owned OpenSea credentials. A long-lived production key remains a later deployment concern, not a Phase 1 design/spike blocker.
- Compatibility/migration impact: none to domain contracts; disposable runner and credential-readiness docs changed.
- Follow-up: keep OpenSea smoke manual-only for targeted revalidation; production auth method is selected at deployment time within the existing adapter contract.
- ADR required: NO — existing adapter/ADR boundaries already permit auth-mode refinement.

### 2026-08-28 — Telegram spike reduces user setup to token + /start
- Original plan: user provides both `TELEGRAM_BOT_TOKEN` and a resolved `TELEGRAM_CHAT_ID` before the delivery spike.
- Actual change: `TELEGRAM_CHAT_ID` became optional. A clean test bot can resolve the latest private chat through `getUpdates` after the user sends `/start`; webhook-configured bots fail closed instead of being modified.
- Why: reduce unnecessary manual configuration while preserving permission/safety boundaries.
- Evidence: updated disposable probe and guarded GitHub Actions smoke `33172110528`; the readiness check proved the current blocker is specifically an absent `TELEGRAM_BOT_TOKEN`, and no network send occurred.
- Impact: exact user prerequisite is now only bot creation, one GitHub secret, and `/start`.
- Compatibility/migration impact: none; explicit `TELEGRAM_CHAT_ID` remains supported.
- Follow-up: after the token is configured and `/start` sent, rerun the manual Telegram spike and record provider delivery evidence.
- ADR required: NO — notifier architecture is unchanged.
