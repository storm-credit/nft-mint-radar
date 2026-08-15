# SPIKE-RUNTIME-001 Result — Scheduler/runtime model

## Status
**PAPER_VALIDATED / FINAL_PROVIDER_CHOICE_DEPENDS_ON_X MODE**

No production code was written.

## Verified against current official GitHub documentation
- Scheduled GitHub Actions workflows have a minimum interval of 5 minutes.
- Scheduled workflows run from the default branch.
- Scheduled events can be delayed during periods of high load, especially near the start of an hour.
- Under sufficiently high load, queued scheduled jobs may be dropped.
- Public-repository scheduled workflows can be automatically disabled after 60 days of repository inactivity.

## Result
`GitHub Actions cron only` is **REJECTED** as the sole Phase 1 runtime for low-latency or persistent-stream sources.

It remains acceptable for:
- batch refreshes;
- low-urgency reconciliation;
- scheduled Dune refresh/read tasks;
- periodic maintenance/evals.

## Provisional topology decision
Use a **HYBRID** runtime contract:
- low-latency/persistent source ingestion: long-running worker or suitable always-on/serverless event path;
- durable state/outbox: PostgreSQL;
- batch/reconciliation: GitHub Actions may be used where timing is non-critical.

The exact low-latency provider is intentionally not chosen yet because X mode is unresolved:
- `STREAM_PRIMARY` requires a persistent connection or webhook-capable always-on endpoint;
- `SEARCH_PRIMARY` can tolerate a scheduled/serverless poller.

## Gate impact
Runtime topology class is resolved (`HYBRID`), but deployment provider selection is `BLOCKED_BY_X_SPIKE` and later cost comparison. This does not require production code now.
