---
name: article-knowledge-extraction
description: Use when a user supplies an external article URL and core keywords and asks to summarize the article, extract reusable database-engineering knowledge, or preserve it in the local knowledge_base.
---

# Article Knowledge Extraction

## Overview

Read `article_url` around `core_keywords`, return an evidence-bounded summary, and preserve the smallest reusable result in `/Users/zhangxiahao/Desktop/projects/knowledge_base`. Treat that canonical checkout as the serialization point and create one local commit after validation. Do not push or create a PR.

Before acting, read [knowledge-base-conventions.md](references/knowledge-base-conventions.md) completely. The target repository's `AGENTS.md` overrides this reference.

## Required inputs

Require exactly these inputs:

- `article_url`: the canonical article URL supplied by the user;
- `core_keywords`: one or more non-empty reading focuses.

If either is missing and cannot be inferred safely, ask one concise question before fetching or writing. Do not guess a URL from search results or expand the keywords into unsupported claims.

## Workflow

Follow this order exactly.

### 1. Gate the canonical checkout before acquisition

First classify the request:

- For a plan, dry run, or test scenario, treat explicitly supplied repository-state premises as facts for that scenario. Do not replace them with the current live checkout state, and do not perform live article acquisition or knowledge-base mutation while answering the scenario. If a premise states any blocking dirty state or an unrelated non-default branch, return the refusal plan immediately; non-overlapping paths do not permit continuation. State that a later actual execution must verify the live checkout again.
- For actual execution, supplied premises are not verification. Perform the live repository reads and `git status --short --branch` gate below, and decide from those observed results.

Use only `/Users/zhangxiahao/Desktop/projects/knowledge_base`. Never create or use a knowledge-base worktree.

Before invoking any article skill, connector, CLI, browser, or search:

1. Read the canonical checkout's `AGENTS.md`, `README.md`, `index.md`, and existing `articles/` and `concepts/` indexes.
2. Run `git status --short --branch` there.
3. Refuse the whole task if any staged or unstaged tracked change or non-ignored untracked path exists. List blocking paths. Do not fetch the article, stash, clean, delete, move, restore, commit, or decide that non-overlapping files make continuation safe.
4. Refuse the whole task on a non-`main`/`master` branch unless it is demonstrably dedicated to this same article task. Do not switch away or bypass it with a branch or worktree.
5. On a clean `main`/`master`, create `docs/<core-topic>`, using at most five lowercase English words joined by hyphens.

The gate is a whole-task prerequisite, not a file-overlap check. A failure ends the task before article acquisition.

### 2. Acquire the complete canonical article

Resolve the URL host and use the first matching route:

| Host | First route | Required continuation |
|---|---|---|
| Zhihu | Invoke `$zhihu` and use its official CLI. Try the explicit URL or numeric ID first; retry by exact title when lookup requires it. | Treat `ContentText`, search summaries, and metadata as incomplete when substantial article sections are missing; then open the canonical URL in the browser. |
| WeChat Official Account (`mp.weixin.qq.com`) | Invoke `$wechat-article-to-markdown` first, even when prior experience suggests extraction may be incomplete. | If extraction fails or omits substantial body text, open the same canonical URL in the browser. |
| Feishu/Lark document | Invoke the matching installed Lark skill identified by the URL, such as `$lark-doc` for Docx or `$lark-wiki` for Wiki. | Use browser fallback only if the specialized route is absent, blocked, or incomplete. |
| Other platform | Discover an applicable installed connector, official CLI, or skill and use it first. | If none exists, or its result is blocked or incomplete, open the canonical URL in the browser. |

Use focused search for the same canonical article only when the original page cannot be read. Never substitute an unrelated repost or a search snippet for the article body. If authentication blocks the page, ask the user to sign in. Ask before solving a CAPTCHA. If the full article remains unreadable, stop without modifying the knowledge base.

Do not install a plugin unless the user explicitly requests installation. An available-but-uninstalled plugin does not alter the routing rule.

### 3. Build the evidence-bounded summary

Return these parts in order:

1. one-sentence conclusion;
2. title, author/publisher, available publication or edit date, and canonical URL;
3. technical summary focused on `core_keywords`;
4. architecture, data flow, decisions, and quantitative claims actually present;
5. separately labeled article claims, inference, unknowns, and independently verified facts.

An external article does not prove current source behavior, transaction or consistency semantics, crash safety, production scale, or general performance. Express performance numbers as “article-reported” or “author-claimed” and preserve the available baseline, workload, data scale, versions, hardware, concurrency, cache state, metric definition, and percentiles. List missing conditions as unverified; do not infer them.

### 4. Preserve the minimum reusable knowledge

Search `articles/`, `concepts/`, `index.md`, and `concepts/index.md` for the title, canonical URL, keywords, aliases, and related concepts.

- Update an existing source note for the same source; otherwise create `articles/<topic>.md`.
- Prefer updating an existing concept page. Create one only for a reusable mechanism or decision framework that existing pages cannot carry cleanly.
- Create no concept when the article supplies no durable reusable knowledge.
- Update the necessary navigation and reverse links so new pages are not orphaned.
- Do not modify `feishu/`, `sync/feishu-manifest.json`, or generated `graphify-out/` artifacts.

Before any knowledge-base write during actual Codex execution, obtain the current session/task ID from the current runtime task/session context—the same ID exposed by Codex’s **Copy session ID** action—even when the user did not paste it into the prompt. Write that exact value to the existing `codex_task_id` field; never introduce a `codex_session_id` alias. This ID is mandatory: if the current runtime cannot provide it, stop before writing and report the traceability blocker instead of using `unavailable`. Use runtime-exposed values for `codex_task_title` and `codex_task_share_url`, or write `unavailable` when either optional value is absent. Never search private stores, local databases, logs, caches, hidden runtime files, or environment secrets to recover identifiers.

Before writing, run `git status --short --branch` again. If non-task changes appeared, stop without overwriting them.

### 5. Validate and create one local commit

Run in the knowledge-base root:

```bash
python3 -B sync/validate_knowledge_base.py
git diff --check
```

Fix failures only in task-owned files. Then inspect the exact diff and status, stage explicit paths only, run `git diff --cached --check`, inspect `git diff --cached --stat`, and create one English Conventional Commit beginning with `docs:`. Read back `git show --stat --oneline --decorate -1` and `git status --short --branch`.

The request to preserve knowledge locally includes this branch-and-local-commit contract. It never includes push, PR creation, or repository-visibility changes.

## Final response contract

First return the five-part article summary from step 3. Then report, in order:

1. whether the `articles/` source note was created or updated and its path;
2. existing concepts updated and concepts created, including “none” where applicable;
3. navigation and reverse-link changes;
4. each validation command and exact result;
5. knowledge-base branch and commit SHA;
6. unverified items and the explicit statement “no push or PR was performed.”

If the gate or acquisition fails, report only completed read-only checks, the blocker, and zero-write/zero-commit facts. Do not fabricate a summary, validation result, or task identifier.

## Red flags

- “Dirty files do not overlap, so continue.”
- “Create a branch or worktree to bypass another unfinished task.”
- “Use `codex/<topic>` in the knowledge base.”
- “Open the browser before invoking an installed matching skill.”
- “`ContentText`, metadata, or a search summary is the complete article.”
- “Write `codex_task_id: unavailable` during actual Codex execution without first obtaining the current runtime session ID.”
- “Use `codex_session_id` instead of the repository-supported `codex_task_id` field.”
- “Search private Codex state to recover traceability.”
- “Knowledge preservation does not require a local commit.”
- “Install a useful plugin, push, or create a PR without a separate explicit request.”

Any red flag means stop and return to the corresponding gate, routing, evidence, traceability, or publication rule.
