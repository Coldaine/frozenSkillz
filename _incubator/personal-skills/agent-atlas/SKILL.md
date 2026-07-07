---
name: agent-atlas
description: Router to per-tool reference docs for coding-agent tooling on Patrick's workstation. Fire whenever the task is about an agent tool itself - installing, configuring, launching, troubleshooting, or asking how it works or where it stores config, skills, sessions, or keys - for Claude Code, OMC, Codex, Cursor, Copilot, Gemini, Antigravity, OpenCode, Kilo, Goose, Qwen, or provider/key routing such as OpenRouter. Do not fire for ordinary coding tasks that merely run inside one of these tools.
---

# Agent Atlas

## Overview

This skill is a router: identify which agent tool the task concerns, open that tool's reference file under `references/`, and route the change to the right authority surface before editing anything. Live runtime files prove current state; `D:\_projects\coldaine-configurations` records durable workstation policy; `D:\_projects\frozenSkillz` holds reviewed or gated skill artifacts.

## Authority Order

1. For current runtime facts, inspect the live file, command, profile, registry key, extension setting, or tool diagnostic first.
2. For durable workstation policy, read or update `D:\_projects\coldaine-configurations\configurations\2026-07-07-agent-tool-configuration-policy.md`.
3. For reusable skill lifecycle, read `D:\_projects\frozenSkillz\docs\skill-review\tracker.md` and keep unreviewed skills in `_incubator/`.
4. For cross-project agent session learnings and retrospectives, read `D:\_projects\agent-control-plane` (despite the name, it is a learnings/reference store, not a runtime control plane; transcripts on disk remain ground truth).
5. For secrets or credentials, load the `doppler` skill before touching values; record names and owners only.

## Workflow

1. Identify the tool and mode: Claude Code, OMC, Codex, Cursor, Copilot, Gemini, OpenCode, Kilo, Antigravity, or another agent client.
2. Read the relevant live config surface. Do not infer from a cached plugin, an old skill, or memory alone.
3. Classify the change:
   - live setup fix: edit the live tool config after backing up or reading it;
   - durable policy: update the coldaine-configurations policy record;
   - reusable skill content: add or update an incubated frozenSkillz skill and tracker row;
   - active marketplace skill: promote only through the frozenSkillz review gate and manifests.
4. Report the status boundary explicitly: live verified, policy recorded, gated candidate, active marketplace, or not changed.
5. If the task changes live configuration, provide the exact verification command that proves the tool loaded the intended surface.

## Current Claude / OMC Split

As of the 2026-07-07 policy record, this workstation intentionally separates:

- `claude` -> vanilla Claude Code using `C:\Users\pmacl\.claude`
- `claudeDanger` -> vanilla Claude Code with `--dangerously-skip-permissions`
- `omcc` / `claudeOmc` -> OMC profile using `C:\Users\pmacl\.claude-omcc`, danger mode by default
- `omccSafe` / `claudeOmcSafe` -> OMC profile without danger mode
- `omcProfile` -> OMC CLI against `C:\Users\pmacl\.claude-omcc`

Before changing those assumptions, re-check the PowerShell profile and the two config roots.

## Per-Tool References

Read `references/workstation-agent-config-map.md` for the overall path map, then the file for the tool at hand:

- `references/codex.md` — Codex CLI: config.toml, plugins, sessions, secrets boundary
- `references/cursor.md` — Cursor IDE + cursor-agent: mcp.json, global-first config pattern, setup audit report
- `references/gemini-antigravity.md` — Gemini CLI and Antigravity (shared `.gemini` root)
- `references/opencode.md` — OpenCode + oh-my-openagent: profiles, providers, `opencode.db` session database
- `references/kilo.md` — Kilo: duplicated `.kilo`/`.kilocode` roots (canonical root unverified)
- `references/copilot-cli.md` — GitHub Copilot CLI
- `references/goose.md` — Goose (lightly used)
- `references/qwen.md` — Qwen CLI (root exists; no chat history found on this machine)
- `references/openrouter.md` — OpenRouter provider/key routing (not an app; keys via Doppler)

Claude Code and OMC are covered in this file and the map.

Every reference file is an incomplete draft against a canonical checklist. `references/research-todo.md` defines what we must eventually know about every agent and tracks per-tool gaps; a dedicated research agent will fill it in. When you learn a missing fact while working, update the tool's reference file and tick it off there.

For session/transcript file formats across all tools, `D:\_projects\llm-archiver\tools\*.yaml` holds parser definitions (claude_export, codex, copilot_cli, gemini, goose, kilo, kimi, opencode, qwen), and `D:\_projects\agent-control-plane\capture\scratch\` holds reverse-engineering notes.

Common anchors:

- PowerShell profile: `C:\Users\pmacl\OneDrive\Documents\PowerShell\Microsoft.PowerShell_profile.ps1`
- Vanilla Claude root: `C:\Users\pmacl\.claude`
- OMC Claude root: `C:\Users\pmacl\.claude-omcc`
- Live personal shared skills: `C:\Users\pmacl\.agents\skills`
- Frozen evaluation copies: `D:\_projects\frozenSkillz\_incubator\personal-skills`
- Frozen active plugin skills: `D:\_projects\frozenSkillz\plugins\frozen-skills\skills`

## Common Mistakes

- Editing frozenSkillz when the user asked to change live Claude or Cursor behavior. FrozenSkillz is a review boundary, not the runtime.
- Editing live config without recording durable policy when the decision should survive future sessions.
- Treating `_incubator/` as installed. It is gated evaluation material.
- Copying secrets into docs. Record secret names, stores, and owners only.
- Assuming `claude` and `omcc` use the same root. They are intentionally split.
