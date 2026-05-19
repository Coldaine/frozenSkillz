---
name: review-repo-docs
description: Review and fix all agent documentation (AGENTS.md, AGENTS.md, README, docs/) by validating against actual codebase state. Finds stale references, contradictions, and gaps.
user_invocable: true
triggers:
  - review docs
  - fix documentation
  - audit docs
  - AGENTS.md
  - AGENTS.md
  - stale docs
  - documentation review
---

# Review Repo Docs

Validates all agent documentation by checking actual codebase state. Identifies broken references, outdated paths, contradictions, and missing documentation.

## When to Use

Run when:
- Adding/moving/deleting files or directories
- Updating tech stack or workflows
- Documentation feels out of sync with code
- User mentions "stale docs" or "broken links"
- After major refactoring

## Process

### 1. Discover Documentation Files

Find all documentation in the project:

```bash
find . -maxdepth 3 \( -name "AGENTS.md" -o -name "AGENTS.md" -o -name "README*" -o -name "docs" -type d \) -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null
cat AGENTS.md AGENTS.md README.md 2>/dev/null | head -200
```

Also check global docs:
```bash
cat ~/.Codex/AGENTS.md ~/.Codex/AGENTS.md 2>/dev/null | head -100
```

### 2. Extract File References

Parse documentation for claimed files/paths:

- Look for code blocks with paths: `` `path/to/file` ``
- Look for links: `[text](path/to/file)`
- Look for bash commands: `ls`, `cat`, `find` in examples
- Look for directory trees and tables listing structure
- Look for "File at X" statements

Extract references as list: `docs/thing.md`, `src/utils.js`, `scripts/build.sh`, etc.

### 3. Validate Against Codebase

For each reference, verify it exists:

```bash
# Check if file/dir exists
test -f "path/to/file" && echo "EXISTS" || echo "MISSING"
test -d "path/to/dir" && echo "EXISTS" || echo "MISSING"

# Glob for similar files if not found
find . -name "*similar*" -not -path "*/.git/*" 2>/dev/null
```

### 4. Check Cross-References

Look for contradictions between docs:

- **AGENTS.md mentions file X** but **AGENTS.md says file Y**
- **README says X is at path A** but **docs/ structure shows path B**
- **tech stack lists Node.js** but **package.json missing** (or vice versa)
- **Workflow instructions reference non-existent command**

Track: File name, location in doc, claimed value, actual value.

### 5. Verify Commands

Test documented commands:

```bash
# If doc says "run: npm install"
npm install --dry-run 2>&1 | head -5

# If doc says "run: python scripts/thing.py"
python scripts/thing.py --help 2>&1 | head -5

# If doc says file at "data/config.json"
test -f data/config.json && cat data/config.json | head -5
```

### 6. Build Report

Output HIGH/MEDIUM/LOW priority fixes:

```
# Review Results: [PROJECT]

## HIGH Priority (Broken References)
- [ ] AGENTS.md line X: mentions "docs/thing.md" — file does not exist
- [ ] AGENTS.md: lists `state_cartographer/` as package but should be `state_cartographer/` (actual dir)
- [ ] README: command `npm run build` fails — no "build" script in package.json

## MEDIUM Priority (Contradictions)
- [ ] AGENTS.md says tech stack includes Redis, AGENTS.md doesn't mention it
- [ ] README path: `/docs/setup.md` vs AGENTS.md path: `docs/setup.md` (trailing slash inconsistent)

## LOW Priority (Gaps)
- [ ] No documentation for `scripts/cleanup.sh` (exists but not documented)
- [ ] `configs/` directory mentioned in AGENTS.md but no AGENTS.md section for it

## Validation Summary
- Files checked: X
- References validated: Y
- Broken: Z
- Contradictions: W
```

### 7. Apply Fixes (Optional)

If user confirms, make changes:

```bash
# Backup originals
cp AGENTS.md /tmp/AGENTS.md.backup
cp AGENTS.md /tmp/AGENTS.md.backup
cp README.md /tmp/README.md.backup 2>/dev/null
```

Then use Edit tool to:
- Fix paths to actual file locations
- Remove references to non-existent files
- Align contradicting statements
- Add missing documentation for existing files

## Output Format

```
COMPLETED AUDIT: [project name]
STATUS: [N broken refs] [M contradictions] [P gaps]

FILES CHECKED:
- AGENTS.md: X references validated
- AGENTS.md: X references validated
- README.md: X references validated
- docs/: X references validated

FINDINGS:
HIGH (broken):    Z items
MEDIUM (conflict): W items
LOW (gaps):       V items

APPLIED FIXES: [if requested]
- Fixed [count] broken paths
- Resolved [count] contradictions
- Backed up originals to /tmp/
```

## Key Validations

✓ File existence (use Glob, test -f, test -d)
✓ Path consistency (trailing slashes, relative vs absolute)
✓ Command validity (run with --help or --dry-run)
✓ Cross-doc consistency (same file described same way everywhere)
✓ Structure alignment (docs claim matches actual dir tree)
✓ Tech stack match (package.json ↔ AGENTS.md declarations)

## What This Does NOT Do

- Generate generic templates (use `Codex-md-enhancer` for that)
- Mine conversation history (separate archival skill)
- Score documentation quality (this is binary: correct or wrong)
- Create new doc files (only validates/fixes existing ones)
- Enforce style (only enforce accuracy)

## Integration

Works with:
- `Codex-md-enhancer` (after reviewing, enhance structure if needed)
- Git workflows (run before committing doc changes)
- CI/CD (gate docs validation on PRs)

## Tools Used

- **Glob**: Find files referenced in docs
- **Read**: Load documentation files
- **Edit**: Fix broken references
- **Bash**: Test command validity, check file existence
- **Grep**: Extract references from docs
