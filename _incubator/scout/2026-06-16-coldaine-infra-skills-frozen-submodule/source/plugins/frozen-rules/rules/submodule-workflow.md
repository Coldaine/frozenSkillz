---
paths:
  - "**/.gitmodules"
---

# Git Submodule Workflow

This rule applies to any git submodule in the project. Submodules are separate repositories — their files are owned by the upstream repo.

## The Golden Rule

**Never modify submodule files from the consuming repo.** Changes must go through the upstream repository.

## What You CAN Do (Read-Only)

- Read files inside submodules for reference
- Copy patterns or ideas from submodule code
- Check what version/commit the submodule points to

## What You MUST NOT Do

- **Edit, create, or delete files** inside the submodule directory
- **Accidentally stage submodule pointer changes** — avoid `git add <submodule-path>` or `git add .` from the repo root unless you are intentionally updating the pointer as described below
- **Run `git checkout` inside the submodule** without understanding detached HEAD state

## How to Make Changes to Submodule Content

1. **Find the upstream URL:**
   ```bash
   git config --file .gitmodules --get submodule.<path>.url
   ```

2. **Clone the upstream repo separately:**
   ```bash
   git clone <upstream-url> /tmp/<repo-name>
   ```

3. **Make changes in the upstream repo** — branch, commit, push, PR as normal.

4. **Update the submodule pointer** (after upstream changes are merged):
   ```bash
   git submodule update --remote <submodule-path>
   ```

5. **Review what changed:**
   ```bash
   git diff --submodule
   ```

6. **Commit the pointer update:**
   ```bash
   git add <submodule-path>
   git commit -m "chore: update <submodule-name> to latest"
   ```

## Common Pitfalls

### Detached HEAD
Inside a submodule, you're in detached HEAD state. Commits made here are NOT on a branch and can be lost.

### Accidental pointer changes
`git add .` from the repo root stages the submodule pointer if it differs from what .gitmodules specifies. This is the #1 cause of accidental submodule breakage.

### Not initialized
After cloning, submodules start empty. Initialize with:
```bash
git submodule update --init
```
A `-` prefix in `git submodule status` means "not initialized."

## Project Customization

Override this rule to specify:
- Exact submodule path(s) and upstream repo URL(s)
- Task runner commands for submodule management (e.g., `just update-skills`)
- Which branch the submodule tracks
