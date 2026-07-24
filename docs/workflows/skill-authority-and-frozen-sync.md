# Skill Authority and Computer Synchronization

This repository has two deliberate authority lanes. Manifest-listed active skills are reviewed here and synchronized outward to computers. Personal or gated skills are authored in the live personal root and mirrored into `_incubator/` for durable review. Mixing those directions recreates the drift this workflow is designed to prevent.

## Authority Model

### Active distributed skills

The active distribution is the intersection of two requirements:

1. the skill directory exists under `plugins/frozen-skills/skills/<skill-name>/`; and
2. the same name and path are listed in all four `frozen-skills` plugin manifests.

The synchronizer refuses to run if the Claude, Codex, Cursor, and Gemini manifests disagree on the plugin version or ordered skill list. For this lane, the repository copy is authoritative and each computer's managed copy is runtime output.

### Personal or gated skills

Personal skills that are not in the active manifests are authored under:

```text
~/.agents/skills/<skill-name>/
```

When this repository tracks one of those skills, its durable evaluation mirror lives under:

```text
_incubator/personal-skills/<skill-name>/
```

The live personal copy is authoritative for this lane. `_incubator/` is review material and is never installed by the active synchronizer.

| Surface | Role |
|---|---|
| `plugins/frozen-skills/skills` | Reviewed source for active distributed skills. |
| Four `plugins/frozen-skills` manifests | Exact allowlist and version contract for the active distribution. |
| `~/.agents/skills` | Managed runtime destination for active skills; authoring source for personal/gated skills. |
| `_incubator/personal-skills` | Durable review mirror for tracked personal/gated skills; never installed. |
| Client plugin/cache directories | Client-managed runtime state, when a client has its own installer. |

The management record at `~/.agents/skills/.frozen-skills-sync.json` distinguishes active managed copies from unrelated personal skills.

## Synchronize Active Skills to a Computer

Clone this repository once on each computer. After cloning or pulling a new revision, inspect and apply the local plan:

```powershell
python scripts/sync_frozen_skills.py --check
python scripts/sync_frozen_skills.py --apply
```

Both commands validate the distribution first. `--check` writes nothing and exits with:

- `0` when every active skill and the management record are current;
- `1` when a safe install, update, adoption, or removal is pending;
- `2` when the distribution is invalid or local content conflicts with it.

`--apply` writes the active skills and management record under `~/.agents/skills`. A matching pre-existing skill is adopted without rewriting it. A previously managed, unchanged copy is safely updated. An unmanaged or locally modified copy is reported as a conflict and left untouched.

For a non-default root:

```powershell
python scripts/sync_frozen_skills.py --apply --destination "C:\path\to\skills"
```

On macOS or Linux, the same Python command works with POSIX paths.

The destination must be disjoint from the repository. The synchronizer rejects a destination inside the checkout and a destination that contains the checkout. It never reverse-synchronizes installed content into reviewed active source.

## Named Profile Deployments

A profile is a named subset of the active distribution for a destination that must not receive every reviewed skill — for example, a standing runtime like Hermes. Profiles are defined at `profiles/<name>.json`:

```json
{
  "schema": 1,
  "name": "hermes-ops",
  "description": "Reviewed shared skills exposed to the standing Hermes operations runtime.",
  "skills": ["doppler", "pdm-cli-operations"]
}
```

Every skill listed in a profile must already be active in all four aligned manifests; a profile cannot select a skill the active distribution does not carry.

```powershell
python scripts/sync_frozen_skills.py --check --profile hermes-ops --destination /srv/hermes/skill-sets/hermes-ops --prune
python scripts/sync_frozen_skills.py --apply --profile hermes-ops --destination /srv/hermes/skill-sets/hermes-ops --prune
```

Rules specific to profile mode:

- `--profile` requires an explicit `--destination` and mandatory `--prune`; there is no default profile destination.
- A destination is owned by exactly one profile (or by the full, unprofiled distribution) for its lifetime. Reusing a destination under a different profile, or under the full distribution, is a conflict.
- Pruning is exact: any top-level destination content that is neither an active profile skill nor a still-recorded retired one is reported as a conflict, not silently ignored.
- `python scripts/validate_manifests.py` validates every file under `profiles/` against the active distribution as part of ordinary manifest validation.

A production consumer (deploy script, service unit, etc.) that pins a specific frozenSkillz commit for its profile sync must pin a commit reachable from `main` — never an unmerged or abandoned branch. A pin that only resolves on a branch is not reviewed distribution.

## Personal/Gated Skill Sync

After a deliberate rewrite or material fix of a personal skill that already has an incubator row:

1. edit and validate `~/.agents/skills/<name>/`;
2. mirror the live tree into `_incubator/personal-skills/<name>/`, including deletion of removed files;
3. update the row or notes in `docs/skill-review/tracker.md`; and
4. commit and push that mirror on a branch/PR in this repository in the same session.

A GitHub issue alone is not the durable rewrite. Uncommitted incubator files are not “in frozenSkillz.” “Stay gated” means do not add the skill to `plugins/frozen-skills/skills` or the manifests; it does not mean skip Git.

## Completion Contract

When the operator asks to rewrite, fix, sync, or land tracked skill material into this repository (including scout/intake under `_incubator/` and related tracker updates), the work is incomplete until the applicable authority lane is durable:

| Required | Not sufficient |
|---|---|
| Active source under `plugins/` updated, or live personal source updated | Opening an issue describing the rewrite |
| Matching active or incubator repository path updated | Copying files only in an uncommitted worktree |
| Tracker updated when status/work notes change | Deferring repository publication “for later” |
| Commit + push, with a PR when not already on one | A local-only sync unless explicitly requested |

Exception: the operator explicitly says “live-only, do not touch the repo.” Otherwise, repository landing is part of the task.

## Removal and Conflict Rules

Removing a skill from the manifests does not delete it from computers during an ordinary apply. This makes removal a separate, reviewable operation:

```powershell
python scripts/sync_frozen_skills.py --check --prune
python scripts/sync_frozen_skills.py --apply --prune
```

Pruning removes only previously managed content that still matches its recorded digest. A locally modified retired skill becomes a conflict.

`--force` permits overwriting a conflicting active skill or deleting a conflicting retired skill. Review the exact reported skill first. Force is not the normal update path and does not override a target that changes after planning.

## Editing and Promotion Flow

For an already active skill, make the reusable change under `plugins/frozen-skills/skills/<skill-name>/`, validate it, review it, merge it, and then synchronize computers outward from that repository revision.

If an active skill was accidentally edited in a local runtime copy, do not run `--force` immediately. Compare it with the repository source, deliberately port any reusable change into the repository, validate and review it, then synchronize. The conflict is evidence that authority must be reconciled.

New skills enter `_incubator/` and pass the gate in `docs/skill-review/tracker.md` before promotion. Promotion requires moving or adapting the skill into `plugins/frozen-skills/skills`, adding it to all four plugin manifests, and aligning plugin and marketplace versions. The next computer synchronization installs it.

## Marketplace Installation Is Different

Claude Code supports this repository as a marketplace:

```text
/plugin marketplace add Coldaine/frozenSkillz
/plugin install frozen-skills@coldaine-skills
```

That installs a Claude-managed plugin copy. It does not synchronize `~/.agents/skills` and does not prove that another client's similarly named manifest is installable. The Codex, Cursor, and Gemini manifests remain packaging metadata and one enforced distribution contract; `sync_frozen_skills.py` is the repository-owned cross-platform local installation path.

## Required Checks

Before publishing a source or synchronization change:

```powershell
python scripts/validate_manifests.py
python -m unittest discover -s tests -v
git diff --check
```

For JSON manifests touched in the same change, also parse them with `ConvertFrom-Json`.

For an end-to-end smoke test, use a unique temporary directory, assert both commands, and remove only that verified temporary path:

```powershell
$tempRoot = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
$target = Join-Path $tempRoot ("frozen-skills-smoke-" + [guid]::NewGuid().ToString("N"))
try {
    python scripts/sync_frozen_skills.py --apply --destination $target
    if ($LASTEXITCODE -ne 0) { throw "Smoke-test apply failed: $LASTEXITCODE" }
    python scripts/sync_frozen_skills.py --check --destination $target
    if ($LASTEXITCODE -ne 0) { throw "Smoke-test check failed: $LASTEXITCODE" }
} finally {
    $resolvedTarget = [System.IO.Path]::GetFullPath($target)
    if ($resolvedTarget.StartsWith($tempRoot, [System.StringComparison]::OrdinalIgnoreCase) -and
        (Test-Path -LiteralPath $resolvedTarget)) {
        Remove-Item -LiteralPath $resolvedTarget -Recurse -Force
    }
}
```

## Reporting

For an active distribution change, report:

- active source paths and manifest/version changes;
- validation and synchronization checks;
- destination conflicts intentionally left unresolved; and
- the repository revision synchronized to each computer when deployment is in scope.

For a personal/gated or incubator/scout landing change, report:

- the live path compared and incubator path changed;
- tracker or promotion status changes;
- any live-versus-incubator delta intentionally left unsynced; and
- branch, commit, and PR URL unless the operator requested live-only work.
