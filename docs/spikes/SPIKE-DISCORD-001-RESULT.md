# SPIKE-DISCORD-001 Result — permitted Discord intelligence

## Status
**PAPER_VALIDATED / OPERATIONAL_SERVER_OPT_IN_REQUIRED**

No production code was written.

## Verified against current official Discord documentation
- Bots/apps require installation/authorization for a server context.
- `GUILD_MEMBERS` is a privileged intent and is relevant to member/role information.
- `MESSAGE_CONTENT` is a privileged intent and affects message content, embeds, attachments and components.
- Privileged intents must be enabled; verified/verification-eligible apps require approval under Discord's current policy.
- REST endpoints can also be restricted by privileged-intent requirements.
- User-installed apps do not gain arbitrary server read access; server-installed apps require server authorization/permissions.

## Result
Phase 3 arbitrary third-party Discord surveillance: **NOT FEASIBLE / NOT ALLOWED BY DESIGN**.
Authorized server read-side intelligence: **FEASIBLE**.

## Decision
Phase 3 mode = `SERVER_OPT_IN / PARTIAL`.

Allowed:
- bot installed by an authorized server administrator/member with required permissions;
- read configured announcement channels where permitted;
- read role/member state when the required intent and server access are authorized;
- parse publicly disclosed Discord requirements from official sites/Galxe/Guild even when no bot access exists.

Not allowed:
- self-bots/user tokens;
- automated user chat/activity;
- assuming access to NFT Discords where the bot was not installed;
- making Phase 1 depend on Discord bot coverage.

## Gate impact
Not required for Phase 1. Phase 3 remains optional and server-opt-in.
