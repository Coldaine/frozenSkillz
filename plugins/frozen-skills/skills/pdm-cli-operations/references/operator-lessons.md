# Operator lessons from prior agent failures (k8s → PDM)

Load this file **only** when hardening `pdm-cli-operations`, writing evals, or deciding whether to add MCP/`qm`/kubectl-style shortcuts. Do not load for ordinary fleet inventory or mutation work.

Evidence base (2026-07-21): local [AgentsView](http://127.0.0.1:8080) (~1805 sessions), plus the Cursor mining session `cursor:26dd7dc4-bf09-44c6-ad58-44111af889bf` that ranked Patrick’s stated solutions across Cursor/Codex/Claude history. This is a distilled map, not a full forensic export.

## What kept going wrong (k8s / Cursor / Claude / Codex)

| Failure mode | What agents did | Homelab countermeasure that emerged |
|---|---|---|
| **Typist on live state** | `kubectl apply` / patch / MCP mutate without a platform loop | P0 gates (`gate-mutating-*.ps1`); “platform operator, not Kubernetes typist” |
| **Authored ≠ applied** | Treated git/docs as done | “Status means applied, not authored” (ADR / AGENTS); re-probe live |
| **Auto-fix without authority** | Drift-correct live cluster | `cluster-status` ConfigMap = read/propose-only; never auto-fix |
| **Fake-applyable / stale YAML** | Succeeded against wrong context or stale pins | Diff git vs live; version re-verify; fewer pretend manifests |
| **Wrong control plane** | Second imperative path when the first was hard | Explicit break-glass; no parallel plane as workaround |
| **Doc sprawl / PROGRESS** | Agents buried truth in temporary docs | Thin AGENTS router; Issues for work; promote-then-delete |

## How that maps onto this skill

| Lesson | Already in `pdm-cli-operations`? | Keep / tighten |
|---|---|---|
| One normal control surface | Yes — official PDM client (+ env launcher) | Keep; reject MCP/`qm` as “easier” default ([related-work.md](related-work.md)) |
| Prove before mutate | Yes — `remote list`, pre-state, identity (remote+node+VMID) | Keep; treat as non-skippable |
| Accepted ≠ completed | Yes — UPID/task started vs `stopped`+`OK` + post-state | Keep; same lesson as “applied means done” |
| Fail closed on trust/auth | Yes — TLS pin, no password on Windows bridge | Keep |
| Break-glass explicit | Yes — native PVE/PBS only when required | Keep; never silent pivot |
| No project diary in skill | Yes — inventory in owning ops repo; gated env notes | Keep |
| Env binding separate from contract | Yes — `env-notes.md` | Keep |
| Mutation authority | Partial — “use supplied identity; don’t silently downgrade” | Good; do **not** invent a P0-gate clone inside the skill — gates belong in the agent host / Hermes / ops repo |
| “Status means applied” wording | Implicit via task evidence | Optional: one bullet mirroring that phrase for agents coming from k8s habits |
| Evals for anti-typist negatives | Partial — break-glass / WSL / generic infra negatives | Optional: add negatives like “just use proxmox MCP”, “ssh to node and qm”, “skip task wait” |

## What not to copy from the k8s stack into this skill

- **P0 / cluster-status machinery** — cluster-specific; Hermes/ops host owns mutation policy for k8s. PDM skill owns *how* to talk to PDM safely once authorized.
- **kubectl/Helmfile/CAPMOX workflows** — different layer (cluster vs fleet roof).
- **MCP Proxmox servers** — recreate the typist failure mode under a different API.
- **PROGRESS.md / long stretch diaries** — anti-pattern already rejected in solution mining.

## Workflow shape this skill should preserve (operator, not typist)

```text
authorize (env identity + secrets skill)
  → bind (ops-repo inventory; launcher or raw login)
  → prove (remote list / version)
  → identify (remote + node + guest; pre-state)
  → mutate once (only if task + identity allow)
  → evidence (terminal task + post-state)
  → report (redacted)
```

If a step fails, stop at that boundary. Do not open a second control plane to “finish the ticket.”

## When to thicken the skill from live use

Only after repeated real intents (Hermes/Codex/Cursor logs or AgentsView search) show the same gap. Prefer:

1. Intent-table row or failure-routing row
2. Eval negative
3. Sibling skill (break-glass PVE) — not MCP inside this package

See also [related-work.md](related-work.md) for adjacent repos and the enhancement policy.
