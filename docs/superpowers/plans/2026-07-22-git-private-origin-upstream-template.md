# Git Private Origin and Official Upstream Template Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a reusable prompt template covering accelerated clone, remote migration, and accelerated verified push from an official open-source repository to a personal private repository.

**Architecture:** Use one standalone Chinese Markdown prompt with explicit inputs, protocol-aware proxy commands, three ordered workflow stages, safety gates, failure classification, and evidence-based verification. Keep the template independent of executable skills or scripts.

**Tech Stack:** Markdown, Git CLI, GitHub CLI, command-scoped HTTP proxy, command-scoped SSH `ProxyCommand`.

## Global Constraints

- Create only `prompt_templates/git-private-origin-upstream/prompt_template.md` plus this plan document.
- Preserve the official repository as `upstream` and use the personal private repository as `origin`.
- Default to a full clone; shallow clone is opt-in.
- Never persist global proxy configuration.
- Use `http.proxy` only for HTTPS remotes; use command-scoped SSH `ProxyCommand` for SSH remotes.
- Push only with explicit authorization and verify with `ls-remote` before claiming success.
- Do not push this repository or create a pull request.

---

### Task 1: Add the end-to-end prompt template

**Files:**
- Create: `prompt_templates/git-private-origin-upstream/prompt_template.md`

**Interfaces:**
- Consumes: official URL, private URL, destination, main branch, push branch, proxy, push authorization, and remote-verification authorization.
- Produces: an executable agent workflow and exact direct/proxied Git commands.

- [ ] **Step 1: Install the approved template body**

Create the template from the approved design, with separate clone, remote migration, and push phases.

- [ ] **Step 2: Verify required workflow contracts**

Run fixed-string checks for `git clone`, `git remote rename origin upstream`, HTTPS push proxy, SSH push proxy, authentication, `ls-remote`, full-clone default, and no global proxy changes.

- [ ] **Step 3: Verify repository formatting and scope**

Run `git diff --check`, inspect `git diff --stat`, and confirm no unrelated files changed.

- [ ] **Step 4: Commit the template and plan**

Commit with `feat(prompt_templates): add private origin workflow` after all checks pass.
