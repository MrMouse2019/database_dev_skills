# knowledge_base conventions for WorkBuddy

在执行 `article-knowledge-extraction` 时完整阅读本文件。知识库内的 `AGENTS.md` 优先于本参考。

## Repository and serialization

- 唯一目标 checkout：`/Users/zhangxiahao/Desktop/projects/knowledge_base`。
- `articles/` 保存外部文章/会议材料的 source note，只证明来源自身的陈述。
- `concepts/` 保存跨来源可复用的机制、权衡和验证问题。
- `index.md`、`concepts/index.md` 及目录内实际索引是导航入口。
- `sync/validate_knowledge_base.py` 是静态校验器。
- 禁止为知识库创建 worktree。canonical checkout 的 tracked change、non-ignored untracked path 和 unrelated non-default branch 都是全任务冲突信号。

在文章获取前读取仓库说明和索引，并运行：

```bash
git status --short --branch
```

`##` 行仅表示分支；其余 staged/unstaged tracked 状态和 `??` non-ignored untracked 状态都必须拒绝。Git 已忽略的文件不会出现在普通 status 输出中，不构成阻塞。拒绝后列出阻塞路径，不 stash、清理、移动、还原、提交或绕过。

干净的 `main`/`master` 使用 `docs/<core-topic>`，其中 topic 最多五个小写英文单词并以短横线连接。非默认分支必须明确属于同一 article task；无关或不确定都停止。

## Evidence vocabulary

只使用知识库支持的 `evidence_status`：

| Value | Use |
|---|---|
| `source-fact` | 固定版本源码中直接可定位的事实 |
| `official-doc` | 权威发布方对自身系统/产品的官方文档 |
| `paper-claim` | 论文作者的陈述或实验结果 |
| `user-confirmed` | 用户明确确认但本任务未独立验证的信息 |
| `inference` | 基于已列证据的推断 |
| `unverified` | 来源类别或结论无法建立 |
| `source-index` | 来源索引页 |
| `conference-summary` | 会议、案例或第三方整理/复述 |
| `technical-analysis` | 综合来源形成的机制或设计分析 |
| `runtime-verified` | 已报告具体运行验证范围和结果的事实 |

source note 的选择规则：权威发布方自己的文档用 `official-doc`；会议/案例整理或复述用 `conference-summary`；不能确定来源类别用 `unverified`。concept 通常用 `technical-analysis`，但其正文仍要逐项标记来源边界。

不要使用未被仓库支持的状态。页面级 status 不能把页面内所有陈述自动升级为同一证据等级。

## Source-note frontmatter

保留相邻页面的字段顺序和格式。新建 source note 至少包含：

```yaml
---
title: "文章标题"
domain: database-architecture
type: source-note
status: draft
code_version: "not-applicable"
last_verified: null
tags:
  - keyword
sources:
  - "发布方、可得日期、canonical URL"
traceability:
  source_url: "https://canonical.example/article"
  workbuddy_session: "unavailable"
  workbuddy_conversation_id: "unavailable"
  workbuddy_conversation_title: "unavailable"
related:
  - "concepts/example.md"
evidence_status: unverified
updated_at: YYYY-MM-DD
---
```

正文结构：

1. `> [!warning] 证据边界`；
2. 一句话结论；
3. 来源、背景与规模口径；
4. 按 `core_keywords` 组织的机制、架构和数据流；
5. 文章主张与量化口径；
6. 可迁移知识；
7. 不可直接外推内容；
8. 后续验证；
9. 相关概念和溯源。

保持必要的短摘录和定位信息，不复制整篇受版权保护的文章。

## Concept frontmatter and content

优先沿用现有 concept 的结构。新建 concept 至少包含：

```yaml
---
title: "概念标题"
domain: database-architecture
type: concept
status: draft
code_version: "not-applicable"
last_verified: null
tags:
  - keyword
sources:
  - "articles/source-note.md"
  - "发布方与 canonical URL"
traceability:
  source_url: "https://canonical.example/article"
  workbuddy_session: "unavailable"
  workbuddy_conversation_id: "unavailable"
  workbuddy_conversation_title: "unavailable"
related:
  - "concepts/related.md"
evidence_status: technical-analysis
updated_at: YYYY-MM-DD
---
```

正文应说明结论、通用机制、适用条件、设计权衡、正确性与失败语义问题、性能验证问题、不可直接接受的来源口径、来源和边界。新 concept 必须加入导航；直接相关的现有页面按仓库风格添加反向链接。

没有足够可复用知识时不要创建 concept。不要为了固定数量创建空页面。

## WorkBuddy traceability

始终记录 canonical `source_url`。仅记录当前 WorkBuddy 会话实际可得的 ID、标题和分享 URL；任何缺失或有多个候选的值都写 `unavailable`，不得推测。

- `workbuddy_session`：用户在任务卡片“分享任务”后产生的分享 URL；未生成即为 `unavailable`。
- `workbuddy_conversation_id`：若当前运行时直接暴露则使用；否则可按既有本地约定，用工作目录和会话开始时间在 `~/.workbuddy/app/sessions.json` 中定位，并用相同时间点日志交叉检查。候选不唯一时停止追溯并写 `unavailable`。
- `workbuddy_conversation_title`：已有 conversation ID 时，可从 WorkBuddy 本地 metadata 取得；查不到写 `unavailable`。不要伪造一个便于搜索的标题。

不得把 WorkBuddy 本地数据库、会话文件、日志、凭证或 token 提交到知识库。概念页从 source note 复制同一组 traceability 值，保证独立回溯。

回溯旧页面时，先用页面中的 UUID 校验会话，再用已记录标题或标题关键词在 WorkBuddy 任务列表搜索。搜索框只匹配任务标题，不用 UUID、页面标题或原文 URL 搜索。若本地 metadata 已不存在，按已记录标题、日期和工作空间人工定位；找不到就保留 `unavailable`。

## Links and protected paths

- 使用仓库相邻页面采用的相对 Markdown 链接或 Obsidian 双链风格。
- source note 和 concept 都显式写 canonical URL。
- 新页面加入 `index.md` 和实际目录索引，避免孤儿页。
- 只修改本任务需要的 source、concept、reverse-link 和 navigation 路径。
- 不修改 `feishu/`、`sync/feishu-manifest.json` 或生成的 `graphify-out/`。

## Validation and local commit

从知识库根目录运行：

```bash
python3 -B sync/validate_knowledge_base.py
git diff --check
```

记录 validator 的完整实际摘要，不预填 `concepts=N` 等变化值。静态校验不构成源码版本语义、数据库运行时、崩溃恢复、故障注入或基准性能证明。

提交前：

```bash
git status --short
git diff -- <explicit-task-paths>
git add <explicit-task-paths>
git diff --cached --check
git diff --cached --stat
```

禁止 `git add .`。缓存区只能包含本任务文件。用英文 `docs:` Conventional Commit message 创建一个本地提交。提交后回读：

```bash
git show --stat --oneline --decorate -1
git status --short --branch
```

默认不 push、不创建 PR、不生成隐含已经发布的陈述。只有用户另行明确授权时才执行发布动作。

## Final report

按顺序报告：

1. source note 新建/更新及实际路径；
2. 更新的现有 concepts 和新建 concepts（可为无）；
3. navigation/reverse-link 变化；
4. 每条验证命令及精确结果；
5. 分支名和 commit SHA；
6. 文章主张、推断、未知、独立验证事实的边界；
7. 未运行的源码/运行时/故障/性能验证；
8. 明确声明未 push、未创建 PR。

若拒绝或读取失败，只报告已经执行的只读检查、阻塞状态和零写入事实。
