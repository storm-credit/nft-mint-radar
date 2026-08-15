# SPIKE-CAMPAIGN-001 Result — PREMINT / Galxe / Guild

## Status
**PAPER_VALIDATED / MIXED_OPERATIONAL_ACCESS**

No production code was written.

## Galxe
Current official Galxe documentation confirms a supported GraphQL Quest API with quest status, start/end timestamps, participant counts and user-specific credential/eligibility data. API calls use an `access-token` generated in Galxe settings.

Decision: `API` adapter candidate. Operational query remains blocked until a token is configured outside the repository.

## PREMINT
Official PREMINT Connect documents `get_project_info`, `get_list`, and `check_wallet`, including registration dates, eligibility requirements and winner/waitlist/registered states. PREMINT Connect requires partner API-key approval and currently states onboarding may take 1–2 weeks.

Decision: `OPTIONAL_API`. PREMINT must not be a hard Phase 1 dependency. Without partner access, use official project/PREMINT references as evidence/manual deep links; do not scrape protected data.

## Guild
Official Guild documentation confirms rich requirement trees and AND/OR/X-of-Y logic across wallet, X, Discord, points, time and other conditions. The currently verified official documentation did not expose a stable general public read API contract suitable for this product.

Decision: `PUBLIC_REFERENCE_ONLY` initially. Add an API adapter only after an official supported read interface is operationally confirmed.

## Result
Campaign architecture: **PASS** because no provider is mandatory.
- Galxe = API-capable but credential-blocked.
- PREMINT = optional partner API.
- Guild = structured requirement source conceptually, public-reference/manual fallback until official programmatic access is confirmed.

## Gate impact
Phase 1 can proceed without PREMINT/Guild programmatic access if Galxe/OpenSea/official channels cover the structured path and campaign adapters degrade safely.
