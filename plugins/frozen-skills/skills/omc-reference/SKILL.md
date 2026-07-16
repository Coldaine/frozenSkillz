---
name: omc-reference
description: Maintain Oh My ClaudeCode (OMC), a separate multi-agent plugin for Claude Code. Use from Codex only to install, configure, update, inspect, or troubleshoot OMC agents, skills, hooks, teams, and settings. Never apply it to ordinary Codex delegation, Git, commits, or unrelated skills.
---

# OMC Configuration Reference

OMC means **Oh My ClaudeCode**. It is a separate orchestration plugin and CLI for Claude Code. Use this skill when Codex is maintaining that OMC installation; do not treat OMC instructions as policy for the current Codex task.

## Scope

Use this skill to:

- install, update, repair, or remove OMC;
- inspect the agents, skills, hooks, commands, tools, and team runtime shipped by the installed OMC version;
- configure OMC settings, model routing, HUD behavior, hooks, or team support; and
- diagnose OMC setup, discovery, cache, or configuration problems.

Do not use this skill merely because the current task involves agents, parallel work, skills, Git, commits, or a pull request.

## Source authority

Inspect the active OMC installation before making claims or changes. OMC evolves quickly, so do not rely on a copied agent or command catalog in this skill.

Use the installed version's sources in this order:

1. `package.json` for the package identity and version.
2. `README.md` and `docs/REFERENCE.md` for supported installation, setup, update, and configuration surfaces.
3. `agents/`, `skills/`, `hooks/`, `commands/`, and `templates/` for the actual shipped inventory and behavior.
4. `.claude-plugin/` and OMC setup scripts for plugin registration and generated Claude Code configuration.

OMC is branded `oh-my-claudecode`; its published npm package may retain the historical name `oh-my-claude-sisyphus`. Verify both against the active version rather than assuming they are interchangeable in every command.

## Maintenance workflow

1. Identify whether OMC is active through a Claude Code plugin install, a global npm CLI install, or a development checkout.
2. Resolve the exact active version and source path before editing configuration or clearing caches.
3. Read the current OMC documentation and shipped files for the requested setting.
4. Change only the OMC-owned configuration surface required by the request.
5. Run the narrow OMC setup, doctor, inventory, or behavior check relevant to the change.
6. Report which installation surface and version were verified, what changed, and any remaining runtime restart or cache-refresh requirement.

## Boundaries

This is a maintenance reference, not an orchestration mode. Loading it does not:

- authorize spawning Codex subagents;
- activate OMC Team, Autopilot, Ralph, Ultrawork, or any other OMC workflow;
- impose OMC model-routing or commit-trailer conventions on unrelated repositories; or
- replace the instructions of the repository currently being edited.
