# Skill Authority and Frozen Sync

This repository is the durable marketplace and registry boundary for reviewed shared skills. It is not the live runtime root for every local agent client.

## Authority Model

On this Windows workstation, personal shared skills are authored and installed as one real copy under:

```text
C:\Users\pmacl\.agents\skills\<skill-name>\
```

Tool-specific skill folders are compatibility or runtime surfaces:

| Client surface | Role |
|---|---|
| `C:\Users\pmacl\.agents\skills` | Canonical live personal skill root. |
| `C:\Users\pmacl\.claude\skills` | Claude Code compatibility mirror. Personal skills should be junctions to `.agents\skills`, not independent copies. |
| `C:\Users\pmacl\.config\opencode\skills` | OpenCode-specific real skill root. Keep empty unless a skill is intentionally OpenCode-only. |
| `C:\Users\pmacl\.codex\skills` | Codex system/runtime surface. Personal skills should not be authored here. |
| `C:\Users\pmacl\.gemini\skills`, `C:\Users\pmacl\.cursor\skills`, `C:\Users\pmacl\.kilo\skills` | Tool-specific roots. Real copies here are exceptions and must be treated as possible drift unless intentionally tool-only. |

`frozenSkillz` owns the reviewed, publishable copy under:

```text
plugins/frozen-skills/skills/<skill-name>/
```

That copy is what marketplace consumers install. It should reflect reviewed live practice, but it is not the first place to make local live edits.

## Active vs Gated Skills

Active marketplace skills are listed in all frozen-skills manifests and live under `plugins/frozen-skills/skills/`.

Gated or historical skills live under `_incubator/`. Do not treat `_incubator/` as installable runtime state. Promote from `_incubator/` only through `docs/skill-review/tracker.md` and the manifest update process.

## Sync Rule

When a live shared skill and an active frozen skill have the same name, compare the live `.agents` copy against the frozen copy:

```powershell
git diff --no-index -- "C:\Users\pmacl\.agents\skills\<skill-name>" "D:\_projects\frozenSkillz\plugins\frozen-skills\skills\<skill-name>"
```

If the live copy contains reviewed improvements that are broadly reusable, update the frozen copy and note the sync in this repo. If the delta is local-only, project-specific, or unreviewed, leave the frozen copy unchanged and document why.

Do not auto-promote every live `.agents` skill into `plugins/frozen-skills/skills/`. A new active frozen skill needs the review gate in `docs/skill-review/tracker.md`, manifest entries, and version updates.

If an active frozen skill has no live `.agents` counterpart, treat frozenSkillz as the source for that skill.

### Personal / gated skills (`_incubator/personal-skills/`)

Many personal skills also have a gated evaluation copy under:

```text
_incubator/personal-skills/<skill-name>/
```

**Live edit still starts in `~/.agents/skills/<name>/`.** After a deliberate rewrite or material fix of a skill that already has an incubator row:

1. Sync the live tree into `_incubator/personal-skills/<name>/` (mirror; delete removed files).
2. Update the tracker row in `docs/skill-review/tracker.md`.
3. **Commit and push that sync on a branch / PR in this repo in the same session.**

A GitHub Issue alone is not the durable rewrite. Uncommitted incubator files on disk are not “in frozenSkillz.” “Stay gated” means do **not** promote into `plugins/frozen-skills/skills/` or manifests — it does **not** mean skip git.

## Completion Contract (do not skip)

When the operator asks to rewrite, fix, or sync a skill that this repo tracks (active under `plugins/` **or** gated under `_incubator/`), the work is incomplete until:

| Required | Not sufficient |
|---|---|
| Live `~/.agents` updated (if that skill is live-authored) | Opening an Issue describing the rewrite |
| Matching path under `plugins/…` or `_incubator/…` updated | Robocopy / copy left only in the working tree |
| Tracker updated when status/work notes change | “Commit when you want” / deferring the PR |
| **Commit + push** (branch + PR when not on an open PR) | Local-only sync “for later” |

Exception: operator explicitly says “live-only, do not touch the repo.” Otherwise assume **repo landing is part of the task**.

Do not treat the global agent habit “ask before committing” as license to leave frozenSkillz skill rewrites uncommitted. In this repository, a requested skill rewrite implies commit and push unless told otherwise.

## Current Snapshot: 2026-07-06

The active frozen-skills plugin registers two skills:

| Skill | Live `.agents` counterpart | Sync status |
|---|---|---|
| `doppler` | `C:\Users\pmacl\.agents\skills\doppler` | Synced in this pass; frozen copy now includes the live 2026-06-29 learnings. |
| `external-skill-intake` | None found | FrozenSkillz is the source copy. |

The broader machine still has tool-local skill surfaces and some stale junctions. Treat those as runtime/config hygiene, not as authoritative source unless a tool-specific skill is intentionally maintained outside `.agents`.

On 2026-07-06 the user's personal `~/.agents/skills` set was reference-copied into `_incubator/personal-skills/` (gated, not installable) so the repo owns a copy of each for evaluation. `deepinit` was excluded (installed OMC package skill) and `doppler` was already active. See `docs/skill-review/tracker.md` → "Personal skills intake" for per-skill provenance/status. The live `.agents` copies remain the source of truth; these frozen copies are evaluation reference, not runtime.

## Required Checks

Before publishing a sync:

```powershell
python scripts/validate_manifests.py
git diff --check
```

For JSON manifests touched in the same change, also parse them with `ConvertFrom-Json`.

## Reporting

Every frozen sync should report:

- which live skill path was compared;
- which frozen path changed (`plugins/…` or `_incubator/…`);
- whether the skill was active or gated;
- whether manifests changed;
- validation commands run;
- any live-vs-frozen delta intentionally left unsynced;
- **branch / commit / PR URL** where the sync landed (required unless operator said live-only).
