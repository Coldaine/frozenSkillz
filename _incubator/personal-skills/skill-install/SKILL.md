---
name: skill-install
description: >
  Install, consolidate, or repair Agent Skills (SKILL.md) across multiple AI
  coding tools on this machine using a single-source-of-truth layout. Use when
  asked to install a skill "in all coding tools", when a skill is duplicated
  across tool directories (~/.codex/skills, ~/.copilot/skills, etc.), when a
  skill shows up multiple times in a tool's picker, or when migrating skills to
  the .agents/skills open standard. Covers Claude Code, OpenCode (+oh-my-openagent),
  Codex, Gemini, Cursor, Copilot, and Kilo.
---

# Installing skills across all coding tools

## The one rule

**One physical copy lives in `~/.agents/skills/<name>/`. Never fan a skill out into
per-tool directories.** All standard-compliant tools read `~/.agents/skills` natively.
The only exception is Claude Code (see below), which gets a *junction/symlink*, not a copy.

Fan-out (a real folder in every `~/.<tool>/skills`) is WRONG: tools that read more than one
root (OpenCode, Cursor, Kilo) then load the same skill several times, and Codex does not
dedup at all — that is the "seventeen copies" failure mode.

## How each tool discovers skills (verified June 2026)

| Tool | Reads `~/.agents/skills`? | Other user-level dirs it reads | Dedup by name? |
|---|---|---|---|
| **Claude Code** | **NO** (open req [#31005], unimplemented) | only `~/.claude/skills` | n/a |
| OpenCode (+omo) | YES | `~/.config/opencode/skills`, **and `~/.claude/skills` unless disabled** | undocumented |
| Codex CLI | YES (its *only* user dir) | — (`~/.codex/skills` is NOT official) | **NO — lists duplicates** |
| Gemini CLI | YES | `~/.gemini/skills` | yes (last-wins + warning) |
| Cursor | YES | `~/.cursor/skills` (+`.claude` compat) | undocumented |
| Copilot CLI | YES | `~/.copilot/skills` | undocumented (same tier) |
| Kilo Code | YES | `~/.kilo/skills` (+`.claude` compat) | yes (last-wins + warning) |

Because Claude Code refuses `.agents/skills`, the canonical copy is mirrored into
`~/.claude/skills/<name>` as a **junction** (Windows) / **symlink** (Unix) — same files, no
second copy. OpenCode also scans `~/.claude/skills`, so that mirror would double-count there;
the OpenCode flag below suppresses it.

## OpenCode: stop the `.claude` double-count (already set on this machine)

omo (oh-my-openagent) is what imports Claude Code skills into OpenCode. Disable it in
`~/.config/opencode/oh-my-openagent.json`:

```json
"claude_code": { "skills": false }
```

Then OpenCode loads only `.agents/skills` (canonical) and ignores the `.claude` mirror.

**Do NOT** use the env var `OPENCODE_DISABLE_CLAUDE_CODE=1` — as of OpenCode v1.1.50 it ALSO
disables `.agents/skills` (bug [#12432]), which would hide every canonical skill. There is no
working `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS` var (it was hallucinated in some docs).

## Install a new skill (Windows / PowerShell)

```powershell
$canon = "$HOME\.agents\skills\<name>"
Copy-Item -Recurse <source-skill-dir> $canon          # 1) one real copy
$link = "$HOME\.claude\skills\<name>"                  # 2) mirror for Claude Code
if (Test-Path $link) { (Get-Item $link).Delete() }     #    (removes link only, never target)
New-Item -ItemType Junction -Path $link -Target $canon
```

Unix equivalent: `cp -r src ~/.agents/skills/<name>` then
`ln -s ~/.agents/skills/<name> ~/.claude/skills/<name>`.

The folder name MUST equal the `name:` in SKILL.md frontmatter (the standard requires it),
so you cannot rename to dodge a collision — physical de-duplication is the only fix.

## Consolidate / repair an over-duplicated skill

1. Pick the canonical content (newest if copies differ) → ensure it is the real dir in `~/.agents/skills/<name>`.
2. Back up, then delete the copies in `~/.codex|.copilot|.cursor|.gemini|.kilo/skills` and `~/.config/opencode/skills`.
3. Replace `~/.claude/skills/<name>` with a junction/symlink to the canonical copy.
4. Leave tool-bundled skills alone (e.g. Codex `.system`/`codex-primary-runtime`, Cursor's
   `code-edit`/`explore`, `~/.claude/skills/omc-learned`) — those are not yours to move.

## Verify

```powershell
Get-ChildItem -Directory "$HOME\.claude\skills" | % {
  $i=Get-Item $_.FullName
  "{0} {1}" -f $_.Name, ($(if(($i.Attributes -band 1024)){"-> $($i.Target)"}else{"REAL"}))
}
```

Every personal skill should be a junction here; the real copy should exist once under
`~/.agents/skills`. For final certainty on OpenCode, run its `/skills` list and confirm no
skill appears twice.
