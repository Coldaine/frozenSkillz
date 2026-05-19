---
name: pr-visual-summary
description: Generate an infographic-style visual summary of a GitHub PR as a single SVG image. Creates a dashboard-style overview showing scope, risk, change types, and key metrics at a glance. Use when the user wants a "visual PR summary", "PR infographic", "PR dashboard", "PR at a glance", or to understand PR characteristics without reading code.
---

# PR Visual Summary

Generate an infographic-style visual summary of a GitHub PR as a single SVG image.

## Goal

One image that summarizes the entire PR for immediate pattern recognition — like a dashboard card or health monitor.

## Workflow

1. **Fetch PR data** — Get metadata, files, and patch statistics via `gh api`
2. **Analyze and score** — Calculate metrics, risk factors, and classifications
3. **Generate SVG** — Create the visual infographic using the specification below
4. **Save and serve** — Write to file and provide viewing instructions

## Step 1: Fetch PR Data

```bash
# PR metadata
gh api repos/{owner}/{repo}/pulls/{number}

# Files with stats
gh api repos/{owner}/{repo}/pulls/{number}/files --paginate

# Commit count
gh api repos/{owner}/{repo}/pulls/{number}/commits --paginate
```

## Step 2: Analysis & Scoring

### Core Metrics to Calculate

| Metric | How to Calculate |
|--------|------------------|
| **Total Changes** | Sum of additions + deletions |
| **Change Ratio** | Additions / (Additions + Deletions) — 0.5 = balanced |
| **File Count** | Total files changed |
| **Commit Count** | Number of commits |
| **Review Comments** | Count of review threads |
| **Files by Extension** | Group files by type |
| **Test Coverage** | % of files that are test files (*/test*, *.spec.*, etc.) |

### Risk Scoring Algorithm

```
BASE_RISK = 0

# Size factors
if total_lines > 1000: BASE_RISK += 2
if file_count > 20: BASE_RISK += 2
if file_count > 50: BASE_RISK += 3

# Complexity factors
if config_files_changed: BASE_RISK += 2
if migration_files: BASE_RISK += 3
if test_coverage < 20%: BASE_RISK += 2
if has_binary_changes: BASE_RISK += 1

# Review factors
if days_since_last_activity > 7: BASE_RISK += 1
if unresolved_threads > 0: BASE_RISK += 2

RISK_LEVEL:
  0-2  → LOW    (Green)
  3-5  → MEDIUM (Yellow)
  6-8  → HIGH   (Orange)
  9+   → CRITICAL (Red)
```

### PR Type Classification

| Type | Detection Rules |
|------|-----------------|
| **Security** | Branch contains "security", "vuln", "cve", "dependabot", or files match `*security*` |
| **Bugfix** | Title contains "fix", "bug", "hotfix", or branch matches `fix/*`, `hotfix/*` |
| **Feature** | Title contains "feat", "add", "implement", or branch matches `feat/*`, `feature/*` |
| **Refactor** | Title contains "refactor", "clean", "restructure", or branch matches `refactor/*` |
| **Deps** | Only `package*.json`, `requirements*.txt`, `Cargo.lock`, `go.mod`, `yarn.lock`, `Gemfile.lock`, `poetry.lock` changed |
| **Docs** | Only `*.md`, `*.rst`, `docs/*` changed |
| **Tests** | Only test files changed |
| **CI/CD** | Only `.github/`, `.circleci/`, `Jenkinsfile`, `Dockerfile` changed |

## Step 3: SVG Visual Specification

### Canvas Layout

```
┌─────────────────────────────────────────────────────────┐
│  [ICON]  PR Title (truncated)              [TYPE_BADGE] │
│  #1234 by @author  •  opened 3 days ago                │
├─────────────────────────────────────────────────────────┤
│  ╔═══════════════╗  ╔═══════════════╗  ╔═════════════╗ │
│  ║  RISK SCORE   ║  ║  SIZE GAUGE   ║  ║ CHANGE TYPE ║ │
│  ║   [DONUT]     ║  ║  [SEMICIRCLE] ║  ║  [ICONS]    ║ │
│  ║   MEDIUM      ║  ║    847 LOC    ║  ║  +420/-227  ║ │
│  ╚═══════════════╝  ╚═══════════════╝  ╚═════════════╝ │
├─────────────────────────────────────────────────────────┤
│  FILE TREEMAP (by extension)                            │
│  ┌────────┬────┬──────────┬─────┬──────────┐           │
│  │  .py   │.ts │   .md    │.yml │   .lock  │           │
│  │  45%   │30% │   15%    │ 5%  │    5%    │           │
│  └────────┴────┴──────────┴─────┴──────────┘           │
├─────────────────────────────────────────────────────────┤
│  TOP DIRECTORIES AFFECTED                               │
│  src/        ████████████████████████████████  12 files │
│  tests/      ██████████████                    5 files  │
│  docs/       ██████                            2 files  │
├─────────────────────────────────────────────────────────┤
│  STATUS BADGES                                          │
│  [TESTS:PASS] [CI:RUNNING] [2 REVIEWS] [3 COMMENTS]    │
└─────────────────────────────────────────────────────────┘
        Dimensions: 800 x 500 px
```

### Color System

```css
/* Background */
--bg-primary: #1a1a2e;      /* Dark navy */
--bg-secondary: #16213e;    /* Slightly lighter navy */
--bg-card: #0f3460;         /* Card backgrounds */

/* Risk Colors */
--risk-low: #4ade80;        /* Green */
--risk-medium: #fbbf24;     /* Yellow/Amber */
--risk-high: #fb923c;       /* Orange */
--risk-critical: #ef4444;   /* Red */

/* Change Type Colors */
--addition: #22c55e;        /* Green */
--deletion: #ef4444;        /* Red */
--neutral: #64748b;         /* Slate */

/* Type Badge Colors */
--type-security: #dc2626;   /* Red - urgent */
--type-feature: #3b82f6;    /* Blue - new */
--type-bugfix: #22c55e;     /* Green - fix */
--type-refactor: #a855f7;   /* Purple - cleanup */
--type-deps: #f59e0b;       /* Amber - dependencies */
--type-docs: #64748b;       /* Gray - documentation */
--type-tests: #14b8a6;      /* Teal - testing */
--type-ci: #6366f1;         /* Indigo - automation */

/* Text */
--text-primary: #e2e8f0;
--text-secondary: #94a3b8;
--text-muted: #64748b;
```

### Component Specifications

#### 1. Risk Score Donut

```
    ╭──────────╮
   ╱   ╭──╮   ╲
  │   ╱ 45 ╲   │     ← Percentage in center
  │  │ RISK  │  │     ← Risk level label
  │   ╲    ╱   │
   ╲   ╰──╯   ╱
    ╰──────────╯

Size: 140x140 px
Stroke width: 12px
Background arc: #334155
Fill arc: Risk color (green/yellow/orange/red)
Animation: None (static SVG)
```

#### 2. Size Gauge (Semicircle)

```
         ╭─────────╮
       ╱    847     ╲
      │     LOC      │    ← Total lines in center
       ╲            ╱
        ╰──────────╯
        ████████████        ← Fill shows relative size
        XS  S  M  L  XL     ← Tick marks

Size: 160x80 px
Range: XS (<100) → S (<500) → M (<1000) → L (<5000) → XL (5000+)
Fill color: Gradient based on size
```

#### 3. Change Type Indicator

```
┌─────────────────┐
│  📊 CHANGES     │
├─────────────────┤
│  [▲] +420 lines │
│  [▼] -227 lines │
│  ─────────────  │
│  58% additions  │
└─────────────────┘

Visual: Stacked horizontal bars showing add/del ratio
Icon style: Unicode or inline SVG path
```

#### 4. File Treemap

```
┌────────────────────────────────────────┐
│            FILE DISTRIBUTION           │
├────────────────────────────────────────┤
│  ┌────────────────┐                    │
│  │                │  ┌────────┐         │
│  │      .py       │  │  .ts   │┌─────┐  │
│  │      45%       │  │  30%   ││.md  │  │
│  │   12 files     │  │8 files ││ 15% │  │
│  │                │  │        ││4 fil│  │
│  │                │  └────────┘└─────┘  │
│  └────────────────┘         ┌──────────┐│
│                             │ .yml  5% ││
│                             │ 1 file   ││
│                             └──────────┘│
└────────────────────────────────────────┘

Layout: Squarified treemap algorithm (simplified)
Color: Gradient by file type (warm = code, cool = config)
Labels: Only if box > 40x30 px
```

#### 5. Directory Impact Bars

```
Top Directories Changed:

src/api/        ████████████████████████████████  8 files
src/utils/      ████████████████████            5 files
tests/          ████████████                    3 files
.github/        ████                            1 file

Bar style: Horizontal with rounded ends
Bar color: #3b82f6 (blue) fading by depth
Max bars: 6 (show top by file count)
```

#### 6. Type Badge (Top Right)

```
┌─────────────────┐
│  🔒  SECURITY   │  ← Red background, shield icon
└─────────────────┘

┌─────────────────┐
│  ✨  FEATURE    │  ← Blue background, sparkles icon
└─────────────────┘

┌─────────────────┐
│  🐛  BUGFIX     │  ← Green background, bug icon
└─────────────────┘

┌─────────────────┐
│  ♻️  REFACTOR   │  ← Purple background, recycle icon
└─────────────────┘

┌─────────────────┐
│  📦  DEPS       │  ← Amber background, package icon
└─────────────────┘

┌─────────────────┐
│  📝  DOCS       │  ← Gray background, document icon
└─────────────────┘

Size: Auto-width, 32px height
Corner radius: 16px (pill shape)
Icon: Unicode emoji or inline SVG
```

### Icon Reference

| Type | Unicode | SVG Path (alternative) |
|------|---------|------------------------|
| Security | 🔒 | Shield with checkmark |
| Feature | ✨ | Sparkles/stars |
| Bugfix | 🐛 | Bug/insect |
| Refactor | ♻️ | Circular arrows |
| Deps | 📦 | Package box |
| Docs | 📝 | Document |
| Tests | 🧪 | Test tube |
| CI/CD | ⚙️ | Gear |
| Addition | ▲ | Up triangle |
| Deletion | ▼ | Down triangle |
| File | 📄 | Document |
| Directory | 📁 | Folder |
| Commit | ⬡ | Hexagon |
| Comment | 💬 | Speech bubble |

## Step 4: SVG Generation

### Template Structure

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500" viewBox="0 0 800 500">
  <defs>
    <!-- Gradients -->
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#1a1a2e"/>
      <stop offset="100%" style="stop-color:#16213e"/>
    </linearGradient>
    <!-- Filters for glow effects -->
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <!-- Background -->
  <rect width="800" height="500" fill="url(#bgGradient)" rx="12"/>
  
  <!-- Header -->
  <g id="header">
    <!-- Title, author, type badge -->
  </g>
  
  <!-- Metrics Cards -->
  <g id="metrics">
    <!-- Risk donut, Size gauge, Change bars -->
  </g>
  
  <!-- Treemap -->
  <g id="treemap">
    <!-- File distribution rectangles -->
  </g>
  
  <!-- Directory Bars -->
  <g id="directories">
    <!-- Horizontal bar chart -->
  </g>
  
  <!-- Status Badges -->
  <g id="status">
    <!-- Review status, CI status, etc. -->
  </g>
</svg>
```

### Donut Chart Math

```python
def donut_path(cx, cy, radius, start_angle, end_angle):
    """Generate SVG path for donut segment"""
    x1 = cx + radius * cos(start_angle)
    y1 = cy + radius * sin(start_angle)
    x2 = cx + radius * cos(end_angle)
    y2 = cy + radius * sin(end_angle)
    
    large_arc = 1 if end_angle - start_angle > pi else 0
    
    return f"M {x1} {y1} A {radius} {radius} 0 {large_arc} 1 {x2} {y2}"

# For a 75% risk score (270 degrees)
risk_angle = 2 * pi * 0.75 - pi/2  # Start from top
```

## Output Format

Save the generated SVG to a temporary location:

```bash
# Generate filename
OUTPUT="/tmp/pr-visual-{owner}-{repo}-{pr_number}.svg"

# After saving, provide viewing options:
echo "Visual summary saved to: $OUTPUT"
echo "Open with: file://$OUTPUT"
```

## Example Usage

**User:** "Create a visual summary for PR #123 in my-org/my-repo"

**Process:**
1. Fetch PR #123 data via `gh api`
2. Calculate metrics and risk score
3. Classify as "Feature" or "Bugfix"
4. Generate SVG following the visual spec above
5. Save and provide path

## Edge Cases

| Case | Handling |
|------|----------|
| Empty PR (no files) | Show "No changes" placeholder, minimal risk |
| Deleted files only | Red-tinted treemap, deletion-focused bars |
| Renamed only | Special "Rename" type badge, low risk |
| Draft PR | "DRAFT" overlay banner, muted colors |
| Very old PR | Add "⚠️ Stale" warning badge |
| Conflicts | Red "CONFLICTS" alert box |
| Large PR (>100 files) | Show "+47 more" in treemap, truncated list |

## Complete ASCII Mockup

```
┌──────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│   📄 Add user authentication flow                         🔒 SECURITY   │
│   #4521 by @alice • opened 2 days ago                                   │
│                                                                          │
│   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────┐  │
│   │    ╭──────╮     │  │       ╭───╮     │  │      📊 CHANGES         │  │
│   │   ╱   75   ╲    │  │     ╱  1.2k ╲   │  │  ┌───────────────────┐  │  │
│   │  │   RISK   │   │  │    │   LOC    │  │  │  ▲ +892 additions │  │  │
│   │  │  MEDIUM  │   │  │     ╲       ╱   │  │  │  ▼ -324 deletions │  │  │
│   │   ╲        ╱    │  │       ╰───╯     │  │  └───────────────────┘  │  │
│   │    ╰──────╯     │  │    ████████░░   │  │  ████████████░░░░░░░░   │  │
│   └─────────────────┘  └─────────────────┘  └─────────────────────────┘  │
│                                                                          │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │                    FILE DISTRIBUTION                            │   │
│   │  ┌──────────────┬────────────┬──────────┬───────────┬─────────┐ │   │
│   │  │     .py      │    .js     │   .yml   │   .md     │  .lock  │ │   │
│   │  │     52%      │    23%     │   12%    │    8%     │   5%    │ │   │
│   │  │   14 files   │   6 files  │  3 files │  2 files  │ 1 file  │ │   │
│   │  └──────────────┴────────────┴──────────┴───────────┴─────────┘ │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│   TOP DIRECTORIES AFFECTED                                               │
│   src/auth/        ████████████████████████████████████████  12 files   │
│   src/middleware/  ████████████████████████████              8 files    │
│   tests/auth/      ██████████████████                        5 files    │
│   docs/api/        ██████                                    2 files    │
│                                                                          │
│   ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────────────┐   │
│   │ ✅ CI:PASS │ │ ✅ 2 REVIEWS│ │ 💬 5 CMNTS │ │ ⚠️ 1 UNRESOLVED    │   │
│   └────────────┘ └────────────┘ └────────────┘ └────────────────────┘   │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```
