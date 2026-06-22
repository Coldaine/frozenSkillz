---
name: setup-rules
description: >
  Helps set up universal rule templates in your project's .claude/rules/ directory.
  Explains each rule template and guides you through customizing them for your project.
version: 1.0.0
tags:
  - rules
  - standards
  - configuration
---

# Setup Rules Skill

This skill helps you install and customize universal rule templates from the frozen-rules plugin.

## What This Skill Does

The frozen-rules plugin includes three universal rule templates:

1. **ansible-playbooks.md** — Standards for Ansible playbook headers, secrets, and usage
2. **documentation-frontmatter.md** — Frontmatter requirements for documentation files
3. **submodule-workflow.md** — Git submodule workflow rules

These are **templates** that need to be copied to your project's `.claude/rules/` directory.

## How to Use This Skill

When invoked, this skill will:

1. **List available rule templates** from this plugin's `rules/` directory
2. **Explain each rule** — what it enforces and when to use it
3. **Guide you through customization** — path patterns, project-specific requirements
4. **Help you install** — copy templates to `.claude/rules/` with appropriate modifications

## Installation Steps

### Step 1: Create the rules directory (if it doesn't exist)

```bash
mkdir -p .claude/rules
```

### Step 2: Copy rule templates

The rule files are located in this plugin at:
```
${CLAUDE_PLUGIN_ROOT}/rules/ansible-playbooks.md
${CLAUDE_PLUGIN_ROOT}/rules/documentation-frontmatter.md
${CLAUDE_PLUGIN_ROOT}/rules/submodule-workflow.md
```

Copy them to your project:
```bash
cp ${CLAUDE_PLUGIN_ROOT}/rules/*.md .claude/rules/
```

### Step 3: Customize path patterns

Each rule has a frontmatter `paths:` section. Edit it to match your project structure.

**Example** (ansible-playbooks.md):
```yaml
---
paths:
  - "ansible/**/*.yml"  # Adjust if your Ansible files are elsewhere
---
```

## Rule Descriptions

### ansible-playbooks.md
- **Enforces**: Playbook header format, no hardcoded secrets, manual execution
- **Use when**: You have Ansible playbooks in your repo
- **Customize**: Update `paths:` to match where your playbooks live

### documentation-frontmatter.md
- **Enforces**: Frontmatter requirements for docs (title, created, updated, tags)
- **Use when**: You have structured documentation in `docs/`
- **Customize**: Adjust required fields and path patterns

### submodule-workflow.md
- **Enforces**: Never modify submodule contents, update via upstream, verify before committing
- **Use when**: Your repo uses git submodules
- **Customize**: Update paths to match your submodule locations

## After Installation

Rules are **automatically active** once in `.claude/rules/`. Claude Code will enforce them when the `paths:` pattern matches.

To verify rules are loaded:
```bash
claude rules list   # (if such a command exists)
```

Or check `.claude/rules/` directory.

## Need Help?

Ask the agent to:
- "Explain the ansible-playbooks rule"
- "Show me how to customize documentation-frontmatter for my project"
- "Install the submodule-workflow rule"
