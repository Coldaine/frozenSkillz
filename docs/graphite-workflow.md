# Graphite Stacked PR Workflow Guide

This guide explains how to use the `graphite-stacked-pr-workflow` skill and the Graphite CLI to manage complex stacks of pull requests.

## Overview

Graphite is a tool designed to simplify the development process when working with small, atomic, and stacked pull requests. It allows you to create branches that depend on each other and submit them as a coherent stack to GitHub.

## Getting Started

1.  **Install Graphite CLI:** Follow the instructions at [graphite.dev](https://graphite.dev).
2.  **Authenticate:** Run `gt auth login` to connect your account.
3.  **Initialize Repository:** Run `gt repo init` in your project root.

## Common Workflows

### Creating a New Stack

To start a new stack, create your first branch:

```bash
gt branch create feature-part-1
```

Make your changes, commit them, and then create the next branch in the stack:

```bash
gt branch create feature-part-2
```

### Submitting Your Stack

When you are ready to open pull requests for your entire stack, run:

```bash
gt stack submit
```

This will create or update pull requests for every branch in your current stack.

### Managing Feedback

If you need to make changes to a branch in the middle of a stack, simply checkout that branch, make your changes, and then use Graphite to propagate those changes up the stack:

```bash
gt checkout feature-part-1
# make changes
git commit -am "Address review comments"
gt stack restack
```

### Merging

Once your stack has been reviewed and approved, you can merge it all at once:

```bash
gt pr merge --stack
```

## Best Practices

- **Keep PRs small:** Each PR should ideally represent a single logical change.
- **Stay synced:** Regularly run `gt stack sync` to keep your local branches up to date with the remote and the base branch.
- **Use the Dashboard:** The Graphite dashboard provides a great visual representation of your stacks and their status.
