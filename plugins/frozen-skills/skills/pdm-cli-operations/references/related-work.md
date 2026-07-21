# Related work (future enhancement candidates)

Load this file **only** when evaluating whether to extend `pdm-cli-operations`, add a sibling skill, or compare adjacent Proxmox agent tooling. Do **not** treat these as dependencies, defaults, or a parallel control plane for normal fleet work.

**Authority reminder:** this skill’s normal surface is the official `proxmox-datacenter-manager-client`. Native PVE/PBS and third-party MCP/API toolkits remain explicit break-glass or separate skills until real usage proves a gap.

Star counts below were fetched live on **2026-07-20**; re-check with `gh repo view owner/repo --json stargazerCount` before citing them elsewhere.

## Official reference (not a skill)

| Resource | Stars | Role vs this skill |
|---|---|---|
| [proxmox/proxmox-datacenter-manager](https://github.com/proxmox/proxmox-datacenter-manager) | 135 | Upstream PDM product + CLI docs. Source of truth for client syntax; not agent packaging. |

## Adjacent agent skills / toolkits (PVE-oriented)

These target **direct PVE API, node helpers, or MCP**, not the official PDM client. Mine **patterns** (evidence loops, safety gates) only after repeated real intents fail under PDM; do not merge their stacks into this skill’s happy path.

| Resource | Stars | What it is | Possible future use |
|---|---|---|---|
| [eddygk/proxmox-ops](https://github.com/eddygk/proxmox-ops) | 11 | PVE ops `SKILL.md` + `pve.sh`, disk resize, guest-agent IP, provisioning refs | Steal safety/checklist patterns; or seed a **sibling** break-glass / node-ops skill if agents keep needing node-local flows |
| [codeandsolder/proxmox-agent-skill](https://github.com/codeandsolder/proxmox-agent-skill) | 0 | Agent-oriented Proxmox Python toolkit (`pxas` / proxmoxer-style scripting; repo description may also mention MCP) | Compare structured error / allowlist ideas; keep out of PDM process-interface path |
| [agentify-sh/cursor-proxmox-mcp](https://github.com/agentify-sh/cursor-proxmox-mcp) | 10 | Cursor MCP server over Proxmox REST (VM lifecycle tools) | Explicit **alternative interface**. Document coexistence with Homelab MCP experiments; do not fold into this skill |
| [vinnie357/claude-skills](https://github.com/vinnie357/claude-skills) | 21 | Broader Claude skill pack; Proxmox skill mentions PDM in estate/architecture notes | Optional decision-table inspiration (PDM vs cluster); belongs in ops docs more than this skill |
| [xobotyi/cc-foundry](https://github.com/xobotyi/cc-foundry) | 18 | Claude Code foundry plugins/skills; Proxmox skill mentions PDM 1.x as central management | Same as above — architecture framing, not PDM CLI operations |

## Marketplace / catalog entries (non-GitHub primary)

- [Proxmox VE API Orchestrator (heyclau.de)](https://heyclau.de/entry/skills/proxmox-ve-api-orchestrator) — API orchestration / auth runbooks for PVE.
- [Proxmox VE API Capability Pack (heyclau.de)](https://heyclau.de/entry/skills/proxmox-ve-api-capability-pack) — lifecycle / task-polling capability pack framing.

Treat as inspiration catalogs only; verify license and freshness before any adaptation.

## Enhancement policy (when uses become clear)

1. Log real agent intents against this skill (inventory, snapshot, migrate, Windows bridge, etc.).
2. If a repeated intent is **PDM-capable**, thicken `SKILL.md` / `commands.md` from live client behavior.
3. If a repeated intent is **not** PDM-capable, prefer a **sibling skill** or ops-repo runbook over expanding this skill into MCP/`proxmoxer`/`qm`.
4. Revisit the table above only when step 3 fires — not preemptively.
