# README Skill Index Design

## Goal

Update the repository README so users can quickly map each available skill's display name to its Codex invocation command and repository directory.

## Source of Truth

- Discover skills from `skills/*/SKILL.md`.
- Read the invocation command from the frontmatter `name` field and render it as `$<name>`.
- Read the display name from the first level-one heading in each `SKILL.md`.
- Use the actual repository-relative skill directory as the location.

## README Structure

Keep the existing repository title and add a `## 可用 Skills` section containing one Markdown table with these columns:

1. Skill 显示名称
2. Codex 调用命令
3. 所在目录

The table will include every current skill under `skills/`, sorted by directory name. Commands and paths will use inline code formatting.

## Scope

- Modify only `README.md` during implementation.
- Do not change skill metadata or the current directory reorganization.
- Do not add installation commands, prompt-template entries, or detailed skill descriptions.

## Verification

- Compare the table row count and names against all `skills/*/SKILL.md` files.
- Confirm every command matches the corresponding frontmatter `name`.
- Confirm every listed directory exists.
- Run `git diff --check`.
