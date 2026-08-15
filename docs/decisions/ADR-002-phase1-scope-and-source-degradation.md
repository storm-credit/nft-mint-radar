# ADR-002 — Phase 1 Scope and Source Degradation

## Status
Accepted

## Context
NFT discovery sources differ in access, cost, reliability and trust. X pricing/access, PREMINT partner access, Dune credits and Discord permissions can change or be unavailable. Making any one optional provider a mandatory runtime dependency would create architecture churn and unsafe fail-open behavior.

## Options considered

### A. X-centric monolith
Make X the primary required feed and add others around it.
- Pros: strong early social coverage.
- Cons: cost/access concentration, misses structured/on-chain sources.

### B. Marketplace-centric MVP
OpenSea + official sites only.
- Pros: simple, supported APIs.
- Cons: late for WL/social tasks.

### C. Pluggable multi-source core with graceful degradation — CHOSEN
Canonical event/evidence models are provider-neutral. Adapters can be HEALTHY/DEGRADED/DISABLED. Action verification fails closed when mandatory evidence is unavailable.
- Pros: resilient, supports future sources, avoids provider lock-in.
- Cons: more design structure.

### D. Scrape-everything aggregator
Bypass missing APIs through page scraping/user-account automation.
- Pros: apparent coverage.
- Cons: brittle, security/ToS/account risk; rejected.

## Decision
- Initial chain scope: Ethereum + Base.
- Phase 1 P0 structured sources: official sites/docs, OpenSea drops, Galxe, on-chain provider; official X is P0 when access/budget permits but degrades cleanly.
- PREMINT/Guild/Dune/Telegram-source are optional adapters until their spike/access contracts are resolved.
- Reddit/generic Telegram/influencers are discovery-only weak signals.
- Discord live intelligence is Phase 3 and server-opt-in; no arbitrary-server assumption.
- Missing verification evidence suppresses/downgrades action rather than failing open.

## Consequences
Provider choices can change after spikes without changing core domain entities. Coverage may temporarily reduce when an adapter is disabled, but safety/verification semantics remain stable.
