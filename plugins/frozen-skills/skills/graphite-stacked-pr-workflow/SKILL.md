---
name: graphite-stacked-pr-workflow
description: "Use when working with Graphite for stacked pull request workflows. Graphite allows developers to create, manage, and merge stacks of PRs that depend on each other. This skill provides rules and workflows for using Graphite effectively."
---

# Graphite Stacked PR Workflow

Use this skill when managing complex stacks of pull requests using Graphite. Graphite simplifies the process of creating small, atomic PRs that are stacked on top of each other.

## Core Rules

- Always use `gt stack submit` to submit a stack of PRs.
- Keep PRs small and focused on a single logical change.
- Use `gt branch create` to start a new branch in a stack.
- Sync your stack with the trunk branch regularly using `gt stack sync`.
- Use `gt pr merge --stack` when you are ready to merge the entire stack.

## Preflight

Before starting work with Graphite, ensure you have the CLI installed and authenticated:

```bash
gt --version
gt auth status
```

## Workflow

1.  **Create a new stack:** `gt branch create <branch-name>`
2.  **Make changes and commit:** `git add . && git commit -m "Your message"`
3.  **Add to the stack:** `gt branch create <next-branch-name>`
4.  **Submit the stack:** `gt stack submit`
5.  **Review and Iterate:** Address feedback on individual PRs in the stack.
6.  **Sync and Rebase:** `gt stack sync` to stay up to date with `master`.
7.  **Merge:** `gt pr merge --stack` when all PRs in the stack are approved.

## Guardrails

- Avoid manual rebasing of branches in a Graphite stack; use `gt` commands instead.
- Ensure each PR in the stack has a clear and descriptive title and body.
- Be mindful of dependencies between PRs in the stack.
