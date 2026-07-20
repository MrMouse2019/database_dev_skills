# Technical Research Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reusable `$technical-research` skill that performs source-grounded topic research and delivers a verified Chinese Feishu cloud document containing meaningful diagrams, comparisons, and implementation-level analysis.

**Architecture:** Keep orchestration in a concise `SKILL.md`, place evidence, domain-analysis, paper/product, and Feishu-delivery rules in directly referenced files, and provide a reusable report outline as an asset. Reuse the installed `lark-shared`, `lark-doc`, and `lark-whiteboard` capabilities instead of copying volatile CLI instructions; retain a standalone prompt template for users who need a copyable prompt.

**Tech Stack:** Markdown skill files, YAML UI metadata, Codex skill-creator scripts, `lark-cli`, Git, shell-based contract checks.

## Global Constraints

- Skill name and directory must both be `technical-research`; the invocation is `$technical-research`.
- The required final deliverable is a verified Feishu cloud document URL, not a Markdown fallback.
- Verify Feishu user authorization before performing the full research task; if authorization is unavailable, initiate the documented split-flow authorization and pause.
- Default language is Chinese and the default audience is database, distributed-systems, or AI Infra engineers.
- Keep single-paper deep interpretation in `$research-paper`; this skill performs topic-level synthesis across papers, source code, open-source systems, products, and public engineering evidence.
- Separate directly verified facts, paper conclusions, official claims, external evidence, and independent judgment.
- Use an architecture diagram, a flow/state diagram, a comparison table, and a code-like block when technically applicable; every visual must convey a specific claim and include attribution.
- Reuse `lark-shared`, `lark-doc`, and `lark-whiteboard`; do not duplicate version-sensitive CLI instructions.
- Do not add repository dependencies or a `scripts/` directory without new evidence that deterministic automation is required.
- Do not push or create a PR as part of this plan.

---

## File Map

| Path | Responsibility |
| --- | --- |
| `skills/technical-research/SKILL.md` | Core authorization, research, synthesis, Feishu delivery, and validation workflow |
| `skills/technical-research/agents/openai.yaml` | Display name, short description, and default invocation prompt |
| `skills/technical-research/references/evidence-and-sources.md` | Source selection, evidence ledger, citation, conflict, and uncertainty rules |
| `skills/technical-research/references/database-and-systems.md` | Conditional database, distributed-system, storage, optimizer, transaction, recovery, and performance analysis |
| `skills/technical-research/references/paper-and-product-review.md` | Paper selection, experiment review, system/product classification, and comparison rules |
| `skills/technical-research/references/feishu-delivery.md` | Authorization gate, Feishu XML composition, visual insertion, recovery, and post-write verification |
| `skills/technical-research/assets/report-outline.md` | Reusable, adaptable report skeleton |
| `prompt_templates/technical-research/prompt_template.md` | Standalone prompt derived from the supplied technical-research template |
| `README.md` | Invocation index entry for the new skill |

### Task 0: Capture Baseline Behavior Without the New Skill

**Files:**
- Create as ignored test evidence: `.superpowers/sdd/baseline-database.md`
- Create as ignored test evidence: `.superpowers/sdd/baseline-distributed.md`
- Create as ignored test evidence: `.superpowers/sdd/baseline-ai-infra.md`
- Create as ignored synthesis: `.superpowers/sdd/baseline-findings.md`

**Interfaces:**
- Consumes: three topic-research requests and the repository state before `skills/technical-research/` exists.
- Produces: observable baseline omissions that Tasks 1-3 must address and Task 5 must retest.

- [ ] **Step 1: Run three fresh-context baseline scenarios without the skill**

Dispatch independent read-only agents for learned cardinality estimation, consensus membership changes, and continuous batching. Tell each agent that no specialized topic-research skill is available. Ask it to describe exactly how it would execute the request, including authorization, evidence classification, visuals, Feishu creation, and completion criteria. Write each unedited response to the corresponding baseline file.

- [ ] **Step 2: Synthesize only observed omissions and rationalizations**

Create `baseline-findings.md` with one row per scenario and these columns:

```markdown
| Scenario | Authorization gate | Evidence classes | Domain correctness | Required visuals | Feishu回读 | Observed rationalization |
| --- | --- | --- | --- | --- | --- | --- |
```

Record only behavior present in the baseline responses. Do not infer a failure that was not observed.

- [ ] **Step 3: Verify RED evidence exists before implementation**

Run:

```bash
test ! -e skills/technical-research
test -s .superpowers/sdd/baseline-database.md
test -s .superpowers/sdd/baseline-distributed.md
test -s .superpowers/sdd/baseline-ai-infra.md
test -s .superpowers/sdd/baseline-findings.md
```

Expected: all checks pass and at least one concrete gap is documented. If all baselines already satisfy the contract, stop and reconsider whether a new skill is justified.

### Task 1: Initialize the Skill and Add the Research Evidence Layer

**Files:**
- Create: `skills/technical-research/references/evidence-and-sources.md`
- Create: `skills/technical-research/references/database-and-systems.md`
- Create: `skills/technical-research/references/paper-and-product-review.md`
- Generated but not yet finalized: `skills/technical-research/SKILL.md`
- Generated but not yet finalized: `skills/technical-research/agents/openai.yaml`

**Interfaces:**
- Consumes: the approved design at `docs/superpowers/specs/2026-07-20-technical-research-skill-design.md` and the source template at `/Users/zhangxiahao/Downloads/technical-research-article-prompt-template.md`.
- Produces: three directly loadable reference contracts that Task 3 links from `SKILL.md`.

- [ ] **Step 1: Confirm the task starts from a clean, expected checkout**

Run:

```bash
git status --short
git branch --show-current
test -f docs/superpowers/specs/2026-07-20-technical-research-skill-design.md
test -f /Users/zhangxiahao/Downloads/technical-research-article-prompt-template.md
test ! -e skills/technical-research
```

Expected: no status output, branch name is displayed, both input files exist, and `skills/technical-research` does not yet exist. If the directory exists, inspect it and reconcile scope instead of overwriting it.

- [ ] **Step 2: Initialize the skill with only the required resource directories**

Run:

```bash
python3 /Users/zhangxiahao/.codex/skills/.system/skill-creator/scripts/init_skill.py \
  technical-research \
  --path skills \
  --resources references,assets \
  --interface 'display_name=技术主题深度调研' \
  --interface 'short_description=综合论文、源码、开源系统与工业产品，生成经过验证的飞书技术调研报告' \
  --interface 'default_prompt=使用 $technical-research 对这个技术主题进行深度调研，并创建包含架构图、流程图、方案比较和证据说明的飞书云文档。'
```

Expected: `skills/technical-research/` contains `SKILL.md`, `agents/openai.yaml`, `references/`, and `assets/`; it contains no `scripts/` directory.

- [ ] **Step 3: Run the evidence-reference contract check before writing**

Run:

```bash
test -f skills/technical-research/references/evidence-and-sources.md && \
test -f skills/technical-research/references/database-and-systems.md && \
test -f skills/technical-research/references/paper-and-product-review.md
```

Expected: FAIL because the three reference files do not exist yet.

- [ ] **Step 4: Write `evidence-and-sources.md`**

Create a concise imperative reference with these exact sections and rules:

```markdown
# 证据与来源规则

## 来源优先级
1. 论文正文、附录和补充材料。
2. 官方规格、文档、源码、发布说明和项目仓库。
3. 官方工程博客、公开演讲和设计文档。
4. 独立基准、复现报告和可信技术分析。
5. 二手综述只作为检索线索。

## 纳入与排除
- 纳入与研究问题直接相关、身份和版本可确认、能够支撑具体主张的来源。
- 排除无法定位原始出处、只复述营销内容、版本不明且影响结论、只有关键词关联或重复转载的材料。

## 证据账本
为每条关键主张记录 Claim、Evidence class、Source、Location、Time/version、Confidence、Conflict 和 Usage。

## 强制边界
- 定量结果保留数据集、工作负载、基线、指标和实验条件。
- 将官方宣称与独立验证事实分开。
- 将未公开实现标记为推断，不把架构猜测写成事实。
- 并列呈现来源冲突及可能原因。
- 证据不足时缩小结论，并明确列出缺口。

## 引用
- 对关键事实、数字、产品能力和时间信息就近给出稳定来源。
- 记录论文页码、图表编号、源码版本和文件位置。
- 文末参考资料必须覆盖正文的关键主张。
```

Keep the final file imperative and remove explanatory duplication already present in `SKILL.md`.

- [ ] **Step 5: Write `database-and-systems.md`**

Create these sections with actionable checklists:

```markdown
# 数据库与系统分析维度

## 使用条件
仅在主题涉及数据库、存储、查询引擎、分布式系统或 AI Infra 时读取本文件。

## 架构和状态
- 定位能力所属的逻辑层、物理组件、持久化状态和元数据。
- 画出请求流、数据流、控制流以及跨节点边界。

## 正确性和失败语义
- 声明事务边界、隔离级别、一致性模型、可见性规则和持久化点。
- 检查崩溃、重试、重复执行、并发、部分失败、网络分区和恢复行为。
- 区分论文定义、官方保证、源码事实和独立推断。

## 性能路径
- 分别分析写入、存储、执行、事务和分布式链路。
- 关注吞吐、尾延迟、CPU、内存、I/O、网络、放大、缓存、队列和资源竞争。
- 检查比较是否存在热缓存、数据集规模、运行时长、基线公平性和多变量变化问题。

## 工程落地
- 分析兼容性、迁移、升级、可观测性、容量、成本、回滚和生产运维要求。
- 无实测证据时给出验证计划，不发明基准或生产结论。
```

- [ ] **Step 6: Write `paper-and-product-review.md`**

Create these sections and preserve the distinction between research and products:

```markdown
# 论文、开源系统与产品分析

## 选择代表性研究
- 按技术路线、问题分解或架构代际组织论文，不按时间简单罗列。
- 每篇只保留与主题相关的背景、方法、实验、局限和技术位置。
- 需要完整单篇论文批判时切换到 `$research-paper`。

## 审查实验
- 记录数据集、工作负载、基线、指标、配置、消融和失败案例。
- 判断证据能支持和不能支持哪些结论。
- 不将相对提升改写为绝对百分点。

## 分析系统与产品
- 区分 API、函数封装、开发框架、执行引擎、数据库、平台和完整基础设施。
- 记录定位、接口、公开实现证据、成熟度、版本、成本、可靠性和治理约束。
- 将商业产品未公开的内部机制标记为推断。

## 横向比较
- 使用统一工作负载、语义、版本和指标口径。
- 比较定位、系统形态、数据模型、核心机制、正确性、性能、扩展性、成本、成熟度、适用场景和局限。
- 解释差异的架构根因，不停留在功能清单。
```

- [ ] **Step 7: Verify the three reference files**

Run:

```bash
test -f skills/technical-research/references/evidence-and-sources.md && \
test -f skills/technical-research/references/database-and-systems.md && \
test -f skills/technical-research/references/paper-and-product-review.md && \
rg -F 'Evidence class' skills/technical-research/references/evidence-and-sources.md && \
rg -F '崩溃、重试' skills/technical-research/references/database-and-systems.md && \
rg -F '$research-paper' skills/technical-research/references/paper-and-product-review.md && \
git diff --check
```

Expected: all commands exit 0; the three required boundary strings are printed; `git diff --check` is silent.

- [ ] **Step 8: Commit the evidence layer**

```bash
git add skills/technical-research/references/evidence-and-sources.md \
  skills/technical-research/references/database-and-systems.md \
  skills/technical-research/references/paper-and-product-review.md
git diff --cached --check
git commit -m "feat(technical-research): add research evidence framework"
```

Expected: one commit containing only the three reference files. Generated scaffold files remain untracked for Task 2 and Task 3.

### Task 2: Define Feishu Delivery and the Report Asset

**Files:**
- Create: `skills/technical-research/references/feishu-delivery.md`
- Create: `skills/technical-research/assets/report-outline.md`

**Interfaces:**
- Consumes: current `lark-shared`, `lark-doc`, and `lark-whiteboard` skills at execution time.
- Produces: the delivery contract and report skeleton linked by Task 3.

- [ ] **Step 1: Run the delivery-resource check before writing**

Run:

```bash
test -f skills/technical-research/references/feishu-delivery.md && \
test -f skills/technical-research/assets/report-outline.md
```

Expected: FAIL because both files are absent.

- [ ] **Step 2: Write `feishu-delivery.md`**

Create an imperative reference containing these contracts:

```markdown
# 飞书云文档交付

## 认证门禁
1. 在完整调研前按照 `lark-shared` 检查用户身份、令牌和所需权限。
2. 未授权或令牌失效时发起最小权限的分步授权，展示链接和二维码，然后暂停任务。
3. 用户返回后完成授权并重新验证；不要仅凭口头确认继续。
4. 不保存令牌、授权链接或设备码。

## 写入方式
- 按 `lark-doc` 当前规则创建原生飞书云文档，默认使用 XML。
- 长文档先创建标题和章节骨架，再按章节写入正文、表格、代码块、图形和参考资料。
- 使用 `lark-whiteboard` 或 Mermaid 表达架构、流程和状态；实验图表可重绘为本地 PNG 后上传。
- 为每幅图添加标题、图注、来源和推断标记。

## 本地图片
1. 将生成图片放在临时工作目录。
2. 在正文建立唯一锚点。
3. 上传图片并取得 block ID。
4. 将图片移动到锚点之后，补充图注并删除锚点。
5. 回读验证后清理临时文件。

## 失败恢复
- 创建失败时不返回虚假链接。
- 章节失败时修复同一文档，避免重复创建。
- 图片或画板失败时记录具体对象，缺图文档不算完成。
- 文档不可恢复时说明原因，再创建替代文档。

## 回读验证
- 检查标题、章节、表格、代码块、图片、画板、图注和参考资料。
- 删除临时锚点和未替换变量。
- 验证当前用户可以读取文档。
- 只有回读通过、无未报告的部分失败并返回文档 URL 时才算完成。
```

Link conceptually to the current Lark skills; do not embed exact authorization scopes or version-sensitive command examples.

- [ ] **Step 3: Write `report-outline.md`**

Create this adaptable output asset:

```markdown
# {{技术主题}}：技术调研报告

> 范围：{{研究范围}}
> 时间截点：{{核验日期}}
> 目标读者：{{目标读者}}

## 核心结论

## 问题背景与技术边界

## 整体架构与关键数据流

## 核心机制

## 技术路线与代表性论文

## 开源系统与工业产品

## 横向比较

## 工程落地判断

## 风险、局限与未解决问题

## 未来演进判断

## 总结

## 参考资料与证据说明
```

Add one instruction above or below the outline: remove inapplicable sections instead of filling them with generic prose, but retain scope, conclusions, evidence limitations, and references.

- [ ] **Step 4: Verify delivery and report resources**

Run:

```bash
rg -F '按照 `lark-shared`' skills/technical-research/references/feishu-delivery.md
rg -F '缺图文档不算完成' skills/technical-research/references/feishu-delivery.md
rg -F '## 整体架构与关键数据流' skills/technical-research/assets/report-outline.md
rg -F '## 参考资料与证据说明' skills/technical-research/assets/report-outline.md
git diff --check
```

Expected: each required line is printed and `git diff --check` is silent.

- [ ] **Step 5: Commit the delivery resources**

```bash
git add skills/technical-research/references/feishu-delivery.md \
  skills/technical-research/assets/report-outline.md
git diff --cached --check
git commit -m "feat(technical-research): define Feishu report delivery"
```

Expected: one commit containing only the Feishu reference and report asset.

### Task 3: Implement the Core Skill and UI Metadata

**Files:**
- Modify: `skills/technical-research/SKILL.md`
- Modify: `skills/technical-research/agents/openai.yaml`

**Interfaces:**
- Consumes: all four files in `skills/technical-research/references/` and `assets/report-outline.md`.
- Produces: the callable `$technical-research` workflow and UI metadata used by README and forward tests.

- [ ] **Step 1: Replace the generated `SKILL.md` with a deliberately failing minimal contract check**

Before editing, run:

```bash
rg -F '先验证飞书授权' skills/technical-research/SKILL.md && \
rg -F 'references/evidence-and-sources.md' skills/technical-research/SKILL.md && \
rg -F 'assets/report-outline.md' skills/technical-research/SKILL.md
```

Expected: FAIL because the generated scaffold does not implement the approved workflow.

- [ ] **Step 2: Write the final frontmatter and core workflow**

Replace the scaffold with a concise imperative `SKILL.md` using only `name` and `description` in frontmatter:

```yaml
---
name: technical-research
description: Use when researching a database, distributed-systems, AI Infra, storage, query-optimization, or systems-software topic across papers, official documentation, source code, open-source systems, industry products, and public engineering evidence, with the result delivered as a verified Chinese Feishu cloud document.
---
```

The body must contain these sections and actions:

```markdown
# 技术主题深度调研

## 核心原则
围绕技术主题建立跨来源证据链，先形成可证伪的工程判断，再组织报告。不要把论文摘要、产品功能和二手文章堆叠成综述。

## 先验证飞书授权
- 在完整调研前遵循 `references/feishu-delivery.md` 的认证门禁。
- 授权无效时先发起授权并暂停；验证成功后再继续。

## 确认范围
- 要求技术主题；按默认值补齐时间、读者、论文、产品、长度和分析重点。
- 只有缺失信息会实质改变结论时才追问。
- 定义工作定义、相邻边界、评价维度、时间截点和非目标。

## 建立研究计划和证据账本
- 阅读 `references/evidence-and-sources.md`。
- 主题涉及数据库或系统软件时读取 `references/database-and-systems.md`。
- 需要分析论文、开源系统或产品时读取 `references/paper-and-product-review.md`。
- 在写作前记录关键主张、来源位置、版本、置信度和冲突。

## 执行分轨分析
1. 概念与历史。
2. 机制与架构。
3. 学术研究。
4. 系统与产品。
5. 综合判断。

## 组织报告
- 使用 `assets/report-outline.md` 作为可裁剪骨架。
- 先给结论；解释设计原因、收益、代价和成立条件。
- 默认至少提供有信息量的架构图、流程或状态图、比较表和代码类块；不适用时使用更准确的替代表达并说明原因。
- 将事实、论文结论、官方宣称、外部证据和独立判断分开。

## 创建并验证飞书云文档
- 按 `references/feishu-delivery.md` 创建原生飞书云文档。
- 创建后回读检查结构、图形、代码、引用、证据边界和当前用户可访问性。
- 只有验证通过才返回文档 URL；列出仍未验证的内容和证据缺口。

## 可选公众表达
- 只有用户明确要求对外发布或面向大众时，增加直观例子并解释术语。
- 不因简化表达删除正确性、限制条件、证据边界或不确定性。
```

Keep `SKILL.md` under 500 lines and link every bundled resource directly from it.

- [ ] **Step 3: Regenerate `agents/openai.yaml` from the final skill**

Run:

```bash
python3 /Users/zhangxiahao/.codex/skills/.system/skill-creator/scripts/generate_openai_yaml.py \
  skills/technical-research \
  --interface 'display_name=技术主题深度调研' \
  --interface 'short_description=综合论文、源码、开源系统与工业产品，生成经过验证的飞书技术调研报告' \
  --interface 'default_prompt=使用 $technical-research 对这个技术主题进行深度调研，并创建包含架构图、流程图、方案比较和证据说明的飞书云文档。'
```

Expected `agents/openai.yaml`:

```yaml
interface:
  display_name: "技术主题深度调研"
  short_description: "综合论文、源码、开源系统与工业产品，生成经过验证的飞书技术调研报告"
  default_prompt: "使用 $technical-research 对这个技术主题进行深度调研，并创建包含架构图、流程图、方案比较和证据说明的飞书云文档。"
```

- [ ] **Step 4: Run the core contract checks**

Run:

```bash
rg -F 'name: technical-research' skills/technical-research/SKILL.md
rg -F '先验证飞书授权' skills/technical-research/SKILL.md
rg -F 'references/evidence-and-sources.md' skills/technical-research/SKILL.md
rg -F 'references/database-and-systems.md' skills/technical-research/SKILL.md
rg -F 'references/paper-and-product-review.md' skills/technical-research/SKILL.md
rg -F 'references/feishu-delivery.md' skills/technical-research/SKILL.md
rg -F 'assets/report-outline.md' skills/technical-research/SKILL.md
test "$(wc -l < skills/technical-research/SKILL.md)" -lt 500
test ! -d skills/technical-research/scripts
git diff --check
```

Expected: all required paths and headings are printed; line-count and directory checks pass; `git diff --check` is silent.

- [ ] **Step 5: Validate the skill with the official validator**

Run:

```bash
python3 /Users/zhangxiahao/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  skills/technical-research
```

Expected: validation success. If the only failure is `ModuleNotFoundError: yaml`, use a temporary dependency without changing repository dependencies:

```bash
python3 -m pip install --target /tmp/codex-skill-validator-deps PyYAML
PYTHONPATH=/tmp/codex-skill-validator-deps \
  python3 /Users/zhangxiahao/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  skills/technical-research
```

Expected: validation success.

- [ ] **Step 6: Commit the callable skill**

```bash
git add skills/technical-research/SKILL.md \
  skills/technical-research/agents/openai.yaml
git diff --cached --check
git commit -m "feat(technical-research): add topic research workflow"
```

Expected: one commit containing only `SKILL.md` and `agents/openai.yaml`.

### Task 4: Add the Standalone Prompt Template and Invocation Index

**Files:**
- Create: `prompt_templates/technical-research/prompt_template.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: the supplied template, final skill boundaries, and `$technical-research` invocation name.
- Produces: a standalone prompt and a discoverable repository index entry.

- [ ] **Step 1: Run the integration check before writing**

Run:

```bash
test -f prompt_templates/technical-research/prompt_template.md && \
rg -F '$technical-research' README.md
```

Expected: FAIL because neither integration entry exists.

- [ ] **Step 2: Create the prompt-template directory and write the standalone prompt**

Create `prompt_templates/technical-research/prompt_template.md`. Preserve the supplied template's variables and useful research questions, but consolidate repeated standard, concise, and database-enhanced variants into one direct prompt with these exact major sections:

```markdown
# 技术主题深度调研提示词模板

请你以资深技术研究员和系统架构师的视角，对「{{技术主题}}」进行深度调研，并直接创建一篇可独立阅读的中文飞书云文档。

## 输入
- 时间范围：{{时间范围；默认不限制历史起点，重点核验最近三至五年}}
- 重点论文：{{重点论文或链接；可选}}
- 重点系统或产品：{{公司、数据库、开源项目或云服务；可选}}
- 分析重点：{{架构、存储、查询优化、事务、分布式、AI Infra 等；可选}}
- 目标读者：{{默认数据库、分布式系统或 AI Infra 研发人员}}

## 调研问题
1. 技术背景、准确概念、工作定义和相邻边界是什么？
2. 整体架构、状态、元数据、关键数据流和执行流程是什么？
3. 核心算法、数据结构、正确性、失败语义和性能路径是什么？
4. 代表性论文、开源系统和工业产品分别提供了什么证据？
5. 不同方案在语义、性能、成本、扩展性、稳定性和运维性上为何不同？
6. 当前局限、未解决问题和未来演进是什么？

## 来源与证据
- 优先使用论文原文、官方文档、源码、仓库、发布说明和公开工程材料。
- 区分直接事实、论文结论、官方宣称、外部证据和独立判断。
- 为关键事实、数字、产品能力和时间信息提供来源。
- 来源冲突时并列说明，证据不足时缩小结论。

## 报告要求
- 先给结论，再展开论证；文章可独立阅读。
- 按技术路线或问题组织论文，不按时间简单罗列。
- 解释设计原因、收益、代价、成立条件和适用边界。
- 使用有信息量的架构图、流程或状态图、比较表，以及代码、伪代码、SQL、执行计划、配置或协议交互块。
- 对数据库和系统主题分析正确性、恢复、写入、存储、执行、事务、分布式、可观测性和工程成本。
- 创建后验证飞书云文档，并返回链接和仍未验证的证据缺口。
```

Do not retain three duplicate full prompt variants. Keep optional public-audience wording as one short conditional instruction.

- [ ] **Step 3: Add the README index row**

Add this row to the existing skill table, preserving current ordering style:

```markdown
| 技术主题深度调研 | `$technical-research` | `skills/technical-research/` |
```

- [ ] **Step 4: Verify prompt and index integration**

Run:

```bash
test -f prompt_templates/technical-research/prompt_template.md
rg -F '{{技术主题}}' prompt_templates/technical-research/prompt_template.md
rg -F '直接事实、论文结论、官方宣称、外部证据和独立判断' \
  prompt_templates/technical-research/prompt_template.md
rg -F '创建后验证飞书云文档' prompt_templates/technical-research/prompt_template.md
rg -F '| 技术主题深度调研 | `$technical-research` | `skills/technical-research/` |' README.md
git diff --check
```

Expected: every required string is printed and `git diff --check` is silent.

- [ ] **Step 5: Commit the prompt and index**

```bash
git add prompt_templates/technical-research/prompt_template.md README.md
git diff --cached --check
git commit -m "docs(technical-research): add prompt template and index"
```

Expected: one commit containing only the prompt template and README.

### Task 5: Validate the Integrated Skill and Forward-Test Its Behavior

**Files:**
- Verify: `skills/technical-research/**`
- Verify: `prompt_templates/technical-research/prompt_template.md`
- Verify: `README.md`
- Modify only if a validation result exposes a concrete defect in those files.

**Interfaces:**
- Consumes: the complete skill and a valid Feishu user authorization.
- Produces: evidence that the skill triggers correctly, enforces authentication, separates evidence classes, creates meaningful visuals, and returns verified Feishu document URLs.

- [ ] **Step 1: Run the full static validation suite**

Run:

```bash
python3 /Users/zhangxiahao/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  skills/technical-research
git diff --check
git status --short
find skills/technical-research -maxdepth 3 -type f | sort
```

If PyYAML is absent, use the temporary `PYTHONPATH` fallback from Task 3. Expected: validator success, no whitespace errors, no unintended working-tree changes, and exactly the designed skill files.

- [ ] **Step 2: Audit trigger separation from `$research-paper`**

Use these two requests in fresh task contexts:

```text
Use $technical-research to research disaggregated storage and compute architectures across papers, open-source databases, and cloud products, then create the Feishu report.
```

```text
Use $research-paper to critically interpret this one paper, including its experiment design and appendix.
```

Expected: the first follows the topic-level multi-source workflow; the second remains a single-paper deep interpretation. Record any accidental overlap before editing the descriptions.

- [ ] **Step 3: Forward-test the database topic path**

Use a fresh agentic task with only the skill path and this request:

```text
Use $technical-research to investigate learned cardinality estimation for relational query optimizers. Compare representative papers, open-source implementations, and production constraints, and create a concise Feishu cloud document for optimizer engineers.
```

Expected checks:

- authorization is verified before full research;
- papers are grouped by technical route;
- claims distinguish experiments, implementation facts, and independent judgment;
- the document contains an optimizer architecture diagram, an estimation or planning flow, a comparison table, and a pseudocode or plan example;
- the returned Feishu URL can be fetched by the current user.

- [ ] **Step 4: Forward-test the distributed-systems topic path**

Use a fresh agentic task:

```text
Use $technical-research to investigate online membership changes in consensus systems. Compare protocol approaches, failure semantics, and representative implementations, and create a Feishu cloud document for distributed-systems engineers.
```

Expected checks:

- safety invariants, partial failures, retries, and recovery are explicit;
- protocol claims cite papers, specifications, or source code;
- the document contains a state or message-flow diagram and implementation-oriented pseudocode;
- marketing or unsupported product claims are not treated as verified facts.

- [ ] **Step 5: Forward-test the AI Infra topic path**

Use a fresh agentic task:

```text
Use $technical-research to investigate continuous batching for LLM inference. Compare research methods, open-source inference engines, and production trade-offs, and create a Feishu cloud document for AI Infra engineers.
```

Expected checks:

- the database-specific reference is not mechanically imposed where irrelevant;
- scheduling, memory, latency, throughput, fairness, and workload assumptions are separated;
- the document contains a serving architecture diagram, request lifecycle flow, comparison table, and scheduler pseudocode;
- time-sensitive engine capabilities include versions or verification dates.

- [ ] **Step 6: Review the three outputs without leaking expected answers into revisions**

For each output, record only observable defects:

```text
Triggering:
Authorization gate:
Source quality:
Evidence classification:
Architecture and flow visuals:
Code-like explanation:
Feishu structure:
Post-write verification:
Unverified gaps disclosed:
```

Expected: all fields can be answered from the produced artifact and execution trace. If a failure is topic-specific, change only the relevant reference; if it affects orchestration, change `SKILL.md`.

- [ ] **Step 7: Re-run validation after any forward-test fixes**

Run:

```bash
python3 /Users/zhangxiahao/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  skills/technical-research
git diff --check
git diff --stat HEAD
```

Expected: validator success and only concrete forward-test fixes in the diff. If no files changed, do not create an empty commit.

- [ ] **Step 8: Commit validated fixes when needed**

If forward testing changed files:

```bash
git add skills/technical-research prompt_templates/technical-research README.md
git diff --cached --check
git commit -m "fix(technical-research): address forward-test gaps"
```

Expected: a focused fix commit. If no changes were needed, skip this step.

- [ ] **Step 9: Perform final repository verification**

Run:

```bash
git status --short
git log -5 --oneline --decorate
git show --stat --oneline --summary HEAD
test -f skills/technical-research/SKILL.md
test -f prompt_templates/technical-research/prompt_template.md
rg -F '$technical-research' README.md
```

Expected: clean status, intended commits visible, all final paths present, and the README invocation row printed. Report the exact validator result, forward-test topics, Feishu document links, known evidence gaps, and the fact that nothing was pushed and no PR was created.
