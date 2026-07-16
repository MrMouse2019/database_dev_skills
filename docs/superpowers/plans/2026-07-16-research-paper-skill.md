# Research Paper Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade the research-paper prompt and add a reusable skill that produces evidence-grounded, Feishu-ready personal technical articles suitable for public publication.

**Architecture:** Keep the prompt template as a standalone user entry point. Put the reusable execution workflow in `research-paper/SKILL.md`, detailed public-writing and illustration guidance in one directly linked reference, and generated UI metadata in `research-paper/agents/openai.yaml`.

**Tech Stack:** Markdown, YAML, shell assertions, Codex skill-creator validation scripts.

## Global Constraints

- Preserve the repository layout: root-level skill directory plus `prompt_templates/<name>/prompt_template.md`.
- Output Chinese content formatted for transfer into a Feishu cloud document.
- Position the result as an independently readable personal technical article that can be publicly published after review.
- Separate paper evidence, author claims, external material, and independent analysis.
- Narrow claims and disclose missing evidence when the full paper, appendix, code, or experiment details are unavailable.
- Borrow only abstract style principles from the downloaded ByteDance article; do not copy its prose, images, logos, or brand identity.
- Require original diagrams with source notes and Feishu-compatible layout.
- Do not add scripts or assets unless validation proves they are necessary.

---

### Task 1: Establish the failing content contract

**Files:**
- Inspect: `prompt_templates/research-paper/prompt_template.md`
- Expect absent: `research-paper/SKILL.md`
- Expect absent: `research-paper/references/public-article-style.md`

**Interfaces:**
- Consumes: the approved design at `docs/superpowers/specs/2026-07-16-research-paper-skill-design.md`.
- Produces: a reproducible RED baseline showing the current repository lacks the requested skill and required prompt clauses.

- [ ] **Step 1: Run the structural RED assertion**

```bash
test -f research-paper/SKILL.md && test -f research-paper/references/public-article-style.md
```

Expected: non-zero exit because the skill files do not exist.

- [ ] **Step 2: Run the prompt-contract RED assertion**

```bash
grep -q '飞书云文档' prompt_templates/research-paper/prompt_template.md \
  && grep -q '公开' prompt_templates/research-paper/prompt_template.md \
  && grep -q '个人技术文章' prompt_templates/research-paper/prompt_template.md
```

Expected: non-zero exit because the current template does not contain the new format and publication contract.

---

### Task 2: Scaffold and implement the reusable skill

**Files:**
- Create: `research-paper/SKILL.md`
- Create: `research-paper/references/public-article-style.md`
- Create: `research-paper/agents/openai.yaml`

**Interfaces:**
- Consumes: paper title, paper URL or local PDF, optional focus area, and optional publication constraints.
- Produces: a Feishu-ready Chinese personal technical article plus explicit evidence and uncertainty notes.

- [ ] **Step 1: Initialize the skill with the official scaffold**

```bash
python3 /Users/zhangxiahao/.codex/skills/.system/skill-creator/scripts/init_skill.py research-paper \
  --path . \
  --resources references \
  --interface 'display_name=论文深度解读' \
  --interface 'short_description=将研究论文深度解读为适合飞书云文档公开发布的中文个人技术文章' \
  --interface 'default_prompt=使用 $research-paper 深度解读这篇论文，并输出适合飞书云文档发布的个人技术文章。'
```

Expected: `research-paper/` contains `SKILL.md`, `agents/openai.yaml`, and `references/`.

- [ ] **Step 2: Replace the scaffolded `SKILL.md` with the approved workflow**

Write a concise imperative workflow with exactly these responsibilities:

```text
frontmatter: name and trigger-only description
overview: source-grounded public technical article
inputs and access levels: full-text, partial-text, abstract-only
evidence ledger: paper fact, author interpretation, external source, independent judgment
workflow: identify, read, reconstruct, challenge, design narrative, illustrate, draft, review
output contract: title, lead, verdict, method, experiments, limits, engineering view, one-page summary, references
failure handling: inaccessible sources and unsupported quantitative claims
publication gate: factual, copyright, editorial, visual, and Feishu checks
reference link: references/public-article-style.md
```

Expected: no scaffold placeholders remain; all instructions use imperative wording.

- [ ] **Step 3: Write the reusable writing and illustration reference**

Write `research-paper/references/public-article-style.md` with these sections:

```text
reader narrative and voice
Feishu document structure
original illustration grammar
diagram selection matrix
captions and source notes
copyright boundaries
publication-readiness checklist
```

Expected: it describes white or light backgrounds, low-saturation grouped colors, consistent rounded containers, concise labels, limited arrows, one message per figure, readable captions, and explicit attribution without copying ByteDance assets.

- [ ] **Step 4: Regenerate UI metadata from the final skill**

```bash
python3 /Users/zhangxiahao/.codex/skills/.system/skill-creator/scripts/generate_openai_yaml.py research-paper --name research-paper \
  --interface 'display_name=论文深度解读' \
  --interface 'short_description=将研究论文深度解读为适合飞书云文档公开发布的中文个人技术文章' \
  --interface 'default_prompt=使用 $research-paper 深度解读这篇论文，并输出适合飞书云文档发布的个人技术文章。'
```

Expected: quoted YAML strings under `interface`, with a default prompt that explicitly mentions `$research-paper` and no unsupported optional fields.

---

### Task 3: Upgrade the standalone prompt and validate the complete change

**Files:**
- Modify: `prompt_templates/research-paper/prompt_template.md`
- Validate: `research-paper/SKILL.md`
- Validate: `research-paper/references/public-article-style.md`
- Validate: `research-paper/agents/openai.yaml`

**Interfaces:**
- Consumes: the same inputs and output contract as the skill.
- Produces: a directly reusable prompt that remains consistent with the skill.

- [ ] **Step 1: Update the prompt template**

Retain the current sixteen analysis topics, then add the following binding requirements:

```text
output format: Feishu cloud document
publication identity: original personal technical article suitable for public release
article narrative: conclusion first, not chapter-by-chapter translation
evidence boundaries: four source categories and explicit uncertainty
illustrations: original redrawn diagrams using the reference visual grammar
copyright: cite necessary paper figures and do not copy third-party brand assets
Feishu layout: headings, short paragraphs, tables, callouts, code, formulas, captions, stable links
publication gate: fact, citation, copyright, tone, and layout review
```

Expected: the original analytical depth is preserved while the new output and publication constraints are explicit.

- [ ] **Step 2: Prepare the validator's temporary dependency**

```bash
python3 -m pip install --target /tmp/codex-skill-validator-deps PyYAML
```

Expected: PyYAML is installed only under `/tmp`; the repository and system Python remain unchanged.

- [ ] **Step 3: Run the skill validator**

```bash
PYTHONPATH=/tmp/codex-skill-validator-deps \
  python3 /Users/zhangxiahao/.codex/skills/.system/skill-creator/scripts/quick_validate.py research-paper
```

Expected: validator reports the skill is valid.

- [ ] **Step 4: Run the GREEN content-contract assertions**

```bash
test -f research-paper/SKILL.md \
  && test -f research-paper/references/public-article-style.md \
  && test -f research-paper/agents/openai.yaml \
  && grep -q '飞书云文档' prompt_templates/research-paper/prompt_template.md \
  && grep -q '个人技术文章' prompt_templates/research-paper/prompt_template.md \
  && grep -q '公开' prompt_templates/research-paper/prompt_template.md \
  && grep -q 'references/public-article-style.md' research-paper/SKILL.md \
  && grep -q '\$research-paper' research-paper/agents/openai.yaml
```

Expected: exit code 0.

- [ ] **Step 5: Run repository hygiene checks**

```bash
git diff --check
git status --short
```

Expected: no whitespace errors; only the implementation plan, updated prompt, and new `research-paper` skill files are in scope.

- [ ] **Step 6: Commit the implementation**

```bash
git add docs/superpowers/plans/2026-07-16-research-paper-skill.md \
  prompt_templates/research-paper/prompt_template.md research-paper
git commit -m 'feat(research-paper): add public article workflow'
```

Expected: one Conventional Commit containing the task-scoped implementation and plan.
