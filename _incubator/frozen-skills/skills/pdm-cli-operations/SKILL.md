---
name: pdm-cli-operations
description: Operate Proxmox VE and Backup Server fleets through the official Proxmox Datacenter Manager client. Use for PDM inventory, status, metrics, guest lifecycle, migration, snapshots, tasks, and fleet troubleshooting. Do not use for native PVE or PBS break-glass access when PDM is unavailable.
---

# PDM CLI Operations

Use `proxmox-datacenter-manager-client` as the shared process interface for agents and operators. It connects to the standing PDM API; it is not another service, database, MCP server, or source of truth.

The official client currently requires a compatible amd64 Debian environment, network access to a same-major PDM server, and a secret-safe credential command.

## Operating Contract

- Load `$doppler` before handling authentication in a Doppler-backed environment; otherwise load the applicable secrets-management skill.
- Resolve the PDM endpoint, TLS fingerprint, non-secret auth ID, and target names from the environment's canonical operational repository. Never copy that inventory into this skill.
- Verify the client and PDM share the same major version before relying on it.
- Pass the password through `--password-command`. Never place a password in argv, a committed file, a prompt, or durable output.
- Pin the expected TLS certificate with `--fingerprint`; do not suppress certificate verification.
- Request `--output-format json` for agent work and preserve the original JSON as evidence when the task requires an audit trail.
- Start with `remote list`, then select the exact remote, node, and guest. A VMID is not globally meaningful without its remote.
- Read current state immediately before a mutation. Execute only the authorized target and action; do not broaden a repair because nearby drift is visible.
- Treat an accepted request or returned UPID as started, not completed. Follow the task to a terminal result when the command is asynchronous, then read state again.
- Distinguish client/authentication failure, PDM unavailability, remote unavailability, and an unsuccessful remote task. Report the actual boundary.
- PDM is the normal fleet surface. Native PVE or PBS access remains the explicit break-glass path when PDM is unavailable; do not deploy a parallel control plane as a workaround.

## Workflow

1. Read the owning repository's current access and fleet references.
2. Confirm the binary exists and record `--version` or package version without changing the host.
3. Build a secret-safe invocation using the endpoint, auth ID, TLS fingerprint, and `--password-command`.
4. Prove authentication with `remote list --output-format json`.
5. Perform read-only discovery before choosing an exact target.
6. For a mutation, record the requested action and pre-state, execute it once, follow any task, and verify post-state.
7. Return concise evidence: PDM endpoint identity, remote, node, guest ID and name when applicable, action, UPID or synchronous result, and final state. Redact credentials.

## Command Reference

Read [references/commands.md](references/commands.md) for installation boundaries, invocation templates, discovery commands, task follow-through, and mutation safeguards. Verify live syntax with `help --verbose` before using a command that is not covered there.
