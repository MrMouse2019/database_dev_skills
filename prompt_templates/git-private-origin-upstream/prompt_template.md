# 开源仓库迁移到个人私有仓库提示词模板

请你帮助我把一个开源代码仓库完整下载到本地，保留官方仓库作为后续同步源，并将代码上传到我的个人私有仓库，用于个人学习和代码分析。请直接执行已获授权的操作，不要只给出命令；如果我只要求命令，则输出可直接复制执行的命令。

## 输入

- 官方开源仓库：`{{official-repository-url}}`
- 个人私有仓库：`{{private-repository-url}}`
- 本地目标目录：`{{local-destination}}`
- 官方主分支：`{{main-branch；默认 main}}`
- 要上传的本地分支：`{{push-branch；默认当前分支}}`
- 本地代理：`{{proxy-url；默认 http://127.0.0.1:7877}}`
- 是否执行上传：`{{push-authorized；yes/no，默认 no}}`
- 是否验证远端：`{{remote-verification-authorized；yes/no，默认 yes}}`

## 目标 remote 布局

- `origin`：个人私有仓库，承载个人分支和个人学习成果。
- `upstream`：官方开源仓库，作为主分支同步源。
- 本地主分支跟踪 `upstream/{{main-branch}}`，个人开发分支按需跟踪 `origin/<branch>`。

## 强制边界

- 修改前检查仓库、remote、分支跟踪、工作区、克隆深度和认证状态。
- 默认完整克隆并保留官方提交历史；只有我明确要求或接受历史缺失时才使用 `--depth 1`。
- 代理必须是单条命令作用域，不要修改全局 `http.proxy`、`https.proxy` 或 SSH 配置。
- `http.proxy` 仅作用于 HTTP/HTTPS remote，不能加速 `git@github.com:...` SSH remote。
- 不修改源码，不删除未知 remote，不重写已发布历史，不 force-push，不持久化凭据。
- 未明确授权上传时，只完成 clone、remote 迁移和本地验证，不执行 push。
- 保留仓库许可证、版权和署名文件；如果项目存在可能影响私有镜像或再分发的限制，明确指出，不自行删除相关文件。

## 阶段一：加速下载官方仓库

1. 检查目标目录是否已经存在。若存在，不得覆盖；先判断它是可复用的完整 checkout、未完成克隆，还是无关目录。
2. 检查官方 URL 使用 HTTPS 还是 SSH，并根据协议选择代理命令。
3. 默认优先使用 HTTPS 进行完整克隆：

```bash
git -c http.proxy={{proxy-url}} clone {{official-repository-url}} {{local-destination}}
```

4. 如果官方 URL 必须使用 SSH，则使用命令级 SSH CONNECT 代理；先确认本机 `nc` 支持 `-X connect -x`：

```bash
git -c core.sshCommand='ssh -o ProxyCommand="nc -X connect -x {{proxy-host-port}} %h %p"' clone {{official-repository-url}} {{local-destination}}
```

其中 `{{proxy-host-port}}` 形如 `127.0.0.1:7877`，不能包含 `http://`。

5. 若代理不可用，报告原始错误，并给出不带代理的回退命令；不要永久修改全局代理。
6. 克隆后核验：

```bash
git -C {{local-destination}} rev-parse --is-inside-work-tree
git -C {{local-destination}} rev-parse --is-shallow-repository
git -C {{local-destination}} remote -v
git -C {{local-destination}} branch --show-current
git -C {{local-destination}} status --short --branch
```

## 阶段二：迁移 remote

在 `{{local-destination}}` 中执行，先检查：

```bash
git remote -v
git branch -vv
git status --short --branch
git config --get-regexp '^(remote\.|branch\.)'
```

根据现状做最小修改：

### 情况 A：只有官方 `origin`，且没有 `upstream`

```bash
git remote rename origin upstream
git remote add origin {{private-repository-url}}
```

### 情况 B：官方仓库已经是 `upstream`

如果 `origin` 不存在：

```bash
git remote add origin {{private-repository-url}}
```

如果 `origin` 已存在且确认应替换：

```bash
git remote set-url origin {{private-repository-url}}
```

### 情况 C：现有 remote 与预期不一致

不要直接删除或覆盖。列出实际 URL、fetch refspec 和分支跟踪关系，说明冲突后再做精确调整。

将本地主分支设置为跟踪官方主分支；如果远端跟踪引用尚不存在，先在获得网络访问授权后 fetch：

```bash
git fetch upstream {{main-branch}}
git branch --set-upstream-to=upstream/{{main-branch}} {{main-branch}}
```

remote 迁移后必须核验：

```bash
git remote -v
git config --get-regexp '^(remote\.(origin|upstream)\.(url|fetch)|branch\.{{main-branch}}\.(remote|merge))$'
git branch -vv
git status --short --branch
```

如果遇到 `could not lock config file .git/config`，将其识别为 Git 元数据写权限问题。确认前序命令没有产生部分修改，再通过获准的权限路径重试同一组精确命令，不要扩大写入范围。

## 阶段三：加速上传到个人私有仓库

仅当 `{{push-authorized}}` 为 `yes` 时执行。

1. 上传前检查认证和目标：

```bash
gh auth status -h github.com
git remote get-url origin
git branch --show-current
git status --short --branch
```

认证失败时，给出准确的 `gh auth login -h github.com` 或 `gh auth refresh -h github.com` 命令并等待我完成授权。不要保存或输出访问令牌。

2. 如果 `origin` 是 HTTPS URL，使用 HTTP 代理加速：

```bash
git -c http.proxy={{proxy-url}} push -u origin {{push-branch}}
```

3. 如果 `origin` 是 SSH URL，`http.proxy` 无效；使用命令级 SSH CONNECT 代理：

```bash
git -c core.sshCommand='ssh -o ProxyCommand="nc -X connect -x {{proxy-host-port}} %h %p"' push -u origin {{push-branch}}
```

4. 如果要首次上传完整官方主分支，必须明确确认目标分支和远端是否为空，再执行：

```bash
git -c http.proxy={{proxy-url}} push -u origin {{main-branch}}
```

SSH remote 则改用上面的 `core.sshCommand` 形式。不得因为普通 push 失败而自动改用 `--force`、`--mirror` 或 `--all`。

5. 区分并报告认证失败、网络失败、代理失败、远端拒绝、对象协商失败和本地对象损坏；不要把它们统称为“GitHub 不可用”。

## 上传后验证

若 `{{remote-verification-authorized}}` 为 `yes`，使用与 remote 协议相匹配的命令级代理验证远端分支：

```bash
git -c http.proxy={{proxy-url}} ls-remote --heads origin {{push-branch}}
```

SSH remote：

```bash
git -c core.sshCommand='ssh -o ProxyCommand="nc -X connect -x {{proxy-host-port}} %h %p"' ls-remote --heads origin {{push-branch}}
```

同时重新执行：

```bash
git remote -v
git branch -vv
git status --short --branch
```

只有 `push` 成功且 `ls-remote` 返回预期分支及提交时，才能声明上传成功。

## 最终输出

请先给结论，再报告：

1. clone 是否完成、是否完整历史、实际使用的代理方式；
2. `origin` 和 `upstream` 的最终 fetch/push URL；
3. 主分支及开发分支的跟踪关系；
4. push 是否执行、推送的精确分支和远端核验结果；
5. 工作区是否干净；
6. 未执行的高风险操作；
7. 仍未验证的状态、原始错误和下一条可执行命令。

不要仅复述计划，也不要在缺少命令输出时声称 clone、remote 迁移或 push 已成功。

