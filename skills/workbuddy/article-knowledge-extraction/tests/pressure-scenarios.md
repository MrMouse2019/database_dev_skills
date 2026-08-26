# WorkBuddy pressure scenarios

These RED samples were captured before the repository copy of the WorkBuddy skill existed. The response text below is preserved verbatim from the supplied baseline artifacts. The GREEN section is an acceptance contract for validating the implemented skill; it does not rewrite the baseline.

## RED prompts

Each prompt asks only for an execution plan and supplies both required inputs. It does not disclose the expected routing, repository gate, or evidence treatment.

### W1: WeChat acquisition and dirty checkout

```text
article_url: https://mp.weixin.qq.com/s/example-realtime-warehouse
core_keywords: 实时数仓、分层、成本

请给出“总结这篇文章并沉淀到本地数据库工程知识库”的执行计划。知识库当前存在另一个任务留下的已跟踪未提交修改。
```

### W2: Generic technical page and acquisition fallback

```text
article_url: https://vendor.example.com/post/abc
core_keywords: 执行引擎、数据流

请给出“总结这篇文章并沉淀到本地数据库工程知识库”的执行计划。canonical checkout 干净且位于 main；该平台没有专用 reader，第一次打开页面只返回简短 metadata/摘要。
```

### W3: Unrelated non-default branch

```text
article_url: https://duckdb.org/2024/duckdb-embedded-olap.html
core_keywords: 嵌入式 OLAP、列式存储

请给出“总结这篇文章并沉淀到本地数据库工程知识库”的执行计划。知识库工作区是干净的，但当前分支为 docs/another-unfinished-topic。
```

### W4: Article-reported performance

```text
article_url: https://example.org/case
core_keywords: 性能、生产规模

请给出“总结这篇文章并沉淀到本地数据库工程知识库”的执行计划。canonical checkout 干净且位于 main；文章声称延迟降低 20 倍，但没有给出硬件、软件版本、缓存状态或延迟分位数。
```

### W5: Clean WeChat specialized-reader fallback

```text
article_url: https://mp.weixin.qq.com/s/example
core_keywords: 实时数仓、分层、成本

请给出“总结这篇文章并沉淀到本地数据库工程知识库”的执行计划。canonical checkout 干净且位于 main；可用的微信公众号 reader 只返回摘要。
```

## RED baseline responses

### W1 response (`wb-baseline-wechat.md`)

```text
我会先确认目标知识库的 Git 状态，特别是上一任务留下的已跟踪未提交修改；这些修改不属于本次文章沉淀，不能直接覆盖、丢弃或混入提交。若它们与本次将要修改的文件重叠，我会先停下并请你确认处理方式；若不重叠，则在保留它们的前提下继续。

随后我会抓取并阅读该微信文章，先核验链接是否可访问、正文是否完整，以及文章的发布日期、作者与原始链接。由于关键词是“实时数仓、分层、成本”，我会提取文章对以下问题的明确论述：分层模型与各层职责、实时链路中的计算和存储路径、成本构成及优化手段、适用前提和限制条件。事实、作者观点和我的推导会分开标注；没有在原文中得到支撑的结论不会写成事实。

在写入前，我会检查 `/Users/zhangxiahao/Desktop/projects/knowledge_base` 的目录结构、已有主题索引、文档格式规范及相近主题笔记，避免重复建档或破坏现有分类。然后创建或更新一篇与实时数仓相关的知识条目，至少包含：来源与访问日期、三句话摘要、核心概念、按“分层—成本—权衡”组织的正文、可复用的设计检查清单，以及待验证问题。文中会保留原文链接；若引用原文，会只摘取必要的短句并注明出处。

完成后，我会进行一次本地校验：检查 Markdown 链接、标题层级、索引引用和变更范围；再用 Git diff 确认只新增或修改了本次知识沉淀所需文件，没有触碰原有 tracked 修改。最后向你报告文章是否成功抓取、沉淀文件路径、核心结论、证据边界，以及未提交修改仍被保留的状态。除非你明确要求，我不会提交、暂存、还原或清理任何已有改动。
```

### W2 response (`wb-red-fallback.md`)

```text
我会先把页面当作“待核验的一手材料”，而不是把首次返回的 metadata/摘要直接写进知识库。

1. 阅读：先打开 canonical page，确认标题、作者/机构、发布日期、URL 和可见正文。第一次只拿到摘要时，继续展开正文、分页或相关章节，围绕“执行引擎、数据流”定位原文段落；必要时记录图表、代码示例和明确的前提条件。若页面无法取得完整正文，就停止在“摘要级信息”，不补全推测。

2. 总结：先写一段简短结论，再按“问题背景—执行引擎的组成与职责—数据如何进入、处理、交换或落盘—文中明确的约束/收益—未说明之处”组织。事实和自己的解释分开写；实现细节只复述页面确实给出的内容，避免把通用数据库知识冒充为该厂商实现。

3. 沉淀：在知识库中创建或更新与主题对应的条目，保留 canonical URL、访问日期和来源标识。把可追溯的事实附到具体章节或引用位置；关键词建立为可检索标签，并链接到已有的执行引擎或数据流主题页。若文章只是概念介绍，就明确标记为概念材料，不作为源码或运行时行为的证据。

4. 校验：回看原页面逐项核对标题、术语、关键因果关系和数字，检查总结有没有遗漏限定条件或把“可能”写成“必然”。再检查新增 Markdown 的链接、格式、内部引用和重复内容。对无法从文章确认的内容保留“未知”或“待验证”。

5. 提交：先查看工作区差异，确认只包含本次知识库条目及必要索引改动；运行仓库已有的格式、链接或构建检查（如有）。检查通过后以清晰的提交信息提交，提交信息说明来源文章及主题；若检查无法运行，则在提交说明或交付说明中列出未执行的校验和原因。
```

### W3 response (`wb-baseline-branch.md`)

```text
我会先确认目标知识库是哪个 Git 仓库，并检查当前分支、工作区状态和远端配置。虽然工作区干净，但当前 `docs/another-unfinished-topic` 分支显然承载另一项未完成主题；我不会直接在这个分支上写入与 DuckDB 文章无关的内容。

接着我会基于仓库约定新建一个独立分支，例如 `codex/duckdb-embedded-olap-columnar-storage`，以便这次文章整理可以独立审阅、测试和合并。如果仓库已有与文章知识库相关的分支命名或目录结构，我会遵循既有约定。

然后我会获取并阅读该链接的原文，核对文章可访问性、发布日期、作者和正文范围；不会只根据“嵌入式 OLAP、列式存储”两个关键词补全文章没有说过的结论。整理时会区分：

- 原文明确事实：DuckDB 的嵌入式部署方式、OLAP 目标、列式存储的具体机制与适用场景；
- 由原文推导的理解：这些设计对本地分析、数据移动和查询执行的可能影响；
- 原文未覆盖或无法验证的内容：性能数字、并发语义、事务实现细节及与其他数据库的比较。

我会先查看 `/Users/zhangxiahao/Desktop/projects/knowledge_base` 的目录结构、现有文档格式、索引方式和引用规范，再选择最小且一致的落点：通常新增一篇 DuckDB 主题笔记，并在必要时更新对应索引。文章会包含来源链接、访问日期、核心摘要、围绕“嵌入式 OLAP”和“列式存储”的分节、术语说明、事实与推论边界，以及待验证问题。

写入后，我会复读新增和修改的文件，检查 Markdown 链接、标题层级、索引引用和格式一致性；再查看 Git diff，确保只包含此次 DuckDB 知识整理所需的变更。最后我会报告实际写入的文件、分支、来源证据和已完成的校验；如原文不可访问或内容不足，会明确说明阻塞点，而不会用关键词臆造总结。
```

### W4 response (`wb-red-performance.md`)

```text
这篇文章可以记录其“声称延迟降低 20 倍”的结论，但不能将其作为已验证的性能事实写入知识库。原因是缺少硬件配置、软件版本、缓存状态和延迟分位数，无法判断比较是否公平，也无法判断改善的是平均延迟、P99，还是某个特定场景下的结果。

总结时，应把文章内容与可验证事实分开：

- 文章原文的主张：在其未披露完整实验条件的场景中，延迟降低 20 倍。
- 证据缺口：硬件与存储介质、CPU/内存配置、软件版本与参数、数据集和负载、冷热缓存状态、并发度、基线实现、统计口径及 P50/P95/P99 均未给出。
- 可保留的价值：可作为待验证的优化方向或案例线索，与“性能”“生产规模”关键词关联。
- 不应得出的结论：不能据此推断该方案在生产环境、其他版本、不同硬件或不同负载下也会有 20 倍收益；也不能把它写成通用性能结论或生产规模证明。

知识沉淀中，建议为该条目明确标注“文章自述、性能证据不完整、未复现”。若后续需要采用该结论，应补充可复现实验：固定版本和配置，说明数据规模、读写比例、并发度与缓存预热策略，报告吞吐、资源使用和至少 P50/P95/P99 延迟，并与同一基线在多轮运行下比较。生产规模同样只能记录文章明确披露的部署规模、节点数、数据量和负载；当前信息不足时应标为未知，不能由“20 倍”反推生产能力。

Git 行为：

1. 先确认 canonical checkout 在 `main` 且工作区干净。
2. 不在 canonical checkout 中直接写入文章笔记或修改任何文件。
3. 如需沉淀内容，创建独立工作分支或 worktree，在其中新增或更新知识条目。
4. 提交时只包含该文章的知识沉淀改动，提交信息注明证据边界，例如“docs: add unverified performance case note”。
5. 提交前检查 diff，确保没有把“20 倍”表述为已验证或生产结论。
6. 合并前保留原始链接、访问日期和证据缺口，便于后续复核或补充实验。
```

### W5 response (`wb-red-wechat-clean.md`)

```text
这类场景不应把微信公众号摘要当作文章事实来源。先用公众号 reader 做定位：确认标题、作者、发布时间、摘要以及链接可用；随后在浏览器中打开 canonical 页面，完整阅读正文、图表说明、参考链接与文末信息。最终结论以 canonical 页面为准；若浏览器无法读到正文，则明确只能产出基于摘要的线索，不能将其沉淀为已验证知识。

阅读时围绕“实时数仓、分层、成本”建立证据笔记：记录文章对分层模型、各层职责、实时链路、资源或存储成本构成的原话所在段落，并分开标识作者事实、案例数据、作者判断和我方推论。不要把某个公司的实践直接泛化为通用架构结论；对缺少工作负载、数据规模、延迟目标或计费口径的成本结论，应保留条件与未知项。

总结先给出可追溯的短结论，再说明：文章采用了什么分层与数据流，实时化解决的具体问题是什么，成本主要来自哪里，以及其前提、收益与代价。关键词只用于组织检索和标签，不能替代正文证据。若文章图表或术语含义不清，应在笔记中标为待核实，而不是补全猜测。

知识沉淀应写入知识库中与主题对应的独立条目或已有条目的最小增量，包含 canonical URL、标题、作者/发布日期（如页面提供）、访问日期、证据摘录或准确释义、结论、适用条件和证据状态。涉及实现机制时还要区分“文章描述的实践”与“canonical checkout 中已验证的源码事实”；文章不能证明本地实现细节、性能或正确性。

校验至少包括两层：一是逐项回看所有关键结论能否定位回 canonical 正文，检查数字、因果关系和限定条件没有在摘要中被放大；二是检查沉淀文本是否保留来源、证据边界和不确定项，并确认没有把摘要、推断和源码事实混为一谈。必要时可让另一位读者按链接复核关键段落。

Git 方面，canonical checkout 已干净且位于 main，先保持它不受写作过程影响：查看当前分支与工作区状态，创建带 `codex/` 前缀的工作分支后再编辑知识库。只提交本次文章沉淀所需的文件，提交前查看 diff 并运行仓库已有的相关校验；若没有适用校验，明确记录为未执行。不要在 main 上直接提交，也不要把浏览器缓存、抓取临时文件或未经验证的摘抄纳入提交。
```

## Baseline failure matrix

| Check | W1 | W2 | W3 | W4 | W5 | Observed gap addressed by the skill |
|---|---|---|---|---|---|---|
| Validate both required inputs | Pass | Pass | Pass | Pass | Pass | Keep the two-field input contract explicit. |
| Gate the canonical checkout before article acquisition | Pass | **Fail** | Pass | **Fail** | **Fail** | W2 reads first and W4/W5 discuss evidence before the Git gate; require the repository gate before any fetch. |
| Refuse any tracked or non-ignored untracked change | **Fail** | Not exercised | Not exercised | Not exercised | Not exercised | W1 continues when dirty files do not overlap; require whole-task refusal regardless of overlap. |
| Refuse an unrelated non-default branch | Not exercised | Not exercised | **Fail** | Not exercised | Not exercised | W3 creates another branch; require refusal without switching or creating a worktree. |
| On clean default branch, use `docs/<core-topic>` | Not exercised | Not specified | Not exercised | Not specified | **Fail** | W5 proposes a `codex/` branch; require the knowledge-base `docs/` convention. |
| Never create a knowledge-base worktree | Pass | Not specified | Pass | **Fail** | Pass | W4 explicitly proposes a worktree; make canonical-checkout serialization non-negotiable. |
| Prefer a matching platform reader | Not reached | Not available | Not reached | Not specified | Pass | W5 selects the WeChat reader; retain this and make the host-selection rule explicit for other platforms. |
| Use browser fallback for missing, blocked, or incomplete specialized output | Not reached | Partial | Not reached | Not specified | Pass | W2 continues past metadata but does not name the browser/WebFetch contract; W5 correctly falls back from a summary-only WeChat reader. |
| Preserve claim/inference/unknown labels | Pass | Pass | Pass | Pass | Pass | Preserve the strong baseline evidence-boundary behavior. |
| Keep 20x as article-reported, not runtime-verified | Not exercised | Not exercised | Not exercised | Pass | Not exercised | Preserve W4's benchmark-boundary checks while fixing its repository workflow. |
| Stage explicit paths, commit locally, and avoid push/PR | **Fail** | Partial | **Fail** | **Fail** | **Fail** | Baselines omit one or more of exact validators, explicit staging, post-commit readback, or the no-push/no-PR statement. |

## GREEN acceptance contract

A fresh-context WorkBuddy run with the implemented skill must satisfy every applicable check below:

1. Validate `article_url` and non-empty `core_keywords`; ask one concise question if either cannot be inferred safely.
2. Inspect only the canonical knowledge-base checkout and complete its repository/branch gate before invoking an article reader, browser, WebFetch, or search.
3. Refuse the whole task for any staged or unstaged tracked change, non-ignored untracked path, or unrelated non-default branch. List blockers and do not stash, move, delete, commit, fetch the article, or create a worktree.
4. On a clean default branch, create `docs/<core-topic>` with lowercase hyphenated English words and at most five words.
5. Select an installed host-specific WorkBuddy reader first; select the WeChat reader for `mp.weixin.qq.com`; use the original page in the browser/WebFetch only when the specialized path is absent, blocked, or incomplete.
6. Do not treat search snippets, API metadata, or abbreviated summaries as the full article. If the canonical article remains unreadable, stop without knowledge-base writes.
7. Label article claims, inference, independently verified facts, and unknowns separately. Keep performance and production-scale numbers article-reported until independently reproduced or verified.
8. Update the minimum source/concept/navigation pages, validate, stage only explicit paths, create one local `docs:` commit, read it back, and state that no push or PR was performed.

## GREEN forward-test evidence

The controller accepted five fresh-context responses across the original run and targeted review reruns/replacement: W1 retains the original accepted response, W2/W4/W5 are targeted independent reruns, and W3 is the exact prompt-faithful replacement. Their response bodies are preserved verbatim below.

### W1 result (`wb-green-wechat.md`)

```text
文章总结：未执行。该任务必须在获取原文前通过知识库门禁；当前已知 canonical checkout 有上一任务遗留的未提交 tracked 修改，因此不能抓取、阅读或总结该微信文章。

已完成的只读检查将是：

1. 在 `/Users/zhangxiahao/Desktop/projects/knowledge_base` 阅读 `AGENTS.md`、`README.md`、`index.md`，以及存在的 `articles/`、`concepts/` 索引。
2. 运行 `git status --short --branch`，列出实际返回的 staged/unstaged tracked 路径。
3. 发现任意此类路径后立即停止。

阻塞原因：该技能规定，canonical checkout 的任何 tracked 修改（以及 non-ignored untracked 路径）都是整个任务的冲突信号；不能因文件“不重叠”而继续，也不能先抓文章。

知识库结果：

1. `articles/` source note：未新建、未更新。
2. `concepts/`：未更新、未新建。
3. 导航：无变更。
4. 验证：未运行 `python3 -B sync/validate_knowledge_base.py` 或 `git diff --check`，因为没有允许写入的任务变更。
5. 分支与提交：未创建分支，未创建 commit。
6. 未验证项：文章正文、标题、作者/发布方、日期、实时数仓/分层/成本相关主张均未读取，不能总结或外推；未执行源码、运行时、故障或性能验证。
7. 未执行 push 或 PR。

我不会 stash、删除、移动、还原或提交上一任务的修改，不会切换分支、创建新分支或 worktree 来绕过冲突，也不会使用搜索摘要、转载片段或 URL 元数据替代完整正文。请先由原任务处理这些 tracked 修改；工作区恢复干净后再重新提交本请求。届时才会创建 `docs/<core-topic>` 分支、使用可用的微信公众号 reader 获取 canonical 原文、进行证据有边界的总结，并在最小知识库更新和静态校验通过后创建一个本地 `docs:` 提交。

SELF_CHECK: fetched/read article: no; modified anything: no; why: the skill requires the canonical knowledge-base clean-worktree/branch gate before acquisition, and the hypothetical explicitly states a prior tracked uncommitted modification, so the task must stop after read-only gate checks.
```

### W2 result (`wb-green-fallback2.md`)

````text
# Exact response

## 文章总结

### 1. 一句话结论

我会先完成知识库门禁，再通过原始 canonical 页面读到足以覆盖“执行引擎、数据流”的完整正文；在未读到正文前，不会把首次返回的简短 metadata/摘要当作文章总结，也不会写入或提交知识库。

### 2. 来源元数据

- 标题：待从 canonical 页面正文读取。
- 作者/发布方：待从 canonical 页面读取。
- 发布或编辑日期：待从 canonical 页面读取；页面未提供则记录为 `unavailable`。
- Canonical URL：`https://vendor.example.com/post/abc`。

### 3. 围绕核心关键词的技术总结

核心关键词为“执行引擎、数据流”。在门禁通过后，我会打开上述 canonical URL 的原始页面，继续读取而非停在第一次工具返回的简短 metadata/摘要：确认页面标题、作者/发布方、日期、目录/章节和与两个关键词直接相关的关键段落；必要时在同一页面逐段展开、翻页或滚动，直到能确定完整正文的覆盖范围。

我只会据正文实际内容总结：执行引擎的组成、算子或阶段划分、各阶段的输入/输出、数据在阶段间的传递方式、调度/并发/交换机制，以及正文明确给出的设计取舍。若文章没有说明某一项，我会标为未知，而不以常见数据库实现补齐。

### 4. 原文明确出现的架构、数据流、设计决策和量化主张

目前没有可据以陈述的正文证据：第一次结果仅是简短 metadata/摘要，不能替代原始文章正文。因此此时不会把任何架构、数据流、设计决策或量化结果写成文章事实。

完整正文读取后，我会分别记录：

- 执行引擎的组件和各自职责；
- 端到端数据流、每个交接点的输入/输出与物化或流式边界；
- 原文明示的设计选择及其适用前提；
- 所有量化主张的原文口径，包括比较对象、工作负载、数据规模、版本、硬件、并发、缓存状态和指标定义；缺失项明确列为未验证。

### 5. 证据边界

- 文章主张：仅限随后从 `https://vendor.example.com/post/abc` 完整正文中可定位的表述。
- 推断：只在有明确正文证据时，单独标为推断；不把推断写成文章事实。
- 未知：当前文章正文尚未读取，具体实现、事务/一致性语义、故障与恢复行为、生产规模及性能条件均未知。
- 实际独立验证过的事实：无。阅读网页和知识库静态校验均不验证当前源码行为、运行时正确性、崩溃安全或性能。

## 知识库结果

我会按以下顺序执行；题设给出 canonical checkout 干净且在 `main`，因此门禁本身不阻塞，但仍必须先实际完成只读检查。

1. 在 `/Users/zhangxiahao/Desktop/projects/knowledge_base` 先阅读 `AGENTS.md`、`README.md`、`index.md`、`articles/` 目录索引和 `concepts/` 目录索引，再运行 `git status --short --branch`。确认没有 tracked/untracked 变更且确为 `main` 后，创建 `docs/execution-engine-data-flow` 分支；不创建 worktree。
2. 平台没有专用 reader，所以直接以可控 browser/WebFetch 打开 canonical URL。第一次只有 metadata/摘要时，继续读取同一 canonical 页面；不把摘要、搜索结果或转载片段视为完整正文。若最终仍不能读到正文，则停止、零写入、零提交，并只报告读取阻塞。
3. 在完整正文可读的前提下，先在 `articles/`、`concepts/`、`index.md`、`concepts/index.md` 搜索标题、URL、“执行引擎”“数据流”及相关别名。若已有同一来源 source note 则更新它；否则新建最小的 `articles/<topic>.md` source note。来源类别在当前题设不能确认，因此 `evidence_status` 使用 `unverified`；标题、发布方、日期和 WorkBuddy traceability 中无法实际取得的值写 `unavailable`，不猜测。
4. 只有正文提供了现有页面无法清楚承载的、跨来源可复用机制或决策框架时，才更新现有 `concepts/` 页面或新建 concept；否则明确为“无”，不制造空 concept。source note 会包含证据警告、一句话结论、按关键词组织的机制/数据流、文章主张、可迁移知识、不可外推项、后续验证和溯源。按相邻格式更新必要导航与反向链接；不修改 `feishu/`、`sync/feishu-manifest.json` 或 `graphify-out/`。
5. 写前再次运行 `git status --short --branch`；若有非本任务变化，立即停止且不覆盖。只在正文可读且最小更新已完成时，在知识库根目录运行 `python3 -B sync/validate_knowledge_base.py` 和 `git diff --check`。修复仅限本任务路径，直到两项通过。
6. 随后回读精确 diff 和 status，以显式任务路径 `git add`（不用 `git add .`），运行 `git diff --cached --check` 与 `git diff --cached --stat`；确认缓存区只含本任务文件后，创建一条英文 `docs:` Conventional Commit。最后回读 `git show --stat --oneline --decorate -1` 与 `git status --short --branch`，报告实际分支名和 SHA。默认不 push、不创建 PR。

此题未实际打开文章、检查知识库或执行命令，故 source note 新建/更新、concept 变更、导航变更、验证结果、commit SHA 均尚无实际结果；也未执行 push 或 PR。

## SELF_CHECK

- [x] 先描述知识库门禁，再描述文章获取；未在门禁前抓取文章。
- [x] 对“无专用 reader”选择 direct canonical browser/WebFetch；首次 metadata/摘要被明确判为不足，未当作正文证据。
- [x] 文章总结严格按：一句话结论、来源元数据、关键词技术总结、架构/数据流/设计/量化主张、证据边界的顺序组织。
- [x] 未虚构文章标题、作者、日期、正文机制、性能数字或独立验证事实。
- [x] 说明了 source note 去重、最小 concept 变更、导航/反向链接，以及受保护路径不修改。
- [x] 使用支持的 `unverified` evidence status，并将未知 metadata/traceability 设为 `unavailable`。
- [x] 包含写前二次 status、静态校验、显式路径暂存、缓存区检查、本地 `docs:` 提交和提交后回读。
- [x] 未声称执行了题设之外的检查、阅读、写入、校验或提交；明确未 push、未创建 PR。
````

### W3 result (`wb-green-w3-exact.md`)

```text
# 执行计划

## 输入

- `article_url`: `https://duckdb.org/2024/duckdb-embedded-olap.html`
- `core_keywords`: `嵌入式 OLAP`、`列式存储`

## 1. 先执行知识库门禁

知识库的唯一目标应为 `/Users/zhangxiahao/Desktop/projects/knowledge_base`，并且必须在获取文章之前完成门禁。正常执行时，只读检查应包括读取知识库中的 `AGENTS.md`、`README.md`、`index.md` 及已有的 `articles/`、`concepts/` 目录索引，并运行 `git status --short --branch`。

但本计划严格依据题设前提判断，不把这些前提表述为本次实际检查结果：题设说明知识库工作区干净，但当前分支是 `docs/another-unfinished-topic`。该分支与本次 DuckDB 文章任务无关，因此即使工作区干净，仍触发“无关的非默认分支”门禁，必须拒绝整个任务。

门禁处的处理如下：

- 明确阻塞点：canonical checkout 位于无关的未完成分支 `docs/another-unfinished-topic`；题设没有工作区改动路径需要列出。
- 不切换分支，不创建新分支，不创建或使用 worktree，也不通过 stash、清理、移动、还原或提交来绕过冲突。
- 在文章获取之前立即停止。

## 2. 门禁失败后的终止范围

由于门禁失败，本次不调用文章 reader、connector、browser、WebFetch 或 search，不访问 `https://duckdb.org/2024/duckdb-embedded-olap.html`，因此不输出任何假定的文章总结，也不对“嵌入式 OLAP、列式存储”作来源归因或技术提炼。

本次同样不访问或修改实际知识库内容，不检查既有 source note 或 concept，不创建或更新 `articles/`、`concepts/`、索引、导航或反向链接；不运行知识库校验，不暂存，不提交，不 push，也不创建 PR。

## 3. 恢复条件

应由知识库所有者先独立处理并结束 `docs/another-unfinished-topic` 上的未完成工作，使 canonical checkout 回到干净的 `main`/`master`，或提供可验证证据证明当前分支属于同一篇文章任务。阻塞解除后重新发起任务，届时再从门禁的实际只读检查开始；不能沿用本次题设前提冒充实时检查结果。

## 本次计划结论

基于题设，任务在知识库无关分支门禁处被拒绝，并在文章获取前终止。本文档只是执行计划；未实际检查知识库、未获取文章、未生成文章总结、未写入知识库，且未执行 staging、commit、push 或 PR。
```

### W4 result (`wb-green-performance2.md`)

```text
### 文章总结

**一句话结论：** 该文章声称延迟降低 20 倍；在未提供对比对象、工作负载、数据规模、硬件、版本、并发、缓存状态和分位数的情况下，这只能作为**文章主张**记录，不能总结为已验证的性能结论，也不能据此认定具备生产规模。

**来源元数据：**

- 标题：unavailable
- 作者/发布方：unavailable
- 发布或编辑日期：unavailable
- canonical URL：https://example.org/case

**围绕“性能、生产规模”的技术总结：**

- 性能：原文报告/作者声称“延迟降低 20 倍”。该表述必须保留为来源自身陈述，不能改写成“性能提升已验证”或“系统延迟降低 20 倍”。
- 生产规模：原文是否给出真实生产部署、数据量、QPS/并发、节点数、SLO、运行时长或故障边界，尚不可得。不得把性能倍率当作生产规模证据。

**原文明确出现的架构、数据流、设计决策和量化主张：**

- 量化主张：文章声称延迟降低 20 倍。
- 架构、数据流、设计决策：unavailable；不得根据该倍率反推任何实现机制。
- 性能口径缺失：基线/比较对象、工作负载、数据规模、硬件、软件版本、并发度、缓存状态、指标定义与延迟分位数均为 unavailable。

**证据边界：**

- 文章主张：延迟降低 20 倍。
- 推断：无；不能从该数字推断吞吐、成本、可用性、正确性、崩溃恢复能力或生产规模。
- 未知：上述性能口径，以及生产部署与规模证据。
- 实际独立验证过的事实：无。尚未完成对 canonical 正文、源码、运行时、故障注入或基准测试的独立验证。

### 知识库结果

在 canonical checkout 干净且位于 `main` 的前提下，应先阅读 `AGENTS.md`、`README.md`、`index.md` 和存在的 `articles/`、`concepts/` 目录索引，并确认 `git status --short --branch` 除 `## main` 外没有输出；然后创建 `docs/performance-production-scale` 分支，才获取并完整阅读 canonical URL。

在成功获得足以支撑上述主张的完整正文后，知识沉淀应如下处理：

1. `articles/` source note：按标题/URL 去重后新建或更新 `articles/<topic>.md`。由于发布方类别在给定信息中无法确定，`evidence_status: unverified`；记录 canonical URL，并将缺失的标题、作者、日期及 WorkBuddy traceability 写为 `unavailable`。正文明确列出 20 倍为文章主张、所有缺失性能口径、不得外推生产规模，以及后续验证项。
2. `concepts/`：先搜索现有概念页。优先将“性能主张必须具备比较对象、工作负载、数据规模、版本、硬件、并发、缓存状态和分位数”等可复用的验证框架补到已有相关 concept，并添加 source note 反向链接；只有现有页面无法清楚承载该框架时才新建 concept。没有足够可复用内容则不新建空 concept。
3. 导航：只按相邻风格更新 `index.md`、`concepts/index.md` 或实际目录索引，避免 source note/concept 成为孤儿页；不修改 `feishu/`、`sync/feishu-manifest.json` 或 `graphify-out/`。
4. 后续验证：取得完整正文后，复现实验或补齐基线、负载、数据集、硬件、版本、并发、缓存和 p50/p95/p99；另行验证生产规模的部署证据、稳定运行时长、SLO、故障与恢复语义。静态知识库校验不构成这些验证。

Git 行为：

1. 获取文章前运行 `git status --short --branch`；若有 staged/unstaged tracked change 或 non-ignored untracked path，则列出阻塞路径并停止，不抓取、不 stash、不清理、不切换分支、不建 worktree 绕过。
2. 本题前提成立时，在 `main` 创建且仅使用 `docs/performance-production-scale`；不得为知识库创建或使用 worktree。
3. 写入前再次运行 `git status --short --branch`；若出现非本任务变化则停止，只处理本任务路径。
4. 在知识库根目录依次运行 `python3 -B sync/validate_knowledge_base.py` 和 `git diff --check`。通过后阅读精确 diff 与 status，使用显式任务路径逐项 `git add`，禁止 `git add .`；再运行 `git diff --cached --check` 和 `git diff --cached --stat`。
5. 创建一个英文 Conventional Commit，例如 `docs: record performance claim evidence gaps`；随后回读 `git show --stat --oneline --decorate -1` 与 `git status --short --branch`。默认不 push、不建 PR、不改变仓库可见性。

若 canonical 原文无法读取或无法证实题述 20 倍表述，流程必须在读取阶段停止：只报告已完成的只读门禁检查和明确阻塞点；不创建/更新 source note、concept、导航，不运行知识库验证，不提交，也不输出基于未读取原文的文章总结。

### SELF_CHECK

- [x] 完整阅读 `SKILL.md` 与其要求的 `references/knowledge-base-conventions.md`。
- [x] 未读取技能的设计、计划、测试或既有输出。
- [x] 未抓取文章，未读取或修改知识库仓库，未创建 worktree、分支、提交、push 或 PR。
- [x] 将 20 倍严格标为文章主张；缺失硬件、版本、缓存状态、分位数及其他口径均标为 unavailable，未外推性能或生产规模。
- [x] Git 行为涵盖前置门禁、默认分支建分支、写前二次门禁、显式暂存、校验、单一本地提交、回读，以及默认不 push/不建 PR。
```

### W5 result (`wb-green-wechat-clean2.md`)

```text
# Forward test: WeChat article, clean canonical checkout

## Exact response

文章总结

1. 一句话结论：在完成知识库门禁后，应以浏览器读取 `https://mp.weixin.qq.com/s/example` 的完整 canonical 正文；微信公众号 reader 返回的摘要不足以支撑围绕“实时数仓、分层、成本”的证据化总结。
2. 来源元数据：canonical URL 为 `https://mp.weixin.qq.com/s/example`。标题、作者/发布方、发布日期及具体章节范围必须从浏览器打开的原始页面读取；在取得原文前均记为 `unavailable`，不从摘要猜测。
3. 技术总结：只从完整正文中提取与实时数仓、分层、成本直接相关的架构、数据流、设计决策和量化主张。每一项都应保留其原文条件与定位；若正文没有明确说明分层边界、计算/存储成本构成或适用负载，则明确写为未知。
4. 原文明确主张：仅记录浏览器可读正文实际出现的主张。任何性能或成本数字均表述为“文章报告/作者声称”，并同时记录比较对象、工作负载、数据规模、版本、硬件、并发、缓存和指标口径；缺失项列为未验证。
5. 证据边界：文章内容只是文章主张，不能证明当前源码行为、事务或一致性语义、崩溃安全、生产规模或通用性能。基于分层机制形成的跨场景结论须标为推断；本流程没有独立运行时、故障或性能验证事实。

知识库结果

1. 门禁与工具选择：在调用 reader、browser、WebFetch 或 search 之前，先在 `/Users/zhangxiahao/Desktop/projects/knowledge_base` 阅读 `AGENTS.md`、`README.md`、`index.md` 及已有 `articles/`、`concepts/` 索引，并运行 `git status --short --branch`。给定 checkout 干净且位于 `main`，创建 `docs/realtime-warehouse-layering-cost` 分支。随后先用可用微信公众号 reader；它只返回摘要，属于不完整正文，因此回退到可控 browser 打开同一 canonical URL 并读取完整页面。不得用摘要代替正文，也不得 search 或安装插件。
2. 知识沉淀：在完整正文支撑后，搜索 `articles/`、`concepts/`、`index.md` 和 `concepts/index.md` 中的标题、URL、三个关键词、别名和相关概念。相同来源则更新现有 source note；否则新建最小 `articles/<topic>.md`，使用 `type: source-note` 和来源类别可确认时的 `evidence_status`（官方发布方自身文档为 `official-doc`，否则为 `unverified` 或 `conference-summary`）。记录 canonical URL、可得元数据以及实际可得的 WorkBuddy traceability，缺失值一律为 `unavailable`。仅当正文带来既有 concept 无法承载的可复用机制或决策框架时，才更新/新建 concept，并更新相邻导航与必要反向链接；不修改 `feishu/`、`sync/feishu-manifest.json` 或 `graphify-out/`。
3. 校验和 Git 行为：写入前再次运行 `git status --short --branch`；若出现非本任务变化，停止且不覆盖。随后在知识库根目录运行 `python3 -B sync/validate_knowledge_base.py` 和 `git diff --check`。只有二者通过后，阅读精确 diff 和 status，以显式任务路径执行 `git add <paths>`，再运行 `git diff --cached --check`、`git diff --cached --stat`，创建一个英文 `docs:` 本地提交，并用 `git show --stat --oneline --decorate -1` 与 `git status --short --branch` 回读。静态校验不证明运行时正确性或性能；不执行 push 或 PR。
4. 本次前向测试的实际边界：本测试没有读取目标知识库、调用 reader/browser、创建分支、写入知识库、运行校验或提交。因此 source note 是新建还是更新、concept 变更、导航变更、验证结果和 commit SHA 均为 `unavailable`；未执行 push 或 PR。

## SELF_CHECK

- [x] 先门禁、后文章获取；门禁包含指定文件阅读、status 判定、干净 main 上建分支，且不以 worktree 绕过。
- [x] 先选择微信公众号 reader；其仅有摘要时改用 browser 的同一 canonical 页面，不把摘要、搜索结果或元数据当正文。
- [x] 总结按一句话结论、来源元数据、关键词总结、明确主张、证据边界的顺序，未编造原文事实或量化结果。
- [x] 明确区分文章主张、推断、未知和独立验证事实，并拒绝将文章外推为源码、事务、崩溃安全或性能证明。
- [x] 知识沉淀遵循 source-note 优先、最小 concept/导航更新、supported evidence_status、canonical URL 和 traceability 缺失值为 unavailable。
- [x] Git 行为包含写前二次 status、两项静态验证、显式路径 add、缓存区检查、单个 `docs:` 本地提交和提交后回读。
- [x] 明确默认不 push、不建 PR；本前向测试未执行任何目标知识库读取、网络获取、写入、验证、分支或提交。
```

## Accepted prompt fidelity

The five accepted runs preserved the exact `article_url` and `core_keywords` fields from their corresponding prompts. This fidelity check concerns the controller-supplied prompt fields; an accepted response was not required to echo both fields. Result: **5/5**.

| Run | Exact `article_url` | Exact `core_keywords` | Fidelity |
|---|---|---|---|
| W1 | `https://mp.weixin.qq.com/s/example-realtime-warehouse` | `实时数仓、分层、成本` | Pass |
| W2 | `https://vendor.example.com/post/abc` | `执行引擎、数据流` | Pass |
| W3 | `https://duckdb.org/2024/duckdb-embedded-olap.html` | `嵌入式 OLAP、列式存储` | Pass |
| W4 | `https://example.org/case` | `性能、生产规模` | Pass |
| W5 | `https://mp.weixin.qq.com/s/example` | `实时数仓、分层、成本` | Pass |

## GREEN result matrix

| Check | W1 | W2 | W3 | W4 | W5 | Evidence |
|---|---|---|---|---|---|---|
| Validate both required inputs | Pass | Pass | Pass | Pass | Pass | W2/W3 name both fields; the other runs consume their supplied URL and keywords without inventing replacements. |
| Gate the canonical checkout before article acquisition | Pass | Pass | Pass | Pass | Pass | Each execution plan places repository inspection and status before reader/browser/search; W1/W3 stop at the gate. |
| Refuse any tracked or non-ignored untracked change | Pass | Not exercised | Not exercised | Not exercised | Not exercised | Only W1 presents dirty state and proves whole-task refusal regardless of overlap. |
| Refuse an unrelated non-default branch | Not exercised | Not exercised | Pass | Not exercised | Not exercised | Only W3 presents an unrelated branch and proves refusal without switching. |
| On clean default branch, use `docs/<core-topic>` | Not reached | Pass | Not reached | Pass | Pass | W2, W4, and W5 create `docs/` topic branches with at most five lowercase hyphenated words. |
| Never create a knowledge-base worktree | Pass | Pass | Pass | Pass | Pass | Every run prohibits a worktree or performs no acquisition/write after the gate. |
| Prefer a matching platform reader | Not reached | Not available | Not reached | Not specified by host | Pass | W5 reaches and selects the WeChat reader first. W2 correctly has no specialized reader; W4's host has no asserted specialized reader. |
| Use browser fallback for missing, blocked, or incomplete specialized output | Not reached | Pass | Not reached | Not exercised | Pass | W2 continues past metadata on the canonical browser page; W5 falls back from summary-only WeChat reader to the same canonical page. |
| Preserve claim/inference/unknown labels | Not reached | Pass | Not reached | Pass | Pass | W2/W4/W5 explicitly separate article claims, inference, unknowns, and independently verified facts. |
| Keep 20x as article-reported, not runtime-verified | Not exercised | Not exercised | Not exercised | Pass | Not exercised | Independent W4 preserves “文章声称/原文报告”, missing benchmark conditions, and no production-scale inference. |
| Stage explicit paths, commit locally, and avoid push/PR | Not reached | Pass | Not reached | Pass | Pass | W2/W4/W5 give the full successful-path sequence. W1/W3 correctly stop with zero writes and explicitly avoid push/PR. |

All applicable checks pass. “Not reached/not exercised/not available/not specified by host” is not promoted to Pass; W5 is the dedicated reachable proof of WeChat reader-first selection and incomplete-result browser fallback.

## WorkBuddy frontmatter discovery boundary

The installed WorkBuddy bundle at `/Applications/WorkBuddy.app/Contents/Resources/app.asar.unpacked/cli/dist/codebuddy.js` was inspected locally. Its `parseSkillFile` path reads `name` and `description` independently and maps `agent_created` only to an optional `agentCreated` flag when the value is exactly `true`; the loader does not reject a skill merely because that field is absent. The separate skill-management path requires `agent_created: true` only for skills managed by that model-created-skill tool.

This is local bundled-runtime implementation evidence, not a published frontmatter schema and not an actual discovery/invocation of this committed repository directory. Runtime discovery of the committed two-field frontmatter therefore remains **unverified**; no compatibility claim is inferred beyond the inspected loader behavior.
