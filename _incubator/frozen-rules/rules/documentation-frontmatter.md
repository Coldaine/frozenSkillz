---
paths:
  - "docs/**/*.md"
---

# Documentation Frontmatter Standards

All markdown files under `docs/` **MUST** have YAML frontmatter.

## Required Fields

```yaml
---
last_edited: YYYY-MM-DD
editor: Claude Code (Claude Opus 4.6)  # or "human", or other tool name
user: <username>
status: draft | ready | complete | deprecated
version: X.Y.Z  # Semver
subsystem: <project-specific>  # Define per project
tags: [keyword1, keyword2]
doc_type: reference | plan | guide | architecture | adr | research | playbook
---
```

## Rules

- **NEVER create a doc under `docs/` without frontmatter** — every file needs at least the required fields above.
- **ALWAYS update `last_edited`** when modifying a document.
- **ALWAYS update `editor`** to reflect who/what made the change.
- **ALWAYS bump `version`** on substantive changes (patch for fixes, minor for new sections, major for rewrites).
- **Use `status: deprecated`** instead of deleting documents. Add a `supersedes:` or `superseded_by:` field.

## Project Customization

Each project should define its own:
- **`subsystem` values** — the domains within that project
- **Exempt files** — files that do NOT require frontmatter (typically CLAUDE.md, GEMINI.md, README.md, TODO.md, OPENCODE.md, AGENTS.md)
- **Additional fields** — project-specific frontmatter fields beyond the base set

Override this rule in your project's `.claude/rules/` to add project-specific values.
