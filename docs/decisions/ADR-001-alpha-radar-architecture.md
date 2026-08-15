# ADR-001 — Alpha Radar architecture and phase boundaries

## Status
Accepted

## Context
The product must discover promising NFT opportunities early, especially before public mint, while later supporting allowlist tasks, Discord requirements, wallet intelligence and personalized progress. Implementing all phases at once would create unnecessary API, permission, security and validation complexity.

## Options considered
1. Simple Mint Radar — fastest, but poor evolvability.
2. Alpha Radar — discovery + verification + scoring + Telegram.
3. Alpha + Quest — add WL task parsing and effort tracking immediately.
4. Personal NFT Alpha Agent — full Discord/wallet/user-progress orchestration immediately.

## Decision
Implement Option 2 first. Preserve domain interfaces for Options 3 and 4.

Dune/on-chain wallet-cohort analysis is allowed as a narrow Phase 1.5 experiment because it strengthens discovery and verification without automating user accounts.

## Why
- delivers useful output earlier
- maintains source/evidence integrity
- avoids unsafe social/wallet automation
- prevents a later data-model rewrite
- allows source ROI measurement before adding more collectors

## Consequences
Phase 1 does not automatically perform X/Discord tasks or wallet actions. Phase 2 will parse allowlist/quest work. Phase 3 will integrate only permitted Discord read-side capabilities. Phase 4 will personalize eligibility/progress.

## Success criteria
Phase 1 is successful when it can produce a deduplicated Telegram alert for a high-priority candidate containing:
- project and opportunity identity
- source/evidence links
- quality/alpha/risk scores
- current mint/WL state
- why it matters
- next action
- KST deadline when known
- confidence and unresolved risks

No private key, wallet signature or user-account impersonation is ever required.
