# ADR-006 — Railway as MVP runtime target

## Status
Accepted for Phase 1 MVP target; account activation/spend not performed.

## Context
Phase 1 needs one deployment target that can support either X Filtered Stream (persistent connection) or Search polling, a background worker, environment secrets, outbound HTTP calls, and PostgreSQL-backed durable state/outbox.

GitHub Actions cron-only was already rejected as the sole low-latency runtime because scheduled workflows can be delayed or dropped.

## Options considered

### A. Cloudflare Workers + separate PostgreSQL
Pros:
- low minimum platform cost
- strong scheduled/event/serverless model

Cons:
- persistent streaming architecture is less straightforward than a normal long-running process
- requires a separate PostgreSQL provider and more operational split

### B. Fly.io Machines + PostgreSQL
Pros:
- low-cost persistent VM
- good fit for long-lived stream connections

Cons:
- more infrastructure choices/ops for a small personal MVP
- database operations/provider choice remains separate or self-managed

### C. Railway worker + Railway PostgreSQL — CHOSEN
Pros:
- one project can host application service/worker and PostgreSQL
- supports GitHub deploy or CLI later
- straightforward environment-variable/secrets model
- private networking between services
- works for both persistent stream and polling modes
- Hobby currently has a $5/month minimum commitment that counts toward resource usage
- usage hard limits can cap spend

Cons:
- PostgreSQL template is operationally unmanaged by Railway in the database-administration sense; backup/maintenance responsibility remains ours
- actual resource spend depends on CPU/RAM usage
- account/payment activation is external user action

### D. Render/other PaaS
Kept as fallback; no unique Phase 1 advantage was identified that justifies another provider dependency before live measurements.

## Decision
Use Railway as the **Phase 1 MVP runtime target** unless the X operational spike reveals a technical incompatibility.

Initial target topology:
- `radar-worker`: long-running service capable of stream or polling
- `PostgreSQL`: durable canonical state + outbox
- optional batch/reconciliation remains on GitHub Actions where timing is non-critical

## Cost guardrail
- target Hobby tier first
- current documented minimum: $5/month, applied toward resource usage
- configure Railway compute usage hard limit before production traffic
- no paid activation or deployment occurs during design/spike work without explicit user action/approval

## Consequences
- runtime packaging uncertainty is substantially removed before coding
- X final mode no longer changes the provider class, only worker behavior
- later migration remains possible because source adapters and persistence contracts are provider-neutral

## Revisit triggers
- X persistent stream cannot be maintained reliably
- measured monthly resource use exceeds budget materially
- outbound-network constraints appear on the selected account/tier
- managed database operations become necessary
