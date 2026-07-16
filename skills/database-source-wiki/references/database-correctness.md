# Database Correctness Review

## Required distinctions

Never conflate:

- page latch and logical row/range lock;
- MVCC visibility and physical page state;
- undo and redo/WAL;
- redo/WAL and binlog/CDC;
- local and distributed atomicity;
- a prepare callback and durable recoverable prepared state;
- commit return and media durability;
- GTID table, global executed set, relay position, and application data;
- at-least-once replay, idempotent transformation, and exactly-once outcome;
- source inspection and runtime verification.

Similarly named features in MySQL, PostgreSQL, DuckDB, ClickHouse, TiDB, StarRocks, or other systems do not imply identical semantics.

## Correctness-sensitive page requirements

State:

1. Statement and transaction boundaries.
2. Isolation/consistency model and visibility rules.
3. Thread, task, worker, and ownership model.
4. In-memory and persistent state.
5. WAL/data/metadata/replica ordering and durability points.
6. Acknowledgement point.
7. Concurrency, lock ordering, deadlock, cancellation, and timeout behavior.
8. Crash, retry, duplicate delivery, partial failure, stale read, and failover behavior.
9. Recovery/rollback behavior and unknown outcomes.
10. Source anchors, tests, observability, and missing evidence.

## Failure Matrix

Every transaction, replication, CDC, DDL, failover, or recovery flow must include or link to a failure matrix:

| Failure Point | Memory State | Durable Data | Progress/Metadata | Restart Behavior | Retry/Idempotency | Evidence | Status |
|---|---|---|---|---|---|---|---|

Place rows at real source boundaries. Do not assign a fault-injection test to a nearby but different window. Split compound progress into distinct durable states.

## Evidence language

Use:

- “The source orders A before B.”
- “The implementation attempts bounded replay under conditions X.”
- “The test injects failure before function Y and does not cover substep Z.”
- “Not yet verified.”

Avoid without proof:

- exactly once;
- guarantees convergence;
- always durable;
- atomically commits across engines;
- crash safe;
- no duplicates;
- transparent compatibility.

## Performance pages

Separate write, storage, execution, transaction, and distributed paths. Require workload, dataset, concurrency, configuration, latency distribution, throughput, CPU, memory, I/O, cache, amplification, queueing, skew, and tail latency. Without measurements, provide a measurement plan rather than a result.
