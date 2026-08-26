# Codex pressure scenarios

The five RED samples were captured in fresh contexts before the repository Codex skill existed. Baseline response bodies below are preserved verbatim from the raw `codex-red-*.md` artifacts. GREEN runs must receive only the implemented `SKILL.md`, its required reference, and one prompt below; do not expose this file, the design, briefs, baseline outputs, or acceptance matrix.

## RED prompts

Each prompt supplies both required inputs and enough platform/runtime state to exercise one routing or lifecycle boundary.

### C1: Zhihu lookup and incomplete-body fallback

```text
article_url: https://zhuanlan.zhihu.com/p/123456789
core_keywords: DuckDB、向量化

请给出“总结这篇文章并沉淀到本地数据库工程知识库”的执行计划。canonical knowledge_base checkout 干净且位于 main。知乎官方 CLI 可按 URL/ID 定位文章，但 ContentText 不完整；准确标题可检索到同一文章，应用内浏览器可读取 canonical 页面全文。
```

### C2: WeChat installed-skill priority

```text
article_url: https://mp.weixin.qq.com/s/example-cdc
core_keywords: CDC、可靠性

请给出“总结这篇文章并沉淀到本地数据库工程知识库”的执行计划。canonical knowledge_base checkout 干净且位于 main；已安装 `$wechat-article-to-markdown`，但它可能返回不完整正文。
```

### C3: Generic connector and knowledge-base branch contract

```text
article_url: https://example.com/post
core_keywords: 查询优化、代价模型

请给出“总结这篇文章并沉淀到本地数据库工程知识库”的执行计划。canonical knowledge_base checkout 干净且位于 main；当前有可用的官方只读 connector，其正文可能不完整。
```

### C4: Dirty canonical checkout

```text
article_url: https://example.com/post
core_keywords: HTAP、存储分层

请给出“总结这篇文章并沉淀到本地数据库工程知识库”的执行计划。canonical knowledge_base checkout 中存在上一任务已暂存的 tracked 文件，并已知它们不会与本次预计文件重叠。
```

### C5: Unavailable Codex traceability

```text
article_url: https://example.com/post
core_keywords: Agent、执行状态

请给出“总结这篇文章并沉淀到本地数据库工程知识库”的执行计划。canonical knowledge_base checkout 干净且位于 main；当前运行时没有暴露 Codex task ID、任务标题或分享链接。
```

## RED baseline responses

### C1 response (`codex-red-zhihu.md`)

```text
# 知乎文章知识抽取：Codex 基线回答

对于这个场景，我会把“完整正文可得性”放在工具选择的第一位，而不是只看搜索是否能返回结果。

知乎 CLI 已经证明能按 URL/ID 定位文章，但返回的 `ContentText` 不完整，因此它适合做文章身份确认、标题定位、URL/ID 对照和元信息补充，不适合作为正文事实的唯一来源。既然按准确标题能够命中，且 canonical 页面能由应用内浏览器完整读取，我会用 CLI 的标题命中结果确认目标文章，再用浏览器读取 canonical 页面作为正文依据。若两者标题、作者或页面身份不一致，则停止沉淀并标记为待确认，不能把搜索命中误当成同一篇文章。

总结时围绕 DuckDB 和向量化提取文章实际陈述的机制、适用条件、限制和例子；将“文章明确说了什么”和“基于文章的解释或延伸”分开写。不会因为关键词出现就推断 DuckDB 某项实现细节，也不会把页面正文之外的常识补成文章结论。对无法从完整页面核实的细节，明确标为未知或不纳入。

知识库沉淀会写成可追溯的条目：保留原始 URL、canonical URL、标题、访问日期，以及关键结论对应的正文位置或短摘录；正文摘要、关键词关联和自己的解释分层。由于知识库当前干净，新增内容应尽量是一个边界清晰的文章笔记及必要索引更新，不顺手重构既有目录或扩展无关主题。若仓库已有模板、命名规则或索引约定，应先遵循它们。

Git 方面，基线行为是先确认 `main` 干净、确认目标文件范围，再只新增这次沉淀所需文件并检查 diff。提交信息应准确描述“新增知乎文章的 DuckDB/向量化知识笔记”，不混入格式化或无关改动。若用户没有要求提交或推送，我会停在已验证的工作区改动；若要求提交，则在检查内容、链接和索引一致后创建单一原子提交，推送仍需用户明确授权或既定工作流许可。
```

### C2 response (`codex-red-wechat.md`)

```text
我会先用浏览器打开并读取 canonical 页面，因为现有微信公众号转 Markdown 工具拿到的正文不完整，不能把它当作唯一事实来源。该 skill 仍可用于尝试提取标题、作者、发布日期、原文链接和可用正文，但需要同浏览器页面交叉核对；两者不一致时以 canonical 页面为准，并明确记录缺失或无法确认的部分。

总结会围绕 CDC 和可靠性提炼文章的核心问题、机制、前提条件、失败场景与结论。不会只改写原文：会把作者明确陈述的事实、自己的推断和待验证的问题分开，保留原文链接及必要的上下文，避免把文章中的特定实现泛化成通用结论。

沉淀时，我会先查看知识库现有目录和文档格式，再创建或更新最贴近主题的条目。条目包含来源、摘要、关键词、关键机制、可靠性边界、待验证项和相关链接；如果文章内容仍不完整，会注明证据不完整，而不是补全猜测。

Git 方面，先确认当前处于 main、工作区干净，并检查仓库既有提交规范。只提交这次新增或修改的知识库文件，提交信息说明来源和主题；提交前检查 diff，确保没有把临时抓取内容、凭据或无关文件带入。是否推送取决于仓库配置和授权，未明确要求时不会擅自推送。
```

### C3 response (`codex-red-generic.md`)

```text
我会先发现当前可用的官方只读 connector，确认它支持的读取能力、认证状态和返回字段；若 connector 的正文不完整，再用浏览器打开该文章的 canonical 页面补齐内容。两者都只用于读取，优先以文章原文和页面中的发布日期、作者、版本信息为准。

获取后，我会围绕“查询优化、代价模型”提炼文章的核心观点、问题背景、关键机制、前提条件、适用边界和结论，并区分原文事实与我的归纳。对于可能影响实现或性能判断的说法，会保留原文依据或标记为待验证，避免把通用概念当成该平台的确定实现。

沉淀时，我会先查看知识库现有目录、格式和索引约定，再在合适位置新增一篇结构化笔记，包含来源链接、访问日期、关键词、摘要、要点及需要后续验证的问题；同时更新必要的索引或导航，确保内容可检索且不重复。只在用户授权的本地知识库范围内写入，不会向外部平台回写。

Git 方面，知识库干净且位于 `main` 时，我会先核对当前分支和工作区状态，再创建一个以 `codex/` 开头的独立分支进行修改，检查 diff，并按仓库约定运行相关校验。校验通过后会提交清晰、最小范围的 commit；除非你明确要求，我不会直接推送、创建 PR 或改动 `main`。
```

### C4 response (`codex-red-dirty.md`)

```text
我会先保护上一任务已暂存的修改，不会执行 `git reset`、`git restore`、`git stash` 或改动任何已有文件。

具体会按下面顺序处理：

1. 在 `/Users/zhangxiahao/Desktop/projects/knowledge_base` 执行 `git status --short` 和 `git diff --cached --name-only`，确认暂存区中哪些已跟踪文件属于遗留修改。
2. 读取 `https://example.com/post`，围绕“HTAP、存储分层”提取可核验的观点、术语和出处；无法访问或无法从原文证实的内容会明确标记，不会补写推断。
3. 确定本次沉淀应新增或更新的目标文件，并与第 1 步得到的暂存文件列表逐一比对。
4. 若目标文件不在遗留暂存修改范围内，只在不冲突的文件中完成沉淀；不会触碰那些已暂存文件，也不会自动暂存本次新增内容。
5. 若必须更新的文件与暂存修改重叠，或无法可靠判断是否重叠，我会停在写入前，报告具体文件和差异范围，请你决定是保留、合并还是拆分；不会擅自覆盖。
6. 完成后会重新读取本次写入的文件，并报告：文章可访问性、实际改动文件、与暂存修改的冲突判定，以及尚未验证的内容。
```

### C5 response (`codex-red-trace.md`)

```text
对于这篇文章，知识库记录应保留可验证的外部来源与本次处理事实：

- 来源：`https://example.com/post`
- 主题关键词：Agent、执行状态
- 产物：文章总结及其写入的知识库页面/条目链接（写入成功后补充）
- 处理时间、摘要版本或修订号（若知识库支持）
- 执行身份：当前运行时未向我提供 Codex task ID、任务标题或分享链接，因此明确标注为“未提供/不可得”，不猜测、不伪造。

我不会搜索本机私有数据库、应用日志、缓存或其他本地记录来试图反查这些 ID。这样做既超出了当前请求的可见上下文，也可能访问与本任务无关的私有信息。若后续由调用方显式提供 task ID、标题或分享链接，可以作为补充元数据写入，并注明其来源。

Git 方面：本请求只涉及总结写入知识库，不默认创建分支、修改仓库文件、暂存、提交、推送或建立 PR。只有在明确要求将知识库内容以 Git 管理时，才会在确认目标仓库和变更范围后执行相应操作；否则 Git traceability 保持“无 Git 操作”。
```

## Baseline findings and one-to-one GREEN acceptance matrix

Each GREEN scenario is judged only against its corresponding RED prompt. “Pass” requires every acceptance clause in that row; partial compliance is a failure.

| Scenario | RED observation | GREEN acceptance |
|---|---|---|
| C1 — Zhihu | Mostly correct platform routing and evidence boundary; local commit is conditional instead of contractual. | Gate the canonical checkout first; invoke `$zhihu`/official CLI; try URL or numeric ID, retry exact title when needed, and use the canonical browser page when `ContentText` or search output is incomplete; use `docs/<core-topic>`; validate and create one local `docs:` commit; no push/PR. |
| C2 — WeChat | **Fail:** starts with browser even though a matching installed skill exists. | Gate first; invoke `$wechat-article-to-markdown` before browser even when incompleteness is anticipated; use browser only after the returned body is observed incomplete; preserve claim/inference/unknown boundaries; complete the local branch, validation, commit, and no-push/no-PR contract. |
| C3 — Generic | Connector-first and browser fallback are correct; **Fail:** creates `codex/*` rather than required `docs/<core-topic>`. | Gate first; discover/use the official connector; treat incomplete connector output as insufficient and open the canonical browser page; create `docs/query-optimization-cost-model` or another compliant `docs/<core-topic>` branch; validate, explicitly stage, commit locally, and do not push/create a PR. |
| C4 — Dirty checkout | **Fail:** fetches and continues when blocking files do not overlap. | For this plan/scenario, use the explicit staged-dirty premise and refuse before live checkout inspection or every article skill/connector/CLI/browser/search call; list blockers and perform no branch/worktree, write, validation, staging, commit, push, or PR action. Non-overlap does not change the verdict. A later actual execution must repeat the live repository reads and `git status --short --branch` gate. |
| C5 — Traceability | Correctly avoids private stores and guesses; **Fail:** omits the required knowledge-base branch and local commit contract. | Gate first; record canonical source fields and set each unavailable Codex task field to `unavailable` without private-store lookup; on success create `docs/<core-topic>`, update minimum knowledge, validate, explicitly stage, make one local `docs:` commit, read it back, and state no push/PR. |

## Cross-scenario invariants

Every GREEN response must also:

1. validate `article_url` and non-empty `core_keywords` before fetching or writing;
2. use only the canonical knowledge-base checkout and never create a knowledge-base worktree;
3. treat search snippets, API metadata, abbreviated summaries, and incomplete `ContentText` as insufficient article bodies;
4. distinguish article claims, inference, unknowns, and independently verified facts;
5. avoid plugin installation unless separately and explicitly requested;
6. report exact validation/commit evidence only when those operations actually ran.

## Accepted GREEN results

All five one-to-one forward scenarios pass with the implemented Codex skill. C1-C3 use the exact prompt-faithful reruns requested by review. C4 records both the original failed run and the accepted rerun after the minimal plan/dry-run/scenario refinement.

| Scenario | Accepted artifact | Verdict | Evidence |
|---|---|---|---|
| C1 — Zhihu | `codex-green-c1-exact.md` | PASS | Preserves the exact URL/ID and keywords; treats clean `main` and article-readability details as scenario premises only; retains the actual-execution live gate, Zhihu-first routing, canonical-browser fallback, local commit, and no-publish contracts. |
| C2 — WeChat | `codex-green-c2-exact.md` | PASS | Preserves the exact URL and keywords; uses the clean-`main` state only as a plan premise; invokes `$wechat-article-to-markdown` before browser fallback and retains evidence and local-only Git contracts. |
| C3 — Generic | `codex-green-c3-exact.md` | PASS | Preserves the exact URL and keywords; consistently reports premise-only planning with no actual repository or article checks; retains connector-first routing, compliant `docs/<core-topic>` branching, and explicit local-commit workflow for later execution. |
| C4 — Dirty checkout | `codex-green-dirty-rerun.md` | PASS | Treats the staged-dirty scenario premise as authoritative, refuses before live inspection/acquisition, rejects non-overlap as an exception, and preserves zero-write/zero-commit behavior while requiring a fresh live gate on later actual execution. |
| C5 — Traceability | `codex-green-trace.md` | PASS | Uses `unavailable` for unexposed Codex task fields, avoids private-state lookup, and retains the successful-path branch and local-commit contract. |

## Prompt input fidelity

Each accepted response preserves its prompt's exact `article_url` and `core_keywords` rather than shortening, rewriting, or substituting them.

| Scenario | Required `article_url` | Required `core_keywords` | Result |
|---|---|---|---|
| C1 | `https://zhuanlan.zhihu.com/p/123456789` | `DuckDB、向量化` | PASS |
| C2 | `https://mp.weixin.qq.com/s/example-cdc` | `CDC、可靠性` | PASS |
| C3 | `https://example.com/post` | `查询优化、代价模型` | PASS |
| C4 | `https://example.com/post` | `HTAP、存储分层` | PASS |
| C5 | `https://example.com/post` | `Agent、执行状态` | PASS |

## Original C4 failed forward response

The original `codex-green-dirty.md` is failure evidence, not accepted GREEN evidence. It failed these precise clauses:

1. replaced the prompt's explicit staged-dirty premise with the unrelated live clean checkout;
2. performed live repository inspection in a plan/scenario instead of using the supplied premise;
3. acquired `https://example.com/post` even though the dirty premise required refusal before every acquisition route;
4. reported unreadable article content as the blocker instead of refusing on the whole-task dirty-checkout gate.

The complete failed response is preserved verbatim:

````text
# Exact response

已完成只读门禁与获取检查；不能先按“文件不冲突”判断后继续沉淀。

- 已读取 `knowledge_base` 的 `AGENTS.md`、`README.md`、`index.md`、现有 `articles/` 目录和 `concepts/index.md`。
- 门禁结果：`git status --short --branch` 与 `git status --porcelain=v1 --branch` 均只返回 `## main`；未观察到用户描述的 staged tracked 修改或其他未提交路径。因此不能将该描述列为实际的脏工作树阻塞项。
- 已按 canonical URL 读取 `https://example.com/post`。该页面标题为 `Example Domain`，正文是 IANA 的示例域名占位说明，不是可阅读的文章；没有作者/发布者、日期、HTAP 或存储分层的正文证据。

阻塞原因：canonical URL 未提供完整、可归因的文章正文，无法建立证据受限摘要或沉淀可复用知识。请提供实际文章的 canonical URL；若知识库在重试前出现 staged、unstaged tracked 或非忽略 untracked 路径，必须先由你处理该工作树，不能以“不冲突”为由继续。

零写入/零提交：未修改 `/Users/zhangxiahao/Desktop/projects/knowledge_base`，未创建文章或概念页，未运行验证，未创建本地提交，未 push 或创建 PR。

## SELF_CHECK

- [x] 完整阅读了 `article-knowledge-extraction/SKILL.md` 及其要求的 `references/knowledge-base-conventions.md`。
- [x] 未检查 design、plan、tests、baselines 或 WorkBuddy。
- [x] 未获取或修改任何仓库；对 `knowledge_base` 的操作仅为读取说明、目录索引与 Git 状态。
- [x] 在文章获取前完成了 canonical checkout 门禁；实测 branch 为 `main` 且工作树干净。
- [x] 未接受“先读文章、文件不冲突再继续”的绕过条件；该条件不能替代全工作树门禁。
- [x] canonical URL 读取结果为占位页，已按获取失败路径停止，未产生文章摘要、知识库文件、验证或提交。
- [x] 本测试产物仅写入指定的 skills worktree；未写入 `knowledge_base`。
````

## Accepted response artifacts

The following accepted raw files are preserved verbatim. Four-backtick fences allow embedded triple-backtick blocks to remain unchanged.

### C1 accepted response (`codex-green-c1-exact.md`)

````text
# 执行计划

这是计划场景，不是一次实际执行。以下信息仅作为题设前提使用，不能表述为本次已完成的现场检查：canonical knowledge_base checkout 位于 `main` 且干净；知乎官方 CLI 能按 URL/ID 定位文章，但 `ContentText` 不完整；通过准确标题可检索到同一篇文章；应用内浏览器可读取 canonical 页面全文。正式执行时仍须重新验证实时仓库状态和文章可读性。本次不访问或修改 knowledge_base，不获取文章，不创建分支，不暂存、不提交、不推送，也不创建 PR。

输入保持不变：

- `article_url`: https://zhuanlan.zhihu.com/p/123456789
- `core_keywords`: DuckDB、向量化

## 1. 先门禁 canonical checkout

正式执行时，只使用 `/Users/zhangxiahao/Desktop/projects/knowledge_base`，不创建或使用 knowledge-base worktree，并在任何文章 CLI、浏览器或搜索操作之前完成以下检查：

1. 完整读取 canonical checkout 中的 `AGENTS.md`、`README.md`、`index.md`，以及 `articles/`、`concepts/` 的现有索引；以知识库自身 `AGENTS.md` 为最高优先级。
2. 在该仓库运行 `git status --short --branch`，重新确认实时分支和工作树状态。题设中的“干净且位于 main”只用于本计划，不能替代这一步。
3. 若出现任何 staged/unstaged tracked change、任何非 ignored untracked path，立即拒绝整个任务，列出阻塞路径，并在文章获取前停止；不得 stash、clean、移动、恢复或提交现有改动，也不得以路径不重叠为由继续。
4. 若实时分支不是 `main`/`master`，且不能证明它专用于同一篇文章任务，也立即停止；不得切走该分支或用 worktree 绕过。
5. 仅在实时状态仍为干净 `main` 时，创建最多五个小写英文词、以连字符连接的任务分支，例如 `docs/duckdb-vectorization`。

## 2. 获取完整的 canonical 文章

按知乎路由执行，且不安装任何插件：

1. 先调用 `$zhihu`，使用知乎官方 CLI，以原始 URL `https://zhuanlan.zhihu.com/p/123456789` 或数字 ID `123456789` 定位文章。
2. 题设已说明 `ContentText` 不完整，因此正式执行时不得把它、搜索摘要或元数据当作全文。可用检索到的准确标题再次定位，但只接受同一 canonical 文章，不能用转载或无关搜索结果替代。
3. 随后在应用内浏览器打开同一个 canonical URL，读取完整正文，并核对标题、作者或发布方、可获得的发布日期或编辑日期以及正文结构。
4. 若遇到登录限制，请用户登录；若遇到 CAPTCHA，先征得用户同意。若最终仍无法读取全文，立即停止，报告已完成的只读检查、获取阻塞以及零写入、零提交，不生成文章总结，也不修改知识库。

## 3. 形成证据有界的文章总结

阅读全文后，先在回复中按以下固定顺序输出：

1. 一句话结论；
2. 准确标题、作者或发布方、可获得的发布日期或编辑日期、canonical URL；
3. 围绕 `DuckDB、向量化` 的技术总结；
4. 文章实际给出的架构、数据流、设计决策和定量结论；
5. 分栏标注“文章主张”“推断”“未知项”“独立验证事实”。

文章只能证明作者实际陈述的内容，不能自动证明 DuckDB 当前源码行为、事务或一致性语义、崩溃安全、生产规模或普遍性能。所有性能数据标为“文章报告”或“作者声称”，并保留文章可得的基线、工作负载、数据规模、软件版本、硬件、并发度、缓存状态、指标定义和分位数；缺失条件统一列为未验证。只保留定位证据所需的短摘录，不复制整篇受版权保护的文章。

## 4. 沉淀最小可复用知识

1. 在写入前，按准确标题、canonical URL、`DuckDB`、`向量化`、相关别名和概念搜索 `articles/`、`concepts/`、`index.md`、`concepts/index.md` 及实际目录索引。
2. 若已有同一来源的 source note，则更新它；否则遵循相邻页面结构创建一个 `articles/<topic>.md`。实际路径须在查重和读取相邻命名约定后确定，计划阶段不臆造。
3. 优先更新已有 concept 页面。只有当文章确实提供了现有页面无法自然承载的、可跨来源复用的机制或决策框架时才创建新 concept；若没有持久可复用知识，则明确记录“新建 concept：none”。
4. 为新增或更新页面补齐必要的导航、直接相关页面的反向链接和 canonical URL，避免孤儿页面；遵循相邻页面已有链接和 front matter 风格。
5. source note 明确设置证据边界；来源类型只能按实际材料选择 `official-doc`、`conference-summary` 或 `unverified`。concept 页面可使用 `technical-analysis`，但不能借页面级状态提升单条陈述的证据等级。
6. Codex traceability 只记录当前运行时直接暴露的 `codex_task_id`、`codex_task_title`、`codex_task_share_url`；缺失值写 `unavailable`。不得搜索私有数据库、日志、缓存、隐藏文件或历史任务来补值。
7. 不修改 `feishu/`、`sync/feishu-manifest.json` 或生成的 `graphify-out/`。
8. 真正写入前再次运行 `git status --short --branch`。若此时出现非本任务改动，停止且不覆盖它们。

## 5. 验证并创建一个本地提交

仅在全文获取成功、知识沉淀完成且第二次状态检查仍通过后，在 knowledge-base 根目录执行：

```bash
python3 -B sync/validate_knowledge_base.py
git diff --check
```

逐字报告 validator 的实际输出；静态检查不能被描述为对源码语义、运行时行为、崩溃恢复、故障处理或性能结论的验证。只修复本任务拥有的文件。随后检查精确 diff 和状态，只暂存显式任务路径，绝不运行 `git add .`：

```bash
git status --short
git diff -- <explicit-task-paths>
git add <explicit-task-paths>
git diff --cached --check
git diff --cached --stat
```

确认 index 仅含本任务文件后，创建且只创建一个以 `docs:` 开头的英文 Conventional Commit。最后回读：

```bash
git show --stat --oneline --decorate -1
git status --short --branch
```

不 push，不创建 PR，也不改变仓库可见性。

## 6. 正式执行后的交付顺序

先返回第 3 节的五部分文章总结，再依次报告：source note 是创建还是更新及实际路径；更新和新建的 concepts（包括 `none`）；导航与反向链接变化；每条验证命令及精确结果；knowledge-base 分支与 commit SHA；所有未验证项；最后明确写出“no push or PR was performed.”

当前仅完成计划编制；没有执行仓库或文章操作，因此不存在实际文章总结、文件路径、验证结果、分支、提交 SHA 或独立验证事实。
````

### C2 accepted response (`codex-green-c2-exact.md`)

````text
结论：本场景可以规划继续执行，但当前只输出计划；后续真实执行必须先重新验证 canonical knowledge_base checkout，完整取得文章正文后再做证据有界的总结与最小知识沉淀，最终只创建一个本地提交，不 push、不创建 PR。

输入保持不变：

- `article_url`: `https://mp.weixin.qq.com/s/example-cdc`
- `core_keywords`: `CDC、可靠性`

执行计划：

1. 前置门禁
   - 场景前提是 `/Users/zhangxiahao/Desktop/projects/knowledge_base` 的 canonical checkout 干净且位于 `main`；这只是本计划采用的场景事实，不是本次已经完成的实际检查。
   - 后续真实执行时，在任何文章抓取、浏览器访问或知识库写入之前，重新读取该仓库的 `AGENTS.md`、`README.md`、`index.md` 以及 `articles/`、`concepts/` 的现有索引，并运行 `git status --short --branch`。
   - 若发现任何 staged/unstaged tracked change、非 ignored untracked path，或与本文章任务无关的非默认分支，立即拒绝整个任务；列出阻塞路径，不 stash、clean、restore、切换分支、创建 worktree 或抓取文章。
   - 若 live gate 确认仍是干净的 `main`，创建任务分支 `docs/cdc-reliability`。知识库只使用 canonical checkout，不创建 worktree。

2. 获取完整 canonical 文章
   - 因 URL 属于微信公众号，先调用已安装的 `$wechat-article-to-markdown` 处理同一个 canonical URL：`https://mp.weixin.qq.com/s/example-cdc`。
   - 检查结果是否包含完整正文，而不是仅有标题、元数据、摘要或局部段落。若失败或遗漏大段正文，再用浏览器打开同一个 canonical URL 补全；不以搜索摘要或无关转载替代原文。
   - 若页面要求登录，请用户登录；若遇到 CAPTCHA，先征得用户同意。若最终仍无法完整读取文章，停止，不修改知识库、不提交，也不编造总结。
   - 不安装任何插件；已安装的匹配技能已满足首选路由要求。

3. 形成围绕 `CDC、可靠性` 的证据有界总结
   - 按顺序输出：一句话结论；标题、作者/发布方、可得的发布日期或编辑日期、canonical URL；围绕 `CDC、可靠性` 的技术总结；文章实际给出的架构、数据流、关键决策和定量结论；最后分别列出“文章主张”“推断”“未知项”“独立验证事实”。
   - 只记录文章实际提供的信息。文章未给出的事务边界、投递语义、顺序保证、幂等机制、故障恢复、崩溃安全、生产规模和性能条件均标为 `unverified`，不能从“可靠性”一词反推。
   - 性能或规模数字统一标成“文章报告”或“作者声称”，保留文中可得的基线、工作负载、数据量、版本、硬件、并发、缓存状态、指标定义和分位数；缺失条件逐项列为未验证。
   - “独立验证事实”只收录真实完成的额外验证；若没有，则明确写“无”，不把文章陈述升级为独立事实。

4. 最小化沉淀到知识库
   - 完整读取文章后，按标题、canonical URL、`CDC、可靠性`、别名和相关概念检索 `articles/`、`concepts/`、`index.md`、`concepts/index.md`，判断是否已有同源笔记或可复用概念页。
   - 同一来源已存在时更新现有 source note；否则在 `articles/` 下创建一个符合相邻页面命名和结构的 source note。始终保留 canonical URL：`https://mp.weixin.qq.com/s/example-cdc`。
   - 优先更新已有概念页；只有当原文确实提供可跨来源复用的 CDC/可靠性机制或决策框架，且现有页面无法自然承载时，才新建概念页。若没有足够的耐久知识，明确记录“新建概念：无”。
   - source note 使用仓库支持的 evidence vocabulary；未知的文章元数据和当前运行时未直接暴露的 Codex task ID、title、share URL 写 `unavailable`，不搜索任何私有状态补齐。
   - 更新必要的导航与反向链接，避免孤儿页面；只修改本任务拥有的 source note、concept、反向链接和索引文件，不修改 `feishu/`、`sync/feishu-manifest.json` 或 `graphify-out/`。
   - 写入前再次运行 `git status --short --branch`。若出现非本任务变更，停止且不覆盖。

5. 验证并创建一个本地提交
   - 在 knowledge_base 根目录运行 `python3 -B sync/validate_knowledge_base.py` 和 `git diff --check`，记录原样输出；静态校验不宣称证明运行时行为、故障恢复、崩溃安全或性能。
   - 检查 `git status --short` 和本任务显式路径的 diff；仅以显式路径 `git add`，绝不使用 `git add .`。
   - 运行 `git diff --cached --check` 和 `git diff --cached --stat`，确认暂存区只有本任务文件后，创建一个以 `docs:` 开头的英文 Conventional Commit。
   - 用 `git show --stat --oneline --decorate -1` 和 `git status --short --branch` 回读提交与最终状态。
   - 不 push、不创建 PR，也不改变仓库可见性。

6. 最终交付
   - 先返回第 3 步的五部分文章总结，再依次报告：source note 是创建还是更新及实际路径；更新和新建的 concept（无则写“无”）；导航与反向链接；每条验证命令及其精确结果；分支和 commit SHA；未验证项；明确声明“no push or PR was performed.”
   - 如果 gate 或正文获取失败，只报告已经完成的只读检查、阻塞原因，以及 zero-write/zero-commit，不伪造总结、验证结果或任务标识。

本次计划编制没有执行仓库状态检查、文章获取、knowledge_base 访问或修改、暂存、提交、push 或 PR。
````

### C3 accepted response (`codex-green-c3-exact.md`)

````text
# 执行计划

## 1. 固定输入与本次边界

- `article_url`: `https://example.com/post`
- `core_keywords`: `查询优化、代价模型`
- 这是计划场景，不是实际执行。以下两项只作为题设前提使用，不视为本次已经完成的检查：canonical `knowledge_base` checkout 干净且位于 `main`；当前有可用的官方只读 connector，且其正文可能不完整。
- 本次不访问文章或 `knowledge_base`，不获取正文，不修改文件，不暂存，不提交，不推送，也不创建 PR。后续实际执行必须重新检查实时状态，不能用上述题设替代验证。

## 2. 实际执行时先门禁 canonical checkout

在任何 connector、CLI、浏览器或搜索之前，只使用 `/Users/zhangxiahao/Desktop/projects/knowledge_base`，不创建 knowledge-base worktree：

1. 完整读取该仓库的 `AGENTS.md`、`README.md`、`index.md`，以及 `articles/`、`concepts/` 的现有索引；仓库内 `AGENTS.md` 优先。
2. 运行 `git status --short --branch`，确认实时分支和工作区状态。
3. 若存在任何已暂存或未暂存的 tracked 变更、任何非 ignored 的 untracked 路径，立即拒绝整个任务，列出阻塞路径；不得先获取文章，也不得 stash、clean、删除、移动、restore、提交或以路径不重叠为由继续。
4. 若分支不是 `main`/`master`，且不能证明是同一文章任务的专用分支，也立即停止，不切换分支、不创建分支或 worktree 绕过。
5. 只有实时检查仍确认 checkout 干净且位于 `main`/`master` 时，才计划创建 `docs/query-optimization-cost-model`。该名称由给定关键词归纳，实际创建前仍以仓库约定和实时状态为准。

题设称 checkout 干净且位于 `main`，因此本场景的计划可以继续到采集阶段；这不是对当前真实仓库状态的确认。

## 3. 获取完整 canonical 文章

`https://example.com/post` 属于 “Other platform” 路由。实际执行时：

1. 先调用题设所称的可用官方只读 connector，目标仅限 canonical URL `https://example.com/post`。
2. 检查 connector 返回内容是否包含可识别的标题、作者或发布方、可用的发布日期或编辑日期，以及足以覆盖 `查询优化、代价模型` 的完整正文。不得把元数据、搜索摘要、片段或缺少大量章节的 `ContentText` 当作完整文章。
3. 题设已提示 connector 正文可能不完整；若检查后确实不完整、受阻或缺失重要章节，则打开同一个 canonical URL 进行浏览器补全。
4. 只有原页面仍不可读时，才对同一篇 canonical 文章做聚焦搜索；不得用无关转载或搜索片段替代正文。
5. 若遇到登录，要求用户先登录；若需要处理 CAPTCHA，先征得用户同意。若最终仍无法读到完整文章，立即停止，不生成臆测摘要，不访问或修改知识库，保持零写入、零提交。
6. 不安装插件；题设中的可用 connector 只决定首选采集路由，不证明正文完整。

## 4. 生成证据有界的文章总结

完整正文可读后，按以下顺序形成总结：

1. 一句话结论。
2. 标题、作者或发布方、可用的发布或编辑日期，以及 canonical URL `https://example.com/post`。
3. 围绕 `查询优化、代价模型` 的技术总结。
4. 文章实际给出的架构、数据流、设计决策和定量结论。
5. 分栏标注“文章声称”“推理”“未知项”“独立验证事实”。

证据边界如下：

- 外部文章本身不能证明当前源码行为、事务或一致性语义、崩溃安全、生产规模或普遍性能结论。
- 性能数据必须写成“文章报告”或“作者声称”，并保留正文可得的 baseline、工作负载、数据规模、版本、硬件、并发、缓存状态、指标定义和分位数；缺失条件明确标为 `unverified`。
- 不把关键词扩展成文章没有支持的机制、公式或效果，也不把推理写成事实。

## 5. 沉淀最小可复用知识

在文章完整可读且初步总结完成后：

1. 搜索 `articles/`、`concepts/`、`index.md`、`concepts/index.md` 中的实际文章标题、canonical URL `https://example.com/post`、`查询优化、代价模型`、别名和相关概念。
2. 同一来源已有 source note 时更新该页；否则创建一个符合相邻页面命名和结构的 `articles/<topic>.md`。
3. 优先更新已有 concept。只有正文确实提供了现有页面无法自然承载的可复用机制或决策框架时，才创建 concept；若没有稳定、可迁移的知识，则明确记录 concept 创建为 `none`。
4. 按仓库现有风格更新必要的导航、目录索引和直接相关页面的反向链接，避免孤儿页面。
5. source note 使用正文实际可得的来源元数据；Codex task ID、标题、分享 URL 只使用当前运行时直接暴露的值，缺失项写 `unavailable`，不搜索私有存储、日志、缓存或隐藏运行时文件。
6. 不修改 `feishu/`、`sync/feishu-manifest.json` 或生成的 `graphify-out/`。
7. 写入前再次运行 `git status --short --branch`。若出现非本任务变更，立即停止且不覆盖。

## 6. 校验并创建一个本地提交

仅在上述步骤成功且差异完全属于本任务时，从 knowledge-base 根目录执行：

```bash
python3 -B sync/validate_knowledge_base.py
git diff --check
```

随后检查精确 diff 和状态，只暂存显式任务路径，不使用 `git add .`；再运行：

```bash
git diff --cached --check
git diff --cached --stat
```

确认 index 仅包含本任务文件后，创建一个以 `docs:` 开头的英文 Conventional Commit，并读回：

```bash
git show --stat --oneline --decorate -1
git status --short --branch
```

实际报告必须逐项给出命令及其精确结果，不预填 validator 计数，也不把静态校验解释为源码语义、运行时行为、故障恢复或性能已验证。只创建本地提交，不 push、不创建 PR。

## 7. 实际执行的最终交付格式

成功时，先返回第 4 节规定的五部分文章总结，再依次报告：

1. `articles/` source note 是创建还是更新，以及实际路径；
2. 更新的已有 concepts 和新建的 concepts，均需显式写出，适用时写 `none`；
3. 导航和反向链接变更；
4. 每条校验命令及精确结果；
5. knowledge-base 分支和本地 commit SHA；
6. 未验证项；
7. 明确声明 `no push or PR was performed.`

若 checkout 门禁或完整正文采集失败，只报告实际完成的只读检查、阻塞原因以及零写入、零提交事实；不虚构摘要、校验结果、任务标识或仓库状态。

本计划编写期间没有执行文章采集、knowledge-base 检查或修改、暂存、提交、push、PR。
````

### C4 accepted response (`codex-green-dirty-rerun.md`)

````text
结论：本场景必须在 canonical knowledge_base 的仓库门禁处停止，不能获取文章，也不能写入或提交知识库。已知存在上一任务已暂存的 tracked 文件，本身就是整项任务的阻断条件；即使这些文件与本次预计文件完全不重叠，也不允许继续。

执行计划：

1. 将题目给出的仓库状态作为本次 plan/scenario 的事实，不用当前 live checkout 状态替换它，也不执行现场检查。
2. 报告阻断项：`/Users/zhangxiahao/Desktop/projects/knowledge_base` 含有上一任务已暂存的 tracked 文件。路径不重叠不构成例外。
3. 在文章获取之前终止本次任务：不访问 `https://example.com/post`，不调用文章抓取工具、浏览器、搜索或连接器，不生成关于“HTAP、存储分层”的文章摘要。
4. 保持零知识库写入、零暂存、零提交：不读取、修改、暂存、清理、stash、移动或恢复 knowledge_base 中的文件，不创建分支或 worktree 绕过门禁，也不 push、不创建 PR。
5. 待上一任务的变更由其所有者妥善处理后，再发起一次实际执行。届时必须从头读取 canonical checkout 的仓库说明与索引，并重新执行 live `git status --short --branch`；只有仓库干净且分支满足规则时，才能继续文章获取、证据有界总结、最小知识沉淀、校验和单个本地提交。

范围自检：本回答仅依据题目显式前提给出拒绝计划；未获取 URL，未检查或修改实际 knowledge_base，未执行 stage、commit、push 或 PR，也未把“不重叠”误判为可继续条件。
````

### C5 accepted response (`codex-green-trace.md`)

````text
已完成的只读前置检查表明，知识库 `/Users/zhangxiahao/Desktop/projects/knowledge_base` 当前为干净的 `main` 分支（`git status --short --branch` 的唯一输出为 `## main`）。但本次前向测试禁止获取文章和修改仓库，因此不能读取 `https://example.com/post` 的完整正文，也不能声称文章总结、知识库写入、校验或本地提交已经完成。

若在允许执行完整流程的运行时，且文章已完整取得，来源笔记的 traceability 应只写当前运行时直接暴露的值：

```yaml
traceability:
  source_url: "https://example.com/post"
  source_title: "unavailable"
  source_author_or_publisher: "unavailable"
  source_published_or_edited_at: "unavailable"
  codex_task_id: "unavailable"
  codex_task_title: "unavailable"
  codex_task_share_url: "unavailable"
```

`Agent` 和“执行状态”是阅读重点，不是 Codex task 元数据，不能据此填充 `codex_task_title`，也不能据此推导 task ID 或分享链接。

不会搜索本机私有数据库、日志、缓存、隐藏运行时文件、任务历史、`~/.codex`、环境变量或其他私有存储来寻找 ID、标题或分享链接；也不会编造这些值。当前运行时未直接暴露的三个 Codex 字段均必须写为 `unavailable`。

完整流程的 Git 行为应是：仅在 canonical knowledge-base checkout 干净且位于 `main`/`master` 时，创建 `docs/agent-execution-state` 分支；在文章取得、最小知识写入及静态校验成功后，以显式任务路径暂存，创建一个英文 Conventional Commit（`docs:` 前缀），并读回 commit 与状态。不得创建 knowledge-base worktree，不得使用 `git add .`，不应 stash/clean/绕过脏工作树；不会 push、不会创建 PR、不会改变仓库可见性。本次前向测试未执行上述写入或 Git 变更：零写入、零 commit、零 push、零 PR。

## SELF_CHECK

- [x] 已完整阅读 `SKILL.md` 及其要求的 `references/knowledge-base-conventions.md`。
- [x] 输入齐全：`article_url=https://example.com/post`；`core_keywords=Agent、执行状态`。
- [x] 仅执行了 Skill 要求的知识库只读 gate：读取 `AGENTS.md`、`README.md`、`index.md`、`concepts/index.md` 和 `articles/`/`concepts/` 目录索引；状态为干净 `main`。
- [x] 未查看设计、计划、测试、基线或 WorkBuddy 材料。
- [x] 未获取 URL、未搜索私有 Codex 状态、未读取数据库/日志/缓存/隐藏文件。
- [x] 未创建分支、未写入知识库、未运行校验、未暂存、未提交、未 push、未创建 PR。
- [x] 没有伪造文章内容、来源元数据、Codex task 元数据、校验结果或 commit SHA。
````
