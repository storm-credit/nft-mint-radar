# SPIKE-RUNTIME-001 Result — Scheduler/runtime model

## Status
**PAPER_VALIDATED / PROVIDER_TARGET_SELECTED / ACTIVATION_NOT_PERFORMED**

No production code was written and no hosting purchase/deployment was performed.

## Verified facts
### GitHub Actions
- scheduled workflows have a minimum interval of 5 minutes;
- scheduled events can be delayed during high load and queued jobs may be dropped;
- therefore cron-only Actions is rejected for low-latency/persistent ingestion.

### Railway
Current official Railway documentation confirms:
- application services and workers can be deployed from GitHub/CLI;
- PostgreSQL can be provisioned in the same project and exposed through `DATABASE_URL`/private networking;
- Hobby is currently $5/month minimum and that amount counts toward resource usage;
- resource pricing is usage-based;
- compute usage hard limits can shut workloads down at a configured ceiling to prevent runaway spend.

## Result
Runtime topology: **PASS**.
Concrete MVP provider target: **Railway** (ADR-006).

Target Phase 1 topology:
- `radar-worker`: Railway long-running service, able to support either X stream or polling mode;
- Railway PostgreSQL: canonical state + transactional notification outbox;
- GitHub Actions: non-critical batch/reconciliation/eval only.

## Why provider selection no longer depends on X mode
Railway can host a normal long-running process for `STREAM_PRIMARY` and can also run a polling worker for `SEARCH_PRIMARY`. X mode therefore changes worker behavior/cost, not the platform class.

## Cost guardrail
- begin with Hobby target;
- documented base/minimum: $5/month applied toward usage;
- configure compute hard limit before production traffic;
- no account activation/payment is required during current no-coding spike work.

## Residual operational evidence
Before production deployment:
- create/verify Railway account;
- confirm full outbound network access on selected tier/account;
- configure hard usage limit;
- perform a small outbound-provider connectivity test;
- measure one-week usage after first deploy and adjust resource limits.

## Gate impact
**Runtime provider-selection P0 blocker is resolved in design.**
Actual hosting activation is an implementation/deployment prerequisite, not a reason to keep Phase 1 architecture unresolved.
