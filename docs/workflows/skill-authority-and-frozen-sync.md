# Skill Authority and Computer Synchronization

This repository is the reviewed source and distribution boundary for shared active skills. Each computer receives that distribution in its local skill root. Local runtime copies are not a second source of truth.

## Authority Model

The active distribution is the intersection of two requirements:

1. the skill directory exists under `plugins/frozen-skills/skills/<skill-name>/`; and
2. the same name and path are listed in all four `frozen-skills` plugin manifests.

The synchronizer refuses to run if the Claude, Codex, Cursor, and Gemini manifests disagree on the plugin version or ordered skill list. `_incubator/` is outside the distribution regardless of what it contains.

On every computer, the default managed destination is:

```text
~/.agents/skills/<skill-name>/
```

This is the shared personal Agent Skills root discovered by Codex and compatible clients. A client may also maintain its own plugin cache or compatibility mirror; those surfaces do not change the repository's authority.

| Surface | Role |
|---|---|
| `plugins/frozen-skills/skills` | Reviewed source for active distributed skills. |
| Four `plugins/frozen-skills` manifests | Exact allowlist and version contract for the distribution. |
| `~/.agents/skills` | Default local runtime destination; unrelated personal skills coexist here. |
| Client plugin/cache directories | Client-managed runtime state, when a client has its own installer. |
| `_incubator/` | Gated review material; never synchronized or installed. |

## Synchronize a Computer

Clone this repository once on each computer. After cloning or pulling a new revision, inspect and apply the local plan:

```powershell
python scripts/sync_frozen_skills.py --check
python scripts/sync_frozen_skills.py --apply
```

Both commands validate the distribution first. `--check` writes nothing and exits with:

- `0` when every active skill and the management record are current;
- `1` when a safe install, update, adoption, or removal is pending;
- `2` when the distribution is invalid or local content conflicts with it.

`--apply` writes the active skills and the management record at `~/.agents/skills/.frozen-skills-sync.json`. A matching pre-existing skill is adopted without rewriting it. A previously managed, unchanged copy is safely updated. An unmanaged or locally modified copy is reported as a conflict and left untouched.

For a non-default root:

```powershell
python scripts/sync_frozen_skills.py --apply --destination "C:\path\to\skills"
```

On macOS or Linux, the same Python command works with POSIX paths.

## Removal and Conflict Rules

Removing a skill from the manifests does not delete it from computers during an ordinary apply. This makes removal a separate, reviewable operation:

```powershell
python scripts/sync_frozen_skills.py --check --prune
python scripts/sync_frozen_skills.py --apply --prune
```

Pruning removes only previously managed content that still matches its recorded digest. A locally modified retired skill becomes a conflict.

`--force` permits overwriting a conflicting active skill or deleting a conflicting retired skill. Review the exact reported skill first. Force is not the normal update path.

## Editing and Promotion Flow

For an already active skill, make the reusable change under `plugins/frozen-skills/skills/<skill-name>/`, validate it, review it, and then synchronize computers outward from the merged repository revision.

If a useful change was first prototyped in a local runtime copy, do not run `--force` immediately. Compare it with the repository source, deliberately port the reusable part into the source, validate and review that change, then synchronize. The conflict is evidence that authority must be reconciled, not a signal to copy in either direction automatically.

New skills enter `_incubator/` and pass the gate in `docs/skill-review/tracker.md` before promotion. Promotion requires adding the skill to all four plugin manifests and aligning the plugin and marketplace versions. On the next synchronization, the new active skill is installed on each computer.

## Marketplace Installation Is Different

Claude Code supports this repository as a marketplace:

```text
/plugin marketplace add Coldaine/frozenSkillz
/plugin install frozen-skills@coldaine-skills
```

That installs a Claude-managed plugin copy. It does not synchronize `~/.agents/skills` and does not prove that another client's similarly named manifest is installable. The Codex, Cursor, and Gemini manifests remain useful packaging metadata and are enforced as one distribution contract, while `sync_frozen_skills.py` is the repository-owned cross-platform local installation path.

## Required Checks

Before publishing a source or synchronization change:

```powershell
python scripts/validate_manifests.py
python -m unittest discover -s tests -v
git diff --check
```

For JSON manifests touched in the same change, also parse them with `ConvertFrom-Json`.

For an end-to-end smoke test, synchronize into a temporary empty directory, check it, and then remove only that temporary directory:

```powershell
$target = Join-Path $env:TEMP "frozen-skills-smoke"
python scripts/sync_frozen_skills.py --apply --destination $target
python scripts/sync_frozen_skills.py --check --destination $target
```

## Reporting

Every distribution change should report:

- which active source paths changed;
- whether manifests or versions changed;
- the validation and sync checks run;
- any destination conflict intentionally left unresolved;
- which repository revision was synchronized to each computer when that deployment is in scope.
