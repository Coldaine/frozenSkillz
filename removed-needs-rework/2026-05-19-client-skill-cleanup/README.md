# Removed Client Skills Needing Rework

Archived on 2026-05-19 from `C:\Users\pmacl` during Claude/Codex/Gemini skill-surface cleanup.

These folders are intentionally not placed under the active `plugins/frozen-skills/skills/` publication path. They are preserved here for later review, rewriting, or deletion decisions.

## Contents

- `morph-skills/`: Morph-authored skills removed from active `.agents`, `.claude`, and `.codex` skill roots because they referenced Morph-specific tools (`edit_file`, `codebase_search`, `github_codebase_search`) that were not confirmed as available in the current client toolkit.
- `omc-shadowed-personal-skills/`: old full-body OMC personal skills removed from `~/.claude/skills` because OMC v4.14.0 now provides plugin-managed compact skill shims and these personal copies shadowed plugin skills.
- `pr-review-canvas/`: tombstone for a broken skill reference. Claude and Codex referenced it, but no live source directory was present at cleanup time.

## Rework Rule

Do not publish any archived skill from this folder as-is. Before reactivation, inspect tool assumptions, update client-specific wording, verify the target client actually exposes the referenced tools, and then move the revised skill through the normal frozen skill publication flow.
