# Wiki Architecture

## Layers

Use three logical layers:

1. Raw evidence: repository source/tests, upstream sources, design documents, and external references.
2. Synthesized knowledge: module pages, concepts, comparisons, and cross-module flows.
3. Navigation and governance: index, overview, reading guide, source catalog, log, templates, maintenance rules, and audit reports.

Raw evidence is read-only. The synthesized wiki is updated incrementally.

## Recommended structure

```text
wiki/
├── README.md
├── index.md
├── overview.md
├── reading-guide.md
├── log.md
├── AGENTS.md
├── assets/
├── modules/
├── cross-module-flows/
├── development/
├── reference/
├── templates/
├── reports/
└── legacy/
```

Split `modules/` into real knowledge domains such as server/SQL, storage engine, replication, distributed execution, or an embedded engine plugin. Make integration seams first-class modules: `handler`, transaction coordinator, catalog, RPC/exchange, or plugin API.

## Cross-module flows

Create independent pages for flows that cannot be understood inside one directory:

- query lifecycle;
- DML write and commit;
- DDL and metadata;
- WAL/redo and checkpoint recovery;
- binlog/replication apply;
- CDC and replay;
- startup/shutdown;
- failover/role change;
- backup/restore;
- distributed transaction;
- cancellation and timeout.

## Frontmatter

Material pages use:

```yaml
---
title: ""
domain: ""
type: module
status: draft
code_version: ""
last_verified: null
tags: []
sources: []
related: []
---
```

Define closed vocabularies for `domain`, `type`, and `status` in the wiki verification policy.

## Navigation

- `README.md`: human/agent entry point and scope.
- `index.md`: compact catalog with page, domain, type, status, summary, and verification date.
- `overview.md`: architecture and boundaries, not a page list.
- `reading-guide.md`: dependency-ordered paths for different roles.
- Parent `README.md`: responsibility, children, and reading order.
- `log.md`: append-only ingest/query/lint history.

Every material page must be reachable from the root through index, parent README, or another content page. Do not exempt every README from orphan detection.

## Phases

### P0

Governance, navigation, repository map, critical query/write/commit/recovery/plugin flows, correctness gaps, and audit tooling.

### P1

Optimizer/executor/storage depth, replication/DDL/observability, runtime tests, fault injection, and performance methodology.

### P2

HA, backup/restore, upgrade/migration, design-only extensions, graph/search, and scheduled lint.

Create pages only when they carry useful content. Represent later coverage in the index instead of empty files.
