---
name: pdm-cli-operations
description: Inspect and operate Proxmox VE and PBS fleets through the official PDM client or an environment-owned wrapper. Use for inventory, guest lifecycle, tasks, metrics, snapshots, migration, and PDM troubleshooting; not native PVE/PBS break-glass work.
---

# PDM CLI Operations

Use `proxmox-datacenter-manager-client` as the shared process interface for agents and operators. An environment may expose a small launcher around that binary for credential retrieval and TLS pinning. It connects to the standing PDM API; it is not another service, database, MCP server, or source of truth.

The official client currently requires a compatible amd64 Debian environment, network access to a same-major PDM server, and a secret-safe credential command.

## Operating Contract

- Load `$doppler` before handling authentication in a Doppler-backed environment; otherwise load the applicable secrets-management skill.
- Resolve the PDM endpoint, TLS fingerprint, non-secret auth ID, and target names from the environment's canonical operational repository. Never copy that inventory into this skill.
- Use the identity supplied by the environment. A read-only identity is suitable for inspection or qualification, not for an authorized execution task; do not silently downgrade the requested operation.
- Verify the client and PDM share the same major version before relying on it.
- Prefer the environment-owned launcher when one exists. It must still invoke the official client and preserve its output and exit code.
- The raw client requires `login` before ordinary commands; persist its XDG ticket cache. Pass the password only to `login` through `--password-command` or a protected short-lived `--password-file`.
- Never place a password in argv, a committed file, a prompt, or durable output.
- Pin the expected TLS certificate and never suppress verification. PDM client 1.1.6 does not seed its verifier cache from `--fingerprint` during noninteractive login; use the independently verified cache-pin procedure in the reference or a launcher that implements it.
- Request `--output-format json` for agent work. Preserve the original output when evidence matters; client 1.1.6 emits a non-JSON terminal `TaskStatus` for some mutations even when JSON was requested.
- Start with `remote list`, then select the exact remote, node, and guest. A VMID is not globally meaningful without its remote.
- Read current state immediately before a mutation. Stay within the task's authority while diagnosing and resolving proven dependencies needed to complete it.
- Treat an accepted request or returned UPID as started, not completed. Require terminal `stopped` plus `exitstatus=OK`, then read state again.
- Distinguish client/authentication failure, PDM unavailability, remote unavailability, and an unsuccessful remote task. Report the actual boundary.
- PDM is the normal fleet surface. Native PVE or PBS access remains the explicit break-glass path when PDM is unavailable; do not deploy a parallel control plane as a workaround.

## Workflow

1. Read the owning repository's current access and fleet references.
2. Confirm the binary exists and record `--version` or package version without changing the host.
3. Select the environment launcher or build the two-step raw-client login using the endpoint, user ID, TLS pin, persistent XDG state, and a secret-safe password source.
4. Prove authentication with `remote list` and JSON output.
5. Read pre-state and select the exact remote, node, resource ID, and name.
6. For a mutation, confirm the supplied identity has the necessary authority, execute the exact action once, follow its task to success or failure, and verify post-state.
7. Return concise evidence: PDM endpoint identity, remote, node, guest ID and name when applicable, action, UPID or synchronous result, and final state. Redact credentials.

## Command Reference

Read [references/commands.md](references/commands.md) for installation boundaries, invocation templates, discovery commands, task follow-through, and mutation safeguards. Verify live syntax with `help --verbose` before using a command that is not covered there.
