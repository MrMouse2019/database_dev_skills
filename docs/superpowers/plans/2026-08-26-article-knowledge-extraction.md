# Article Knowledge Extraction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add separately packaged WorkBuddy and Codex `article-knowledge-extraction` skills that read platform articles, summarize them by core keywords, and safely commit evidence-bounded knowledge to the canonical knowledge-base checkout.

**Architecture:** Keep the two runtime implementations isolated under `skills/workbuddy/` and `skills/codex/`, while preserving the same input/output and repository-mutation contract. Each skill contains a concise workflow plus a runtime-specific knowledge-base reference; scenario artifacts document acquisition routing, dirty-worktree refusal, evidence labeling, and local-only Git behavior.

**Tech Stack:** Markdown Agent Skills, YAML frontmatter, WorkBuddy skills, Codex skills and `agents/openai.yaml`, Git, Python knowledge-base validator.

**Spec:** `docs/superpowers/specs/2026-08-26-article-knowledge-extraction-design.md`

## Global Constraints

- The target branch is `codex/article-knowledge-extraction`; never implement on `main`.
- Preserve exactly two new commits: WorkBuddy implementation first, Codex implementation second.
- The first commit includes the approved design, this plan, and WorkBuddy artifacts.
- Do not push or create a pull request.
- The article-extraction runtime must mutate only `/Users/zhangxiahao/Desktop/projects/knowledge_base` and must not use a knowledge-base worktree.
- Reject the whole extraction task when the canonical knowledge-base checkout has tracked changes, non-ignored untracked files, or an unrelated non-default branch.
- Treat external performance, scale, correctness, and production claims as source claims until independently verified.
- Use explicit paths for Git staging; never use `git add .`.

---

### Task 1: WorkBuddy baseline scenarios

**Files:**
- Create: `skills/workbuddy/article-knowledge-extraction/tests/pressure-scenarios.md`

**Interfaces:**
- Consumes: the approved design and the current WorkBuddy skill at `~/.workbuddy/skills/article-knowledge-extraction/` as source material only.
- Produces: documented baseline failure modes and acceptance checks for the WorkBuddy implementation.

- [ ] **Step 1: Define baseline prompts before writing the new skill**

Define four prompts: WeChat acquisition routing, generic-page browser fallback, dirty knowledge-base refusal, and article-reported performance labeling. Each prompt supplies `article_url` and `core_keywords` and asks for an execution plan without exposing the intended answer.

- [ ] **Step 2: Run the prompts without the new repository skill**

Use fresh-context agents that cannot read the not-yet-created WorkBuddy repository skill. Capture whether they select a platform reader, gate the knowledge base before fetching, reject dirty state, avoid worktrees, preserve evidence labels, and avoid push/PR.

- [ ] **Step 3: Record observed failures verbatim**

Write the prompts, concise baseline responses, and a failure matrix into `pressure-scenarios.md`. The production wording must address observed failures rather than hypothetical ones.

### Task 2: WorkBuddy skill implementation

**Files:**
- Create: `skills/workbuddy/article-knowledge-extraction/SKILL.md`
- Create: `skills/workbuddy/article-knowledge-extraction/references/knowledge-base-conventions.md`
- Modify: `skills/workbuddy/article-knowledge-extraction/tests/pressure-scenarios.md`
- Include: `docs/superpowers/specs/2026-08-26-article-knowledge-extraction-design.md`
- Include: `docs/superpowers/plans/2026-08-26-article-knowledge-extraction.md`

**Interfaces:**
- Consumes: `article_url`, `core_keywords`, the canonical knowledge-base checkout, and WorkBuddy platform readers/browser.
- Produces: an article summary, knowledge-base source/concept/navigation updates, static validation evidence, and a local knowledge-base commit report.

- [ ] **Step 1: Initialize the runtime directory**

Create only the required `SKILL.md`, `references/`, and `tests/` structure. Preserve WorkBuddy-compatible metadata and keep the public name `article-knowledge-extraction`.

- [ ] **Step 2: Write the minimal workflow**

Implement the exact sequence: validate inputs; inspect canonical knowledge-base state; refuse conflicts; choose platform reader; use browser fallback for missing/incomplete content; summarize by keywords; inspect existing pages; update or create the minimum source/concept pages; update navigation; validate; stage explicit paths; commit locally; report outputs and evidence boundaries.

- [ ] **Step 3: Write the WorkBuddy reference**

Define supported frontmatter values, WorkBuddy conversation traceability, canonical-checkout serialization, branching, validation, commit, and final-report rules. Reuse current knowledge-base conventions but remove stale or contradictory `external-article` status guidance.

- [ ] **Step 4: Re-run scenarios with the skill**

Provide the new skill to fresh-context agents. Require all matrix checks to pass. Add only wording needed to close observed gaps.

- [ ] **Step 5: Validate and commit WorkBuddy artifacts**

Run:

```bash
python3 /Users/zhangxiahao/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/workbuddy/article-knowledge-extraction
git diff --check
```

Stage the design, plan, and WorkBuddy skill with explicit paths. Inspect `git diff --cached --check` and `git diff --cached --stat`, then commit:

```text
feat(workbuddy): add article knowledge extraction skill
```

Read back the commit and verify the worktree contains no unexpected paths.

### Task 3: Codex baseline scenarios

**Files:**
- Create: `skills/codex/article-knowledge-extraction/tests/pressure-scenarios.md`

**Interfaces:**
- Consumes: the approved design, installed Codex skill catalog, and WorkBuddy behavior contract.
- Produces: documented Codex baseline failures and routing-specific acceptance checks.

- [ ] **Step 1: Define Codex prompts before writing the Codex skill**

Cover Zhihu CLI lookup with incomplete-body browser fallback, WeChat skill routing, generic connector discovery, dirty-checkout refusal, and unavailable Codex traceability.

- [ ] **Step 2: Run prompts without the Codex repository skill**

Use fresh-context agents and record whether they invoke the platform skill before browsing, distinguish summary fields from complete content, check the canonical checkout first, avoid knowledge-base worktrees, and write only exposed task metadata.

- [ ] **Step 3: Record baseline failures**

Add the prompts, concise baseline responses, and failure matrix to the Codex scenario file.

### Task 4: Codex skill implementation and repository index

**Files:**
- Create: `skills/codex/article-knowledge-extraction/SKILL.md`
- Create: `skills/codex/article-knowledge-extraction/references/knowledge-base-conventions.md`
- Create: `skills/codex/article-knowledge-extraction/agents/openai.yaml`
- Modify: `skills/codex/article-knowledge-extraction/tests/pressure-scenarios.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: `article_url`, `core_keywords`, the Codex skill/tool catalog, browser fallback, and the canonical knowledge-base checkout.
- Produces: the same business outputs as WorkBuddy with Codex-compatible invocation and traceability.

- [ ] **Step 1: Initialize the Codex skill**

Run `init_skill.py` with `--resources references`, supplying deterministic interface values for display name, short description, and a default prompt that explicitly invokes `$article-knowledge-extraction`. Remove unused generated files.

- [ ] **Step 2: Write the Codex workflow**

Keep only `name` and `description` in frontmatter. Encode the routing table: `$zhihu` first for Zhihu, `$wechat-article-to-markdown` first for WeChat, matching Lark skill for Feishu documents, matching installed connector/CLI/skill for other hosts, browser only when the specialized reader is absent, blocked, or incomplete.

- [ ] **Step 3: Write Codex knowledge-base conventions**

Mirror the shared repository rules. Replace WorkBuddy metadata with runtime-neutral source fields and optional Codex task fields; unavailable values remain `unavailable`, and the skill must not search private stores for identifiers.

- [ ] **Step 4: Update the README index**

Document both runtime variants, invocation name, and their exact directories without changing unrelated entries.

- [ ] **Step 5: Re-run Codex scenarios**

Provide the new Codex skill to fresh-context agents and require all acceptance checks to pass. Refine only observed gaps.

- [ ] **Step 6: Validate and commit Codex artifacts**

Run:

```bash
python3 /Users/zhangxiahao/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/codex/article-knowledge-extraction
git diff --check
```

Validate `agents/openai.yaml`, inspect exact diffs, stage Codex paths and `README.md`, then commit:

```text
feat(codex): add article knowledge extraction skill
```

### Task 5: Final verification

**Files:**
- Verify only; no expected new files.

**Interfaces:**
- Consumes: the two commits on `codex/article-knowledge-extraction`.
- Produces: evidence that layout, validation, commit count, order, and no-push state meet the request.

- [ ] **Step 1: Validate both skill directories again**

Run `quick_validate.py` separately for WorkBuddy and Codex plus `git diff --check`.

- [ ] **Step 2: Verify repository state and history**

Run:

```bash
git log --oneline --decorate main..HEAD
git diff --stat main..HEAD
git status --short --branch
git branch -vv
```

Require exactly two commits in WorkBuddy-then-Codex order, a clean worktree, and no upstream publication of the feature branch.

- [ ] **Step 3: Report delivery**

Provide absolute file links, both commit SHAs, exact validation results, the unpushed branch name, and remaining validation boundaries. Do not create a PR title or description until the user later confirms the implementation and asks for them.
