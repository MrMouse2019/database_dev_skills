---
name: database-source-wiki
description: Use when designing, building, reviewing, migrating, or auditing a source-code knowledge wiki for a database kernel, storage engine, SQL engine, replication system, distributed database, or database plugin repository.
---

# Database Source Wiki

## Overview

Build a persistent, evidence-tracked wiki between raw sources and repeated code analysis. Organize knowledge around architectural boundaries and database lifecycles, not filenames alone.

## Required workflow

1. Inspect repository instructions, Git state, source layout, build/test systems, existing documentation, and upstream version before proposing structure.
2. Identify knowledge domains, integration boundaries, and cross-module flows. Propose 2–3 architectures and obtain approval before bulk creation.
3. Write a design and phased plan. Keep P0 useful: do not create empty placeholder trees.
4. Establish governance, templates, evidence states, navigation, source catalog, and maintenance rules before module pages.
5. Trace each material claim through current source. Treat external articles as explanation, not implementation proof.
6. Document normal, error, retry, crash, and recovery paths for correctness-sensitive flows.
7. Review each delivery for specification compliance and database correctness. Fix material findings before proceeding.
8. Run the audit tool and record static versus runtime evidence separately.

## Evidence contract

Use this precedence: current source/tests; version-matched upstream source/official docs; repository design docs; external articles.

Use page states consistently:

- `draft`: initial synthesis.
- `source-checked`: current source anchors and primary behavior inspected.
- `verified`: current source plus a named test/result or reproducible runtime check/result.
- `partial`: only explicitly identified behavior is verified.
- `design-only`: proposed, not implemented.
- `stale`: related source changed after verification.
- `deprecated`: superseded.

Never promote generated prose to `verified`. Separate facts, assumptions, hypotheses, recommendations, and known gaps.

## Load references

- Read [references/wiki-architecture.md](references/wiki-architecture.md) when designing directories, navigation, page schema, or phases.
- Read [references/database-correctness.md](references/database-correctness.md) before transaction, WAL/redo, replication, CDC, DDL, failover, recovery, concurrency, or persistent-format pages.
- Read [references/maintenance-workflows.md](references/maintenance-workflows.md) when ingesting sources, answering from the wiki, migrating legacy docs, or auditing it.

Copy and adapt templates from `assets/`; do not edit the originals in place.

## Audit

Run:

```bash
python3 <skill>/scripts/audit_wiki.py --wiki <wiki-directory>
```

The audit is static evidence only. It must not be reported as a successful build, MTR, crash test, benchmark, or runtime verification.

## Delivery contract

Report:

- architecture and scope;
- pages and flows created;
- source and version evidence;
- static audit result;
- build/test/runtime commands actually executed;
- unverified correctness and performance gaps;
- legacy debt and migration status.

Do not claim completion without fresh audit output and an explicit requirements check.
