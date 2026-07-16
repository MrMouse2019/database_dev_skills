# README Skill Index Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a complete index of repository skills, Codex invocation commands, and directories to `README.md`.

**Architecture:** Treat every `skills/*/SKILL.md` as the source of truth. Render one compact Markdown table whose display name comes from the first level-one heading, invocation comes from the frontmatter `name`, and directory comes from the file location.

**Tech Stack:** Markdown, POSIX shell, Git

## Global Constraints

- Preserve the existing `# database_dev_skills` title.
- Modify only `README.md` during implementation.
- Do not alter the current skill directory reorganization.
- Do not include installation commands, prompt templates, or long descriptions.
- Sort rows by skill directory name.

---

### Task 1: Add and verify the skill command index

**Files:**
- Modify: `README.md`
- Read: `skills/database-source-wiki/SKILL.md`
- Read: `skills/formatting-markdown-for-feishu/SKILL.md`
- Read: `skills/research-paper/SKILL.md`

**Interfaces:**
- Consumes: frontmatter `name`, first level-one heading, and repository-relative directory from each `skills/*/SKILL.md`.
- Produces: a `## 可用 Skills` table in `README.md` with one row per discovered skill.

- [ ] **Step 1: Capture the expected source mappings**

Run:

```bash
for file in skills/*/SKILL.md; do
  name=$(sed -n 's/^name: //p' "$file" | head -1)
  title=$(sed -n 's/^# //p' "$file" | head -1)
  printf '%s\t$%s\t%s\n' "$title" "$name" "${file%/SKILL.md}/"
done
```

Expected output:

```text
Database Source Wiki	$database-source-wiki	skills/database-source-wiki/
Formatting Markdown for Feishu	$formatting-markdown-for-feishu	skills/formatting-markdown-for-feishu/
论文深度解读	$research-paper	skills/research-paper/
```

- [ ] **Step 2: Update `README.md` with the complete table**

Replace the file content with:

```markdown
# database_dev_skills

## 可用 Skills

| Skill 显示名称 | Codex 调用命令 | 所在目录 |
|---|---|---|
| Database Source Wiki | `$database-source-wiki` | `skills/database-source-wiki/` |
| Formatting Markdown for Feishu | `$formatting-markdown-for-feishu` | `skills/formatting-markdown-for-feishu/` |
| 论文深度解读 | `$research-paper` | `skills/research-paper/` |
```

- [ ] **Step 3: Verify completeness, exact commands, directories, and Markdown whitespace**

Run:

```bash
python3 - <<'PY'
from pathlib import Path

readme = Path("README.md").read_text(encoding="utf-8")
skills = sorted(Path("skills").glob("*/SKILL.md"))
assert readme.count("\n| ") - 1 == len(skills), "README row count differs from discovered skills"
for skill_file in skills:
    text = skill_file.read_text(encoding="utf-8")
    name = next(line.removeprefix("name: ") for line in text.splitlines() if line.startswith("name: "))
    title = next(line.removeprefix("# ") for line in text.splitlines() if line.startswith("# "))
    directory = f"{skill_file.parent.as_posix()}/"
    row = f"| {title} | `${name}` | `{directory}` |"
    assert row in readme, f"missing or incorrect row: {row}"
    assert skill_file.parent.is_dir(), f"missing directory: {directory}"
print(f"verified {len(skills)} skill mappings")
PY
git diff --check -- README.md
```

Expected output:

```text
verified 3 skill mappings
```

Both commands must exit with status `0`.

- [ ] **Step 4: Commit only the README implementation**

```bash
git add -- README.md
git diff --cached --check
git diff --cached --name-only
git commit -m "docs(readme): index skill invocation commands"
```

Expected staged path before commit:

```text
README.md
```
