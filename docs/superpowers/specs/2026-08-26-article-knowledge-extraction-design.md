# Article Knowledge Extraction Skill Design

## 1. Background

The repository needs two runtime-specific implementations of the same reusable workflow:

- WorkBuddy: read an external article, summarize it, and persist durable knowledge into the local database-engineering knowledge base.
- Codex: provide the same business behavior while using Codex skills, connectors, CLI tools, and browser fallback rules.

Both implementations use the public skill name `article-knowledge-extraction`, but live under separate runtime directories to avoid filename and metadata conflicts.

## 2. Goals

1. Accept exactly two required inputs:
   - an article URL;
   - one or more core keywords that define the reading focus.
2. Produce two user-facing outputs:
   - an evidence-bounded article summary;
   - a report of the knowledge committed to `/Users/zhangxiahao/Desktop/projects/knowledge_base`.
3. Prefer a platform-specific reader before using a browser.
4. Serialize knowledge-base mutations through the canonical checkout and reject a new task when unfinished work is visible.
5. Preserve source provenance, distinguish article claims from verified facts, update navigation, validate the knowledge base, and create a local commit.
6. Never push or create a pull request unless separately authorized.

## 3. Non-goals

- Do not fact-check every claim in the source article unless the user asks for verification.
- Do not treat an external article as proof of current source-code behavior, production performance, crash safety, or consistency semantics.
- Do not modify `feishu/`, `sync/feishu-manifest.json`, or generated `graphify-out/` artifacts.
- Do not automatically publish, push, create a PR, or change repository visibility.
- Do not create empty concept pages merely to satisfy a fixed output count.

## 4. Repository Layout

```text
skills/
├── workbuddy/
│   └── article-knowledge-extraction/
│       ├── SKILL.md
│       └── references/
│           └── knowledge-base-conventions.md
└── codex/
    └── article-knowledge-extraction/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        └── references/
            └── knowledge-base-conventions.md
```

The WorkBuddy implementation may retain WorkBuddy-specific metadata supported by that runtime. The Codex implementation follows the Codex skill schema and keeps only `name` and `description` in `SKILL.md` frontmatter.

## 5. Input and Output Contract

### Inputs

| Field | Required | Meaning |
|---|---:|---|
| `article_url` | yes | Canonical article URL supplied by the user |
| `core_keywords` | yes | Reading focus; used for extraction, summary emphasis, concept matching, and branch naming |

If either field is missing and cannot be inferred without risk, ask one concise question before fetching or writing anything.

### Article summary

Return, in order:

1. One-sentence conclusion.
2. Source metadata: title, author/publisher, publication or edit date when available, and canonical URL.
3. Keyword-focused technical summary.
4. Architecture, data flow, decisions, and quantitative claims that are actually present.
5. Evidence boundary: clearly label article claims, inference, unknowns, and any independently verified facts.

### Knowledge-base result

Return, in order:

1. Whether the task created or updated an `articles/` source note.
2. Which existing `concepts/` pages were updated and which new concept pages were created, if any.
3. Navigation changes.
4. Validation commands and their exact results.
5. Knowledge-base branch and commit SHA.
6. Unverified items and the statement that no push or PR was performed.

## 6. Article Acquisition Routing

### Selection rule

Resolve the URL host, then use this priority:

1. A matching installed platform skill, connector, or official CLI.
2. The original page in a controllable browser.
3. A focused search for the same canonical article only when the original page cannot be read.

A search result or API summary is not automatically the full article. If the platform response omits substantial sections, continue to the browser before writing the summary.

### WorkBuddy routing

- Use an installed WorkBuddy platform connector or skill when one exists.
- For WeChat Official Account URLs, use the available WeChat article reader when present.
- Fall back to WorkBuddy browser/WebFetch only when the platform reader is missing, blocked, or incomplete.

### Codex routing

- Zhihu: use `$zhihu` and its official CLI first. Search by exact title after URL or numeric-ID lookup if needed. If CLI fields are incomplete, use the browser on the canonical URL.
- WeChat Official Account: use `$wechat-article-to-markdown` first. Use the browser if extraction fails or the returned article is incomplete.
- Feishu/Lark documents: use the matching Lark document skill when the link identifies a supported document.
- Other platforms: discover and use an applicable installed connector, CLI, or skill; otherwise use the browser.

Do not install a plugin merely because it might help. Installation requires a separate explicit user request.

## 7. Knowledge-base Serialization Gate

Always operate on the canonical checkout:

`/Users/zhangxiahao/Desktop/projects/knowledge_base`

Do not create a knowledge-base worktree for article extraction because isolated worktrees would bypass the shared dirty-worktree conflict signal.

Before article acquisition or any write:

1. Read the repository `AGENTS.md`, `README.md`, `index.md`, and relevant directory indexes.
2. Run `git status --short --branch` in the canonical checkout.
3. Stop the entire task when tracked changes are staged or unstaged.
4. Stop when non-ignored untracked files exist. Report their paths; do not stash, delete, move, or commit them.
5. Ignore only files already excluded by Git, including an ignored `.workbuddy/` directory.

This matches the WorkBuddy conflict strategy: the shared checkout is the serialization point. A dirty checkout means another task is unfinished or residual work needs user handling.

When the checkout is clean:

- On `main` or `master`, create `docs/<core-topic>` using lowercase English words, hyphens, at most five words.
- On a non-default branch, continue only if the branch is already dedicated to the same article task; otherwise stop and ask the user to finish or switch the existing task.

## 8. Knowledge Extraction and Persistence

### Repository inspection

- Search `articles/`, `concepts/`, `index.md`, and `concepts/index.md` for the title, URL, keywords, aliases, and related concepts.
- Prefer updating an existing concept page.
- Create a concept page only when the article supports a reusable mechanism or decision framework that existing pages cannot carry cleanly.

### Source note

Create or update `articles/<topic>.md` with:

- `type: source-note`;
- `evidence_status` chosen from the repository-supported vocabulary: use `official-doc` for an authoritative publisher's own documentation, `conference-summary` for conference or case-study retellings, and `unverified` when the source class cannot be established;
- canonical source URL and available source metadata;
- runtime traceability fields, using `unavailable` rather than guesses;
- evidence warning, conclusion, keyword-focused analysis, article claims, transferable knowledge, non-transferable claims, and follow-up validation.

### Concept knowledge

For each justified concept update:

- preserve the existing page structure and terminology;
- add the article source and a reverse link;
- distinguish general mechanism, design recommendation, article claim, inference, and unknown;
- cover correctness/failure semantics and performance validation gaps when relevant.

Create no concept page when the source contains no durable reusable knowledge. The source note still satisfies knowledge preservation.

### Traceability

- WorkBuddy records the available WorkBuddy conversation ID, title, and share URL using the existing convention.
- Codex records only task metadata exposed by the current runtime. Missing task ID, title, or share URL is `unavailable`; never search private stores or invent identifiers.
- Both variants always record the canonical source URL.

## 9. Validation and Commit

Run from the knowledge-base root:

```bash
python3 -B sync/validate_knowledge_base.py
git diff --check
```

Before committing:

1. Review the exact diff and `git status --short`.
2. Stage explicit paths only; never use `git add .`.
3. Run `git diff --cached --check` and inspect `git diff --cached --stat`.
4. Commit with an English Conventional Commit message beginning with `docs:`.

After committing:

```bash
git show --stat --oneline --decorate -1
git status --short --branch
```

Report actual evidence only. Static validation does not prove runtime correctness or performance.

## 10. Error Handling

| Condition | Required behavior |
|---|---|
| Platform tool unavailable | Use browser fallback and report the fallback |
| Tool returns only a summary | Continue to canonical page before summarizing |
| Authentication blocks canonical page | Ask the user to sign in; do not substitute an unrelated article |
| CAPTCHA appears | Ask before solving it |
| Article still unreadable | Stop without modifying the knowledge base |
| Knowledge-base checkout dirty | Refuse the entire task and list blocking paths |
| Existing unrelated feature branch | Stop and ask the user to finish the current task |
| Validation fails | Fix only task-owned files; do not commit until validation passes |
| Source conflicts with existing knowledge | Preserve both claims and label the conflict; do not silently overwrite verified knowledge |

## 11. Runtime-specific Packaging

### WorkBuddy commit

The first commit contains:

- this approved design document;
- the WorkBuddy skill and its knowledge-base reference;
- WorkBuddy-specific test scenarios or validation artifacts required by repository conventions.

### Codex commit

The second commit contains:

- the Codex skill and its knowledge-base reference;
- `agents/openai.yaml` generated from the final skill;
- repository README/index updates that expose both variants;
- Codex-specific test scenarios or validation artifacts.

The branch remains local. No push or PR is performed.

## 12. Verification Scenarios

Each implementation must be checked against at least these scenarios:

1. Zhihu URL: platform tool first, exact-title retry, browser fallback for incomplete content.
2. WeChat URL: WeChat reader first, browser fallback on failure.
3. Generic technical article: matching connector when installed, otherwise browser.
4. Dirty knowledge-base checkout: refuse before fetching or writing.
5. Clean default branch: create a topic branch, update source/concept/navigation, validate, and commit locally.
6. External performance claims: label as article-reported and preserve missing benchmark verification.

## 13. Acceptance Criteria

- Both runtime directories exist and use the intended public skill name.
- Both skills define the same input/output and knowledge-base semantics.
- Platform-specific acquisition and browser fallback are explicit and testable.
- The canonical knowledge-base checkout is the only mutation target and rejects residual work.
- Skill validation, repository checks, and scenario checks pass.
- Git history contains exactly two new commits on `codex/article-knowledge-extraction`: WorkBuddy first, Codex second.
- The branch is not pushed.
