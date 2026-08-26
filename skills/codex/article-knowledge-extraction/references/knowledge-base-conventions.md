# knowledge_base conventions for Codex

Read this file completely before running `article-knowledge-extraction`. The knowledge base's own `AGENTS.md` has higher priority.

## Repository and serialization

- Canonical checkout: `/Users/zhangxiahao/Desktop/projects/knowledge_base`.
- `articles/` stores source notes for external articles or conference material. A source note proves only what its source states.
- `concepts/` stores reusable mechanisms, trade-offs, and validation questions across sources.
- `index.md`, `concepts/index.md`, and actual directory indexes are navigation entry points.
- `sync/validate_knowledge_base.py` is the static validator.
- Never create a knowledge-base worktree. A tracked change, non-ignored untracked path, or unrelated non-default branch in the canonical checkout blocks the entire task.

Before article acquisition, read the repository instructions and indexes, then run:

```bash
git status --short --branch
```

The `##` line identifies the branch. Any other staged or unstaged tracked status and any `??` non-ignored untracked status requires refusal. Git-ignored files do not appear in ordinary status output and are not blockers. List blockers, then stop without stashing, cleaning, moving, restoring, committing, fetching the article, or bypassing the checkout.

On a clean `main`/`master`, create `docs/<core-topic>` with at most five lowercase English words joined by hyphens. Continue on a non-default branch only when it is demonstrably for the same article task; otherwise stop.

## Evidence vocabulary

Use only statuses supported by the repository:

| Value | Use |
|---|---|
| `source-fact` | Fact directly located in source code at a fixed version |
| `official-doc` | An authoritative publisher's documentation about its own system or product |
| `paper-claim` | A paper author's statement or experiment |
| `user-confirmed` | Information the user confirmed but this task did not independently verify |
| `inference` | A conclusion derived from listed evidence |
| `unverified` | Source class or conclusion cannot be established |
| `source-index` | Source index page |
| `conference-summary` | Conference, case-study, or third-party retelling |
| `technical-analysis` | Mechanism or design analysis synthesized from sources |
| `runtime-verified` | Fact with the actual runtime verification scope and result reported |

For a source note, use `official-doc` only for the publisher's own authoritative documentation, `conference-summary` for a conference/case-study retelling, and `unverified` when the class cannot be established. A concept commonly uses `technical-analysis`, but each statement still needs its own evidence boundary. A page-level status does not upgrade every statement on the page.

## Source-note shape

Preserve the ordering and formatting of adjacent pages. A new source note includes at least:

```yaml
---
title: "Article title"
domain: database-architecture
type: source-note
status: draft
code_version: "not-applicable"
last_verified: null
tags:
  - keyword
sources:
  - "Publisher, available date, canonical URL"
traceability:
  source_url: "https://canonical.example/article"
  source_title: "Article title or unavailable"
  source_author_or_publisher: "Author or publisher or unavailable"
  source_published_or_edited_at: "Available date or unavailable"
  codex_task_id: "<current Codex session ID>"
  codex_task_title: "unavailable"
  codex_task_share_url: "unavailable"
related:
  - "concepts/example.md"
evidence_status: unverified
updated_at: YYYY-MM-DD
---
```

Use repository-supported field names when neighboring pages establish a different schema; preserve the same semantic values rather than introducing duplicate aliases.

Organize the body as:

1. `> [!warning] Evidence boundary`;
2. one-sentence conclusion;
3. source, background, and scale context;
4. mechanisms, architecture, and data flow organized by `core_keywords`;
5. article claims and quantitative conditions;
6. transferable knowledge;
7. claims that cannot be transferred directly;
8. follow-up validation;
9. related concepts and traceability.

Keep only short excerpts needed for evidence location. Do not reproduce the complete copyrighted article.

## Concept pages

Preserve an existing concept's structure and terminology. A new concept includes at least:

```yaml
---
title: "Concept title"
domain: database-architecture
type: concept
status: draft
code_version: "not-applicable"
last_verified: null
tags:
  - keyword
sources:
  - "articles/source-note.md"
  - "Publisher and canonical URL"
traceability:
  source_url: "https://canonical.example/article"
  codex_task_id: "<current Codex session ID>"
  codex_task_title: "unavailable"
  codex_task_share_url: "unavailable"
related:
  - "concepts/related.md"
evidence_status: technical-analysis
updated_at: YYYY-MM-DD
---
```

Cover the conclusion, general mechanism, applicability conditions, trade-offs, correctness and failure-semantics questions, performance validation questions, source conditions that cannot be accepted directly, and source boundaries. Add every new concept to navigation and add reverse links to directly related pages following repository style.

Create no concept page when the article has insufficient reusable knowledge. Do not target a fixed page count.

## Codex traceability boundary

Always record the canonical source URL and source metadata available from the article. During actual Codex execution, proactively obtain the current session/task ID from the current runtime task/session context—the same value exposed by Codex’s **Copy session ID** action—even when the prompt does not contain it. Record traceability with the repository-supported fields:

- `codex_task_id`: required; write the exact current Codex session/task ID;
- `codex_task_title`: write the runtime-exposed title or `unavailable`;
- `codex_task_share_url`: write the runtime-exposed share URL or `unavailable`.

Never replace `codex_task_id` with a new `codex_session_id` alias. If actual Codex execution cannot obtain the current ID from the runtime, stop before knowledge-base writes and report the blocker; do not degrade the required ID to `unavailable`. A plan, dry run, or test premise may state that runtime metadata is unavailable, but a later actual execution must retrieve its own current ID. Never inspect `~/.codex`, application databases, task histories, logs, caches, hidden files, environment secrets, or other private stores to infer a value. Never invent a convenient title or derive a share URL. User-supplied values may be recorded only with their provenance clear.

Do not commit runtime databases, task files, logs, credentials, tokens, or acquisition caches to the knowledge base. Concept pages copy the same exposed traceability values from their source note when the adjacent schema requires standalone traceability.

## Links and protected paths

- Follow neighboring pages for relative Markdown links or Obsidian links.
- Put the canonical URL in every source note and directly sourced concept page.
- Add new pages to `index.md` and the actual directory indexes; avoid orphan pages.
- Modify only task-owned source, concept, reverse-link, and navigation paths.
- Do not modify `feishu/`, `sync/feishu-manifest.json`, or generated `graphify-out/`.

## Validation and local commit

Run from the knowledge-base root:

```bash
python3 -B sync/validate_knowledge_base.py
git diff --check
```

Report the validator's exact output; never prefill changing counts. Static checks do not prove source-version semantics, runtime behavior, crash recovery, fault handling, or benchmark performance.

Before committing:

```bash
git status --short
git diff -- <explicit-task-paths>
git add <explicit-task-paths>
git diff --cached --check
git diff --cached --stat
```

Never use `git add .`. The index must contain only task files. Create one local commit with an English Conventional Commit message beginning `docs:`. Read it back with:

```bash
git show --stat --oneline --decorate -1
git status --short --branch
```

The normal successful outcome includes this local commit. It does not include push, PR creation, or publication. Perform none of those actions without a separate explicit user request.

## Final report

Report in order:

1. source note create/update and actual path;
2. existing concepts updated and concepts created, including none;
3. navigation and reverse-link changes;
4. each validation command and exact result;
5. branch and commit SHA;
6. article claims, inference, unknowns, and independently verified facts;
7. source/runtime/failure/performance checks not run;
8. explicit confirmation that no push or PR was performed.

On refusal or acquisition failure, report only completed read-only checks, the blocking state, and zero-write/zero-commit facts.
