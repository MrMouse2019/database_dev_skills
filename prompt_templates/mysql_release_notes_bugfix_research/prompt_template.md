# MySQL Release Notes 模块 Bugfix 检索与表格整理任务模板

请你系统检索 MySQL 官方 Release Notes，整理与指定模块或数据类型相关的 Bugfix，并输出为 CSV 和 XLSX 电子表格。

## 一、检索目标

- MySQL 版本范围：`<起始版本>` 及以上，检索至当前最新的 MySQL 8.0.x 版本
- 目标模块：`<模块名称>`
- 检索关键词：
  - `<关键词 1>`
  - `<关键词 2>`
  - `<关键词 3>`
  - `<同义词、函数名、类名、组件名或常见拼写变体>`

示例：

```text
模块：临时表
关键词：
- temporary table
- temp table
- TempTable
- internal temporary table
- temptable
- tmp table
```

或者：

```text
模块：大字段
关键词：
- BLOB
- TEXT
- JSON
- LOB
- long column
- large object
- off-page
- externally stored
```

## 二、官方数据源

以以下官方来源为准：

1. MySQL Release Notes  
   `https://dev.mysql.com/doc/relnotes/mysql/8.0/en/`

2. MySQL 官方 GitHub 源码仓库  
   `https://github.com/mysql/mysql-server`

3. MySQL Bugs 社区  
   `https://bugs.mysql.com/`

社区补充资料可以检索，但优先级如下：

1. MySQL Bugs
2. MySQL 官方 GitHub
3. 阿里云开发者社区
4. 其他有明确复现、分析或补丁说明的技术社区

不要使用 Percona、MariaDB 或其他分支仓库的提交替代 MySQL 官方提交。只有在“补充资料”中可以提及这些分支，不能作为第 3 列的官方 commit。

## 三、筛选口径

### 3.1 收录范围

收录 Release Notes 中与目标模块直接相关的 Bugfix，包括但不限于：

- 正确性问题
- 错误结果
- 数据丢失或结果集不完整
- Server crash、assertion failure
- 内存泄漏或内存异常增长
- 性能退化
- 执行计划错误
- 索引访问异常
- 复制、恢复、DDL、DML 或并发问题
- 错误处理缺失
- 输出格式或元数据错误
- 与目标模块相关的兼容性问题

不要求 Release Note 描述必须精确包含所有关键词。只要问题本质上属于目标模块，就应收录。

例如检索 BLOB/TEXT/JSON 时，还需要识别：

- large column
- packed addon
- external storage
- off-page column
- LOB
- long value
- large row
- JSON function
- JSON_TABLE
- JSON_VALUE
- generated column based on JSON

### 3.2 排除范围

排除以下内容：

- 纯新增功能或 WorkLog 功能发布
- 仅有文档修改、拼写修正
- 仅在测试用例或代码注释中偶然出现关键词
- 问题本身与目标模块无关，只是示例数据使用了该类型
- 没有 Bugfix 含义的行为说明

### 3.3 关联 Bug

一条 Release Note 可能包含多个 Bug 编号，必须全部分析。

除了正文括号中的 Bug，还必须检查条目后面的：

- `References`
- `See also`
- `This issue is a regression of`
- `Related`
- `Duplicate of`
- `Introduced by`
- `Fixed as part of`

例如：

```text
(Bug #36775910)

References: See also: Bug #36341532.
```

应同时记录：

```text
Bug #36775910
Bug #36341532
```

若一条 Release Note 同时关联多个 Bug，不要拆成多行。保持“一条 Release Note 对应表格一行”，在 commit 和社区讨论单元格中分段记录多个 Bug。

## 四、Bug 编号分类规则

MySQL Release Notes 中通常存在两类 Bug 编号。

### 4.1 公开 MySQL Bugs 编号

通常为 5 位或 6 位，例如：

```text
Bug #106621
Bug #117085
```

这类编号通常对应：

```text
https://bugs.mysql.com/bug.php?id=<BUG_ID>
```

公开 Bug 编号及讨论链接放在第 4 列“社区相关讨论”。

格式：

```text
Bug #106621
https://bugs.mysql.com/bug.php?id=106621
```

### 4.2 Oracle/MySQL 内部 Bug 编号

通常为 8 位，例如：

```text
Bug #33917625
Bug #36775910
```

这类编号用于检索 `mysql/mysql-server` 官方 GitHub commit。

内部 Bug 编号及对应提交放在第 3 列“mysql 官方 commit”。

格式：

```text
Bug #33917625
https://github.com/mysql/mysql-server/commit/<commit_sha>
```

### 4.3 缺失处理

- 找不到官方 GitHub commit：第 3 列留空
- 找不到公开 MySQL Bugs 页面：第 4 列留空
- 不要填写“未找到”“未公开”“无结果”等占位文字
- 不要因为找不到 commit 或社区讨论而删除 Release Note 条目

## 五、GitHub Commit 检索规则

在 `mysql/mysql-server` 官方仓库中按以下方式检索：

```text
Bug#<8位编号>
Bug #<8位编号>
BUG#<8位编号>
<Release Note 中的核心错误描述>
<相关类名、函数名、错误信息>
```

例如：

```text
Bug#33917625
Handle buffer full for multi-valued indexes
```

优先选择：

1. 主体修复 commit
2. 明确包含该 Bug 编号的 commit
3. commit message 与 Release Note 根因和修复方案一致的提交
4. MySQL 8.0 分支对应提交

不要优先选择：

- post-push test fix
- merge commit
- revert commit
- 仅修复编译错误的 follow-up commit

如果一个修复由多个必要 commit 组成，可以在同一 Bug 编号下列出多个 commit，但应明确区分主体修复与 follow-up。

格式：

```text
Bug #36189820
主体修复：
https://github.com/mysql/mysql-server/commit/<sha1>

Follow-up：
https://github.com/mysql/mysql-server/commit/<sha2>
```

若同一个 commit 同时修复多个内部 Bug，可以写为：

```text
Bug #32738705, Bug #33501541
https://github.com/mysql/mysql-server/commit/<sha>
```

## 六、社区讨论检索规则

每个公开 Bug 编号都应尝试访问：

```text
https://bugs.mysql.com/bug.php?id=<BUG_ID>
```

优先收录 Release Note 正文或 References 中明确出现的公开 Bug。

如有高质量补充资料，可以继续追加：

```text
Bug #106621
https://bugs.mysql.com/bug.php?id=106621

阿里云开发者社区：
https://developer.aliyun.com/article/xxxx
```

不要把没有在 Release Note 或 References 中出现、仅凭猜测相关的 Bug 混入主记录。若确有必要补充，必须标注为“补充关联”，并说明关联依据。

## 七、输出表格结构

输出 CSV，同时生成一个便于查看的 XLSX 文件。

CSV 列固定为：

1. 版本号
2. 描述
3. mysql 官方 commit
4. 社区相关讨论

### 第 1 列：版本号

格式：

```text
8.0.40
```

### 第 2 列：描述

尽量保留 MySQL Release Note 的完整原文，包括：

- Bugfix 描述
- Bug 编号
- References
- See also
- Regression 信息

不要只做一句话摘要，以免丢失根因、修复方式和关联 Bug。

示例：

```text
When executing an index range scan using IndexRangeScanIterator...

(Bug #36775910)

References: See also: Bug #36341532.
```

### 第 3 列：mysql 官方 commit

只记录 8 位内部 Bug 编号和 `mysql/mysql-server` 官方 commit。

示例：

```text
Bug #36775910
https://github.com/mysql/mysql-server/commit/57b6d0d3d3c6c4ea3d057396b86c0554ec333f79

Bug #36341532
https://github.com/mysql/mysql-server/commit/7a090498b66e204a6ea2304c328cf7e49c09eb81
```

### 第 4 列：社区相关讨论

只记录公开 MySQL Bugs 编号和社区链接。

示例：

```text
Bug #106621
https://bugs.mysql.com/bug.php?id=106621

阿里云开发者社区：
https://developer.aliyun.com/article/1066057
```

## 八、XLSX 格式要求

XLSX 至少包含两个工作表。

### 工作表 1：Bugfixes

- 第一行冻结
- 开启筛选
- 描述、commit、社区讨论自动换行
- 单元格垂直顶端对齐
- 版本号列宽较窄
- 描述列宽最大
- commit 和社区链接列适合显示长 URL
- 一条 Release Note 对应一行

### 工作表 2：映射规则

说明：

- 检索范围
- 关键词
- 收录与排除规则
- 6 位公开 Bug 和 8 位内部 Bug 的区别
- References 的处理方式
- GitHub commit 的筛选标准
- 缺失链接留空规则
- 官方数据源

## 九、质量检查

输出前逐条验证：

1. 是否遗漏 `References`、`See also` 或 regression Bug
2. 第 3 列是否只包含 8 位内部 Bug
3. 第 4 列是否只包含公开 MySQL Bugs 或补充社区资料
4. commit 是否来自 `mysql/mysql-server`
5. commit message 是否与 Release Note 描述一致
6. 是否错误选择了 merge、revert 或 post-push commit
7. 找不到链接的单元格是否为空
8. 是否误收录纯功能新增或无关条目
9. 是否覆盖版本范围内所有 Release Notes
10. CSV 是否使用 UTF-8 BOM，确保 Excel 打开中文不乱码

## 十、最终交付

请输出：

1. 检索结果概述
2. 收录条目数量
3. 覆盖的 MySQL 版本
4. 主要 Bug 类型分布
5. CSV 下载链接
6. XLSX 下载链接
7. 对无法定位官方 commit 或公开讨论的条目做数量统计，但不要在表格单元格中填入占位说明

## 本次任务参数

```text
起始版本：<例如 8.0.28>
结束版本：当前最新 MySQL 8.0.x

模块名称：<例如 临时表>
关键词：
- <temporary table>
- <temp table>
- <TempTable>
- <internal temporary table>
- <temptable>

补充关注对象：
- <temptable_max_ram>
- <temptable_use_mmap>
- <Created_tmp_tables>
- <Created_tmp_disk_tables>
- <TABLE>
- <filesort>
- <materialization>
- <derived table>
- <CTE>
```

---

## 附录：大字段主题参数示例

```text
起始版本：8.0.28
结束版本：当前最新 MySQL 8.0.x

模块名称：大字段与复杂数据类型

核心关键词：
- BLOB
- TEXT
- JSON
- LOB
- large object
- large column
- long value

存储相关关键词：
- off-page
- externally stored
- overflow page
- external field
- lob index
- lob page
- compressed blob
- partial update

执行相关关键词：
- sort buffer
- packed addon
- filesort
- row too large
- temporary table
- hash join
- materialization

JSON 相关关键词：
- JSON_TABLE
- JSON_VALUE
- JSON_EXTRACT
- JSON_SCHEMA_VALID
- MEMBER OF
- multi-valued index
- multi-value index
- multivalued index
- typed array
- Field_typed_array

事务与复制相关关键词：
- row image
- binlog_row_image
- generated column
- replication
- undo
- purge
- rollback
- recovery
```

> 核心原则：一行对应一条 Release Note，纵向管理版本，横向区分内部 Bug/官方提交与公开 Bug/社区讨论，同时完整保留 References 形成的 Bug 关联链。
