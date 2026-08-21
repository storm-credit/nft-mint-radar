# Eval Fixtures v1.1 Addendum

These fixtures are mandatory before the executable harness runner can be considered frozen after ADR-007/ADR-008.

## F21 — Multi-stage GTD / FCFS / Public
Input: one verified drop with GTD, FCFS and Public stages, each with distinct limits and prices.
Expected:
- one MintCampaign;
- three MintStage objects;
- three distinct stage-scoped Opportunities when user actions differ;
- no stage field overwrites another.
Forbidden:
- collapsing all stages into one price/deadline.

## F22 — ERC-20-priced mint
Input: verified Robinhood Chain mint paid in an ERC-20 token.
Expected:
- `price_state=KNOWN`;
- AssetAmount identifies ERC20 and chain;
- USD estimate may be displayed separately.
Forbidden:
- storing amount as `mint_price_native`;
- inferring token solely from `$` display text.

## F23 — Explicit free mint
Input: official stage says Free.
Expected:
- `price_state=FREE`;
- canonical price may be null/zero only under explicit FREE state;
- gas/network cost is not described as mint price.
Forbidden:
- changing UNKNOWN price to FREE.

## F24 — Compromised official social CTA
Input:
- previously verified project X identity;
- new urgent mint post links an unseen domain;
- canonical website has not changed and does not link the new domain.
Expected:
- source identity remains T1/official;
- action link safety becomes QUARANTINED;
- WARNING or WATCH only;
- no wallet-impacting CTA.
Forbidden:
- APPLY_WL/MINT_RECHECK clickable CTA merely because X identity is official.

## F25 — Official compromise recovery/disavowal
Input:
- canonical project website or restored social account disavows F24 link.
Expected:
- malicious link REVOKED;
- prior evidence retained;
- risk event emitted;
- only newly corroborated official URL may become CTA-safe.

## F26 — Legacy collection reactivation / chain migration
Input:
- old NFT project resumes official activity;
- announces a new collection or migration on another Phase 1 chain;
- legacy/early holders get priority registration.
Expected normalized events:
- PROJECT_REACTIVATED
- CHAIN_MIGRATION_ANNOUNCED when applicable
- LEGACY_HOLDER_ACCESS_ANNOUNCED
Expected action:
- WATCH or APPLY_WL depending on current registration evidence and snapshot timing.
Forbidden:
- treating legacy project age alone as Quality proof;
- recommending purchase of legacy NFT after a passed snapshot.

## F27 — Shared launchpad factory
Input:
- two unrelated NFT projects deployed by same known factory;
- distinct creators/owners.
Expected:
- factory relationship stored separately;
- projects not merged;
- no creator-quality bonus/penalty from shared factory alone.

## F28 — OpenSea absent but official mint exists
Input:
- verified official project/campaign/on-chain mint evidence;
- project absent from OpenSea Drops calendar.
Expected:
- opportunity remains valid;
- OpenSea absence is `NO_DATA`, not negative verification evidence.
Forbidden:
- suppressing candidate solely for missing OpenSea calendar entry.

## Acceptance
Runner freeze requires all F21–F28 to have expected normalized outputs and forbidden-output assertions.
