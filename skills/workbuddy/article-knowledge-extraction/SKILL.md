---
name: article-knowledge-extraction
description: 当用户提供微信公众号、技术博客、官方文档或会议整理稿的文章链接与核心关键词，并要求总结文章、提炼可复用数据库工程知识或沉淀到本地 knowledge_base 时使用。
---

# Article Knowledge Extraction

## Overview

围绕 `core_keywords` 阅读 `article_url`，先输出证据有边界的文章总结，再把最少且可复用的知识写入 `/Users/zhangxiahao/Desktop/projects/knowledge_base`。知识库只通过 canonical checkout 串行修改；静态校验通过后创建本地提交。默认不 push、不建 PR。

执行前完整阅读 [knowledge-base-conventions.md](references/knowledge-base-conventions.md)。仓库内 `AGENTS.md` 是最终约束。

## Required inputs

只接受两个必需输入：

- `article_url`：用户给出的 canonical article URL；
- `core_keywords`：一个或多个阅读焦点。

若任一输入缺失且无法无风险推断，在抓取或写入前只问一个简短问题。不要用搜索结果猜 URL，不要自行扩展关键词含义。

## Workflow

严格按以下顺序执行。

### 1. Gate the canonical checkout before acquisition

知识库的唯一目标是：

```text
/Users/zhangxiahao/Desktop/projects/knowledge_base
```

不得为知识库创建或使用 worktree。共享 canonical checkout 是并发任务的串行化信号。

在调用任何文章 reader、connector、browser、WebFetch 或 search **之前**：

1. 在 canonical checkout 阅读 `AGENTS.md`、`README.md`、`index.md`，以及存在的 `articles/`、`concepts/` 目录索引。
2. 运行 `git status --short --branch`。
3. 若存在任意 staged/unstaged tracked change 或 non-ignored untracked path，拒绝整个任务。列出阻塞路径；不得继续抓文章，也不得 stash、删除、移动、还原或提交这些文件。
4. ignored 文件不构成阻塞；不要把 ignored `.workbuddy/` 内容误报为工作区改动。
5. 若当前是非 `main`/`master` 分支，仅当分支明确属于同一篇文章任务时继续；若分支无关或无法确认，拒绝整个任务。不得切离未完成分支，也不得用新分支或 worktree 绕过冲突。
6. 若工作区干净且位于 `main`/`master`，创建 `docs/<core-topic>` 分支；`core-topic` 使用最多五个小写英文单词，以短横线连接。

门禁失败时，到此结束并报告阻塞原因。不要输出基于未读取原文的文章总结。

### 2. Acquire the complete canonical article

按 URL host 选择获取路径：

1. 先使用已安装且匹配该平台的 WorkBuddy skill、connector 或官方 CLI。
2. `mp.weixin.qq.com` 链接先用可用的微信公众号文章 reader。
3. 专用 reader 不存在、被阻断或返回内容不完整时，才用可控 browser 或 WebFetch 打开原始 canonical URL。
4. 原始页面无法读取时，只可定向搜索同一篇 canonical article；搜索摘要、API 元数据和转载片段不能自动视为完整正文。

检查标题、作者/发布方、可用日期、章节范围和关键段落是否足以支撑关键词总结。若登录阻断，要求用户登录；出现 CAPTCHA，先询问用户；正文仍不可读时停止，不修改知识库。不要为了获取文章安装插件，除非用户另行明确要求。

### 3. Build the evidence-bounded summary

只写原文实际提供的内容，并按下列顺序形成用户可读总结：

1. 一句话结论；
2. 来源元数据：标题、作者/发布方、可用的发布或编辑日期、canonical URL；
3. 围绕 `core_keywords` 的技术总结；
4. 原文明确出现的架构、数据流、设计决策和量化主张；
5. 证据边界：分别标记文章主张、推断、未知和实际独立验证过的事实。

外部文章不证明当前源码行为、事务/一致性语义、崩溃安全、生产规模或通用性能。性能数字必须写成“文章报告/作者声称”，附原文可得的比较对象、工作负载、数据规模、版本、硬件、并发、缓存和指标口径；缺项列入未验证，不得外推。

### 4. Inspect existing knowledge

在 `articles/`、`concepts/`、`index.md` 和 `concepts/index.md` 中搜索标题、canonical URL、关键词、别名和相关概念：

- 同一来源已存在时更新现有 source note，不重复建页；
- 优先更新能承载该知识的现有 concept；
- 仅当文章提供了现有页面无法清楚承载的可复用机制或决策框架时创建 concept；
- 没有可复用概念时不创建空 concept，source note 已满足知识保存。

### 5. Make the minimum knowledge-base update

创建或更新 `articles/<topic>.md`：

- `type: source-note`；
- `evidence_status` 只能从仓库支持的词汇中选择：发布方自己的权威文档用 `official-doc`，会议/案例整理或复述用 `conference-summary`，无法确定来源类别用 `unverified`；
- 保存 canonical URL、可得来源元数据和 WorkBuddy traceability；不可得值写 `unavailable`，不得猜测；
- 正文包含证据警告、一句话结论、关键词分析、文章主张、可迁移知识、不可直接外推内容、后续验证和相关概念。

对每个确有必要的 concept 更新：

- 保留现有结构和术语；
- 添加 source note、原文 URL 和反向链接；
- 区分通用机制、设计建议、文章主张、推断和未知；
- 涉及时，补充正确性/失败语义问题和性能验证缺口。

按相邻条目风格更新 `index.md`、`concepts/index.md` 或实际目录索引，保证新页面不是孤儿页。不得修改 `feishu/`、`sync/feishu-manifest.json` 或生成的 `graphify-out/`。

写入前再次运行 `git status --short --branch`。若出现非本任务变化，停止且不覆盖；只处理本任务创建或修改的路径。

### 6. Validate and create one local commit

在知识库根目录运行：

```bash
python3 -B sync/validate_knowledge_base.py
git diff --check
```

失败时只修复本任务路径，重新执行验证；通过前不得提交。随后：

1. 阅读精确 diff 和 `git status --short`；
2. 用显式路径逐项 `git add`，禁止 `git add .`；
3. 运行 `git diff --cached --check` 并检查 `git diff --cached --stat`；
4. 用英文 Conventional Commit message 创建一个 `docs:` 本地提交；
5. 运行 `git show --stat --oneline --decorate -1` 与 `git status --short --branch` 回读。

静态校验只证明知识库结构、链接和文本检查结果，不证明数据库运行时正确性或性能。未经单独授权，不 push、不建 PR、不改变仓库可见性。

## Final response contract

先给出“文章总结”，严格使用步骤 3 的五部分顺序；再给出“知识库结果”，严格包含：

1. `articles/` source note 是新建还是更新；
2. 更新了哪些现有 `concepts/` 页面、新建了哪些 concept（若无则明确为无）；
3. 导航变更；
4. 验证命令及精确结果；
5. 知识库分支和 commit SHA；
6. 未验证项，以及“未执行 push 或 PR”。

若任务在门禁或文章读取阶段停止，报告已完成的只读检查和明确阻塞点，不声称已经总结、验证或提交。

## Red flags

- “脏文件不重叠，所以可以继续”
- “切新分支/建 worktree 就能绕过未完成任务”
- “先抓文章，之后再检查知识库”
- “搜索摘要足以代替正文”
- “文章报告 20 倍，所以性能提升已验证”
- “为了方便使用 `git add .`”
- “本地提交后顺便 push 或生成 PR”

出现任一想法时停止并回到对应门禁或证据规则。
