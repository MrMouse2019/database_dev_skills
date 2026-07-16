# Research Paper Skill Design

## Background

The existing `prompt_templates/research-paper/prompt_template.md` asks for a deep Chinese technical summary of a research paper. It does not yet define Feishu cloud document formatting, publication readiness, a reusable skill workflow, or a sufficiently concrete visual language.

The downloaded ByteDance technical-team article is a style reference only. Its useful reusable traits are conclusion-first exposition, short progressive sections, restrained visual hierarchy, and diagrams built from light backgrounds, low-saturation color blocks, concise labels, and limited directional arrows. The implementation must not copy its prose, original illustrations, logos, or brand identity.

## Goals

- Update the standalone prompt template to request a Feishu cloud document.
- Create a reusable root-level `research-paper` skill for paper interpretation tasks.
- Produce Chinese personal technical articles that can be publicly published after review.
- Require source-grounded analysis, explicit evidence attribution, critical evaluation, and uncertainty handling.
- Define an original, reusable illustration style suitable for Feishu documents.

## Non-goals

- Automatically publish or share a Feishu document.
- Copy or imitate ByteDance branding, prose, or existing artwork.
- Guarantee complete analysis when the paper body, appendices, code, or experimental artifacts are unavailable.
- Replace domain-specific source inspection or reproducibility work with secondary commentary.

## Repository Structure

The change will create or update these files:

```text
prompt_templates/research-paper/prompt_template.md
research-paper/SKILL.md
research-paper/agents/openai.yaml
research-paper/references/public-article-style.md
```

The prompt remains a directly reusable entry point. The skill contains the core workflow and output contract. Detailed writing and illustration guidance lives in one directly referenced file to keep `SKILL.md` concise. UI metadata is generated from the finished skill.

## Inputs and Evidence

The skill accepts a paper title plus a URL or local PDF, with an optional focus area and optional publication constraints. It should attempt to inspect the full paper, experiments, appendices, official code, author material, cited work, and relevant industry practice.

Evidence must be separated into:

1. statements supported by the paper;
2. author claims or speculation;
3. information from external sources;
4. the article author's independent analysis.

When the full text, appendix, code, or experiment details cannot be accessed, the output must identify the missing evidence and narrow its claims. It must not imply that inaccessible material was reviewed.

## Workflow

1. Confirm the paper identity, version, available artifacts, target reader, and focus area.
2. Read the paper body, experiments, and appendix before drafting conclusions where available.
3. Build an evidence ledger for claims, numbers, formulas, figures, and external context.
4. Reconstruct the problem, assumptions, method, execution flow, and evaluation design.
5. Test whether the experiments support the stated conclusions, including baselines, fairness, ablations, costs, failures, and reproducibility.
6. Add domain analysis from database, optimizer, distributed-systems, or machine-learning perspectives only when relevant.
7. Design the article around a reader narrative rather than the paper's section order.
8. Plan original diagrams and tables that explain the central mechanism and trade-offs.
9. Draft a Feishu-ready Chinese article with conclusion-first organization and source links.
10. Run factual, editorial, visual, copyright, and publication-readiness checks.

## Output Contract

The result is a self-contained Chinese personal technical article, formatted for direct transfer into a Feishu cloud document. It includes:

- a publication-ready title and short lead;
- an explicit one-sentence conclusion;
- problem context and why the work matters;
- intuitive and technical explanations of the core method;
- formulas, pseudocode, architecture, or execution flows only when they improve understanding;
- quantitative experimental analysis and a critical validity assessment;
- limitations, applicability boundaries, engineering implications, and future directions;
- a concise one-page summary;
- numbered references or stable source links;
- an evidence and uncertainty note when source coverage is incomplete.

The article must not read like a chapter-by-chapter translation, a raw literature review, promotional copy, or an internal scratchpad.

## Feishu and Visual Style

The article uses Feishu-compatible headings, short paragraphs, callouts, tables, code blocks, formulas, image captions, and restrained emphasis. It avoids relying on complex HTML or fragile layout tricks.

Illustrations should be redrawn for the article. The default visual grammar uses a white or very light background, low-saturation blue, violet, green, orange, and red accents, rounded grouped containers, consistent typography, short labels, and only necessary arrows. Each diagram has one message, readable labels, a caption, and a source note such as `根据论文整理` or `作者绘制`.

Figures from the paper may be quoted only when necessary and must retain attribution. Third-party or ByteDance reference graphics must not be copied into the output.

## Failure Handling

- If a paper link is inaccessible, report the access limitation and ask for or use an available local copy.
- If only an abstract is available, produce an explicitly labeled preliminary reading rather than a full technical interpretation.
- If experimental setup or raw numbers are missing, do not manufacture comparisons or calculate unsupported gains.
- If an external claim conflicts with the paper, present the conflict and source boundaries instead of silently reconciling it.
- If the output cannot be written directly into Feishu, produce Feishu-ready Markdown-like content and clearly state that transfer remains manual.

## Validation

- Validate `SKILL.md` frontmatter and directory-name consistency with the skill validator.
- Confirm `agents/openai.yaml` matches the final skill and contains no unsupported optional fields.
- Check that the prompt and skill both require Feishu output, public personal-article positioning, evidence separation, uncertainty disclosure, and original diagrams.
- Check that the style reference contains no copied article prose, images, or brand assets.
- Run `git diff --check` and review that only task-scoped files changed.
