---
name: pr-review-dashboard
description: Generate a unified PR review dashboard with multiple visualization modes - visual summary, architecture diagram, flow chart, and curated code review. One HTML page with buttons to switch between views. Use when reviewing PRs to understand changes at multiple levels of detail.
---

# PR Review Dashboard

A unified, multi-view PR review page. One URL, multiple lenses on the same changes.

## The Four Views

| View | Icon | Purpose | When to Use |
|------|------|---------|-------------|
| **Summary** | 📊 | Infographic dashboard with metrics, risk, file distribution | First glance - "what am I looking at?" |
| **Architecture** | 🏗️ | Component diagram showing structural changes | Understanding system impact |
| **Flow** | 🌊 | Data/control flow showing behavioral changes | Understanding logic changes |
| **Changes** | 📝 | Curated code review with annotations | Deep dive into specific files |

## Quick Workflow

1. **Fetch PR data** - Get metadata, files, patches via `gh api`
2. **Analyze and curate** - Classify files, identify core vs mechanical, detect patterns
3. **Generate views** - Create SVG summary, Mermaid diagrams, annotated diffs
4. **Assemble** - Inject all views into the single-page template
5. **Serve** - One HTML file, four view modes via button navigation

## Curation Philosophy

**Show the story, not the data dump.**

- **Summary view:** Always generate - immediate context
- **Architecture view:** Skip if < 5 files or only config/docs
- **Flow view:** Generate if behavioral keywords detected
- **Changes view:** Max 5 core files annotated; bucket rest as mechanical

## Detailed Specifications

| Document | Purpose |
|----------|---------|
| [references/view-specs.md](references/view-specs.md) | Detailed specs for all 4 views (SVG layout, Mermaid syntax, HTML structure) |
| [references/assembly.md](references/assembly.md) | Step-by-step assembly process, data model, injection points |
| [assets/template.html](assets/template.html) | HTML shell with view switcher and CSS |
| [assets/renderer.js](assets/renderer.js) | View switching logic and Mermaid integration |

## Example Output

User runs skill on PR #18 and gets a dashboard with:

- **Summary:** Risk MEDIUM, 43 files, type REFACTOR, docs/ 35%, scripts/ 7%
- **Architecture:** Boxes for new playbook, cleanup script, deleted artifacts
- **Flow:** 5-step corpus review workflow with detect/ledger highlighted
- **Changes:** 3 annotated cards (playbook, cleanup script, doc mismatch note) + collapsed mechanical changes

All in one page. User clicks buttons to switch views instantly.

## Progressive Disclosure

This skill uses three-level loading:

1. **SKILL.md** (this file) - Workflow and concepts (~100 lines)
2. **references/** - Detailed specs when implementing (~500+ lines)
3. **assets/** - Template and scripts (loaded at assembly, not into context)

Read reference files only when building the skill, not for understanding it.
