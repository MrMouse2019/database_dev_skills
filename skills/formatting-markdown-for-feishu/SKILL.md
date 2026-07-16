---
name: formatting-markdown-for-feishu
description: Use when Markdown reports, paper summaries, technical documents, design docs, or incident reviews must be imported or pasted into Feishu and formulas, code fences, tables, lists, headings, or references render incorrectly.
---

# Formatting Markdown for Feishu

## Overview

Convert an existing Markdown document into a Feishu-stable form without changing its technical meaning, facts, data, conclusions, or section structure.

**Core principle:** Prefer portable Markdown and plain-text mathematical notation over renderer-dependent extensions.

## When to Use

Use this skill when the source contains one or more of these symptoms:

- LaTeX blocks such as `\\[`、`\\]` or `$$`;
- formulas rendered as literal brackets after import;
- fenced code blocks carrying nonstandard attributes such as `id="..."`;
- broken or unclosed code fences;
- lists, headings, tables, or quotations that shift after pasting;
- model-specific citations or markers that Feishu cannot resolve.

Do not use it when the target explicitly requires native LaTeX, MathJax, HTML, or another renderer-specific format.

## Output Contract

Produce the **complete repaired Markdown document**, not a change list or partial sample.

The result must:

1. preserve every meaningful section and technical claim;
2. use UTF-8-compatible Markdown;
3. import into Feishu without extra rendering plugins;
4. contain no unresolved model-specific or nonstandard Markdown syntax;
5. include a final consistency check before delivery.

## Workflow

### 1. Protect Content

Before formatting, identify and preserve:

- facts, measurements, formulas, experimental results, links, and conclusions;
- distinctions between source claims and the report author's evaluation;
- code, pseudocode, architecture diagrams, and execution flows.

Do not silently correct uncertain facts. Add a **待确认问题** section when a factual contradiction cannot be resolved from the source.

### 2. Normalize Structure

- Use `#` for the document title, `##` for major sections, `###` for subsections, and `####` only when necessary.
- Do not skip heading levels.
- Use `-` for unordered lists and `1.` for ordered procedures.
- Keep one blank line around headings, lists, block quotes, tables, and code fences.
- Use standard Markdown tables with the same number of columns in every row.

### 3. Convert Formulas

Choose the smallest stable representation:

| Formula shape | Feishu-compatible representation |
|---|---|
| Short expression | Inline code, such as `d = O(log n)` |
| Multi-term or recursive formula | Fenced `text` block |
| Common operators | Unicode symbols such as `∪`, `∈`, `≤`, `α`, `λ`, `×`, `→`, `²`, `ⁿ` |
| Formula requiring explanation | Formula plus prose defining variables and semantics |

Remove renderer-dependent syntax:

- `\\[` and `\\]`;
- `$$`;
- standalone `[` and `]` used as fake formula fences;
- `$...$`;
- `\\frac{}`, `\\begin{aligned}`, `\\left`, `\\right`, `\\operatorname{}` and similar LaTeX commands.

Example:

Before:

```markdown
\\[
C(S)=\\min_{\\varnothing\\neq A\\subset S}
[C(A)+C(S-A)+J(A,S-A)]
\\]
```

After:

```text
C(S) = min {
    C(A) + C(S - A) + J(A, S - A)
}
```

Then explain `A`, `S - A`, and `J(A, S - A)` in ordinary Markdown.

### 4. Normalize Code Blocks

- Keep code, pseudocode, text diagrams, and execution flows in fenced blocks.
- Use a real language identifier only for real source code.
- Use `text` for pseudocode, formulas, architecture flows, and trees.
- Remove nonstandard fence metadata such as `id="abc123"`.
- Do not turn ordinary enumerations into code blocks; use Markdown lists instead.
- Ensure every opening fence has exactly one closing fence.

### 5. Clean Unsupported Markers

Remove or replace:

- unresolved internal citation IDs;
- model-generated content references;
- unsupported HTML anchors;
- duplicate links and decorative metadata that add no meaning.

Preserve valid paper, repository, and official-document links.

## Quick Reference

| Problem | Repair |
|---|---|
| `\\[` formula `\\]` | Inline code or `text` block |
| `$$...$$` | Inline code or `text` block |
| `O(n^2 2^n)` | `O(n² × 2ⁿ)` |
| Code fence with `id=` | Remove the attribute |
| Plain item list inside `text` block | Convert to `-` or `1.` list |
| Pseudocode marked as Python | Change fence language to `text` |
| Broken table | Equalize column counts and restore separator row |
| Heading used only for emphasis | Convert to bold text or a real section consistently |

## Common Mistakes

- **Converting every formula into a code block:** short expressions are clearer as inline code.
- **Converting every code block into a list:** real code, pseudocode, formulas, and diagrams should remain fenced.
- **Changing mathematical meaning while removing LaTeX:** preserve precedence, grouping, subscripts, and variable relationships.
- **Improving prose beyond the requested scope:** formatting repair must not silently rewrite the report's argument.
- **Deleting inconvenient content:** repair it instead; never omit sections to make formatting easier.
- **Leaving a valid-looking but unclosed fence:** scan the entire document, not only edited sections.

## Verification Checklist

Before returning the repaired document, verify:

- [ ] All code fences are paired and correctly typed.
- [ ] No `\\[`、`\\]`、`$$` or unsupported `$...$` formula remains.
- [ ] No fenced block contains `id="..."` or similar attributes.
- [ ] Short formulas use inline code; complex formulas use `text` blocks.
- [ ] Unicode conversion has not changed mathematical meaning.
- [ ] Every Markdown table has consistent columns.
- [ ] Heading levels are continuous.
- [ ] Lists are not accidentally wrapped in code blocks.
- [ ] Facts, data, links, conclusions, and section coverage match the source.
- [ ] The output is the complete repaired Markdown, with no process narration.
