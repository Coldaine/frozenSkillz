# Evaluation cases

Run these before promotion. Preserve redacted command output or a concise evidence summary in the pull request.

## Trigger routing

The skill should trigger for requests such as:

- "Use PDM to list every VM across the managed Proxmox authorities."
- "Find VM 220 through PDM and report its remote, node, name, and state."
- "Restart this exact guest through PDM and prove the task finished."
- "Why does one Proxmox remote appear unavailable in PDM?"

It should not trigger for:

- "PDM is down; use the documented native PVE recovery path."
- "Install a new Proxmox VE host from ISO."
- "Change the Kubernetes deployment running on this guest."

## Live client evaluation

1. Confirm the operator host is compatible and the installed package came from the selected official PDM repository.
2. Record the package and server versions; require matching major versions.
3. Confirm `help --verbose` exposes the documented connection, JSON, discovery, and task-status options.
4. Authenticate with `--password-command` without exposing the returned password in argv, output, or a file.
5. Run `remote list --output-format json` and parse the result as JSON.
6. Select one PVE remote and run node, resource, QEMU, LXC, and task discovery as applicable.
7. Resolve one guest by remote, node, VMID, and name; prove that VMID alone is not reported as a global identity.
8. Supply a deliberately incorrect TLS fingerprint and prove the client fails closed. Do not alter the trusted pin.
9. If a mutation is explicitly authorized, capture pre-state, submit one exact action, follow its terminal result, and capture post-state. Do not invent an evaluation mutation.

## Pass conditions

- All claimed commands exist in the installed version.
- Read-only output is valid JSON and sufficient to select an exact authority and resource.
- Authentication and certificate failures are classified correctly and reveal no credential.
- No request acceptance, connection loss, or returned task ID is described as successful completion.
- Native PVE or PBS access is described only as break-glass, not as a second standing control plane.
