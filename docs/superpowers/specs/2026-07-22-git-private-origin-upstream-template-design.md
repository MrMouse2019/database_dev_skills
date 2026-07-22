# Git Private Origin and Official Upstream Prompt Template Design

## Goal

Add one reusable Chinese prompt template that directs an agent to migrate an existing checkout from an official `origin` to a personal private `origin`, preserve the official repository as `upstream`, configure main-branch tracking deliberately, and verify the resulting Git metadata.

## Location

The template will be the sole user entry point at:

`prompt_templates/git-private-origin-upstream/prompt_template.md`

This follows the repository convention `prompt_templates/<template-name>/prompt_template.md`.

## Inputs

The template accepts:

- local repository path;
- official repository URL;
- personal private repository URL;
- main branch name, defaulting to `main`;
- development branch to push, if any;
- clone mode and optional one-shot HTTP proxy;
- whether remote network verification and push are authorized.

## Workflow

The agent must inspect the checkout before mutation, distinguish common initial remote layouts, preserve the official repository as `upstream`, make the private repository `origin`, and set the main branch to track `upstream/<main-branch>`. It must not alter source files, create commits, push, force-push, delete remotes, or persist a global proxy unless explicitly authorized.

For a repository that has not yet been cloned, the prompt also defines a full-clone default and an optional command-scoped proxy such as `git -c http.proxy={{proxy-url}} clone ...`. Shallow clone is opt-in because it omits history.

For publishing, authentication is checked first. A requested push targets the private `origin`, uses `-u` for the selected development branch, and is verified using remote refs rather than inferred from command intent.

## Failure Handling

- A `.git/config` lock or permission error is reported as a metadata-write failure; the same narrow operation may be retried only through an approved permission path.
- Authentication, network, remote negotiation, and local object-integrity failures are kept distinct.
- Existing unexpected remotes or divergent branch tracking stop destructive rewriting and require an evidence-based adjustment.
- Force-push and remote deletion always require explicit authorization.

## Verification

The final response reports exact commands and results for remote URLs, fetch refspecs, main-branch tracking, current branch, worktree status, and—when authorized—remote reachability or pushed refs. It explicitly lists operations not performed and any remaining unverified state.

## Scope

Only the prompt template is added. No executable Skill, helper script, README index, source-repository mutation, remote push, or Git configuration change is included.
