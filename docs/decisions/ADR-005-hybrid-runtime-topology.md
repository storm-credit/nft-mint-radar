# ADR-005 — Hybrid runtime topology class

## Status
Accepted in topology class. The deferred provider decision is **resolved**: `ADR-006` selected
Railway as the Phase 1 MVP runtime, and `ADR-010` froze the X mode without changing the provider
class. The deferral recorded below is historical.

## Context
Phase 1 may use either X Filtered Stream (persistent near-real-time connection) or Recent Search polling depending on the unresolved X cost/access spike. GitHub Actions schedule has a 5-minute minimum and official documentation warns scheduled jobs may be delayed or dropped during high load. The radar also requires durable cursors, deduplication and a notification outbox.

## Options considered
A. GitHub Actions cron only
B. Serverless scheduled functions only
C. Long-running worker only
D. Hybrid: low-latency ingestion runtime + PostgreSQL, with Actions/batch jobs for non-critical work

## Decision
Choose **D — Hybrid** as the topology class.

- PostgreSQL remains the durable state/outbox store.
- Low-latency/persistent ingestion runs outside GitHub Actions when required.
- GitHub Actions may run non-critical batch/reconciliation/eval/Dune tasks.
- If X ends as `SEARCH_PRIMARY`, the low-latency component may be serverless polling rather than a persistent worker.
- If X ends as `STREAM_PRIMARY`, use a persistent worker or webhook-capable always-on service.

## Why
This preserves the 10-minute alert SLO without coupling reliability to cron scheduling behavior, while avoiding a premature hosting-provider decision before X operational cost is known.

## Consequences
- GitHub Actions is not the primary real-time event runtime.
- Final hosting provider/cost decision was deferred here and has since been made: see `ADR-006`
  (Railway MVP runtime) and `ADR-010` (X mode frozen). This line is historical context, not a
  current blocker.
- Source adapters remain provider-neutral.
