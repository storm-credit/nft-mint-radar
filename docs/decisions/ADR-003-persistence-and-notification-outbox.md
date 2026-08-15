# ADR-003 — Persistence and Notification Outbox

## Status
Accepted

## Context
The radar needs immutable evidence, deterministic state transitions, deduplication, retries and reliable Telegram notifications. A file-only or stateless scheduler design would make corrections, conflicts and duplicate prevention fragile.

## Options considered

### A. JSON files in repository
Simple but unsuitable for concurrent state, evidence history and notification delivery.

### B. SQLite everywhere
Useful for local/dev fixtures, but weaker as the long-term shared runtime store.

### C. PostgreSQL-compatible relational store + transactional outbox — CHOSEN
Projects, Evidence, Opportunities, Notifications and progress use relational tables; source-specific metadata can use JSONB. Notification intent is written transactionally before provider delivery.

### D. Event-stream/Kafka architecture
Powerful but unnecessary for the first single-user deployment.

## Decision
- Production persistence semantics target PostgreSQL.
- Local/dev harness may use SQLite behind the same repository interfaces.
- Evidence is append-only.
- Provider RawEvents use deterministic idempotency keys.
- Telegram delivery uses a transactional outbox and stable notification fingerprint.
- Provider timeout after possible delivery is treated as ambiguous and reconciled conservatively; retries must not become message storms.

## Consequences
The runtime needs a persistent datastore even if the scheduler is serverless. GitHub Actions cron alone is not automatically selected; the runtime spike determines deployment topology.
