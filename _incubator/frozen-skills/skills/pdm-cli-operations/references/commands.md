# Official PDM client commands

The authoritative references are the Proxmox Datacenter Manager
[client description](https://pdm.proxmox.com/docs/sysadmin.html#proxmox-datacenter-manager-client),
[command syntax](https://pdm.proxmox.com/docs/command-syntax.html#proxmox-datacenter-manager-client),
and [package repository instructions](https://pdm.proxmox.com/docs/installation.html#debian-package-repositories).

## Installation boundary

The executable is `proxmox-datacenter-manager-client`. First check:

```sh
command -v proxmox-datacenter-manager-client
dpkg-query -W -f='${Package} ${Version}\n' proxmox-datacenter-manager-client
```

Install it only on a compatible Debian operator host from an official Proxmox PDM repository. Use the repository channel selected for that environment and the official signed keyring; do not silently enable `pdm-test`. Install only the client package, not a PDM server meta-package. Record the installed package version and confirm its major version matches the PDM server.

## Invocation template

The official client accepts `--host`, `--port`, `--user`, `--fingerprint`, `--password-command`, and `--output-format` as inherited options. Keep the password command itself non-secret:

```sh
proxmox-datacenter-manager-client remote list \
  --host '<pdm-host>' \
  --port 8443 \
  --user '<auth-id>' \
  --fingerprint '<sha256-fingerprint>' \
  --password-command '<secret-manager command that writes only the password>' \
  --output-format json
```

Do not use `--password-file` unless the owning environment explicitly requires and protects a short-lived file. Do not use an inline password.

## Read-only discovery

```sh
proxmox-datacenter-manager-client remote list [CONNECTION OPTIONS] --output-format json
proxmox-datacenter-manager-client pve node list <remote> [CONNECTION OPTIONS] --output-format json
proxmox-datacenter-manager-client pve resources <remote> [vm|storage|node|sdn] [CONNECTION OPTIONS] --output-format json
proxmox-datacenter-manager-client pve qemu list <remote> [CONNECTION OPTIONS] --output-format json
proxmox-datacenter-manager-client pve lxc list <remote> [CONNECTION OPTIONS] --output-format json
proxmox-datacenter-manager-client pve qemu config <remote> <vmid> [CONNECTION OPTIONS] --output-format json
proxmox-datacenter-manager-client pve lxc config <remote> <vmid> [CONNECTION OPTIONS] --output-format json
proxmox-datacenter-manager-client pve task list <remote> [CONNECTION OPTIONS] --output-format json
proxmox-datacenter-manager-client pbs datastore list <remote> [CONNECTION OPTIONS] --output-format json
proxmox-datacenter-manager-client pbs snapshot list <remote> <datastore> [CONNECTION OPTIONS] --output-format json
proxmox-datacenter-manager-client pbs task list <remote> [CONNECTION OPTIONS] --output-format json
```

`[CONNECTION OPTIONS]` is notation, not literal CLI text. Use `help --verbose` to confirm commands and flags against the installed version.

## Mutations and tasks

The client supports guest start, shutdown, stop, migration, snapshot, and rollback commands for PVE resources. Select the graceful lifecycle command when it satisfies the request; abrupt `stop` is not a synonym for `shutdown`.

Before execution:

1. Re-read the exact guest config and current resource state.
2. Confirm remote, node, VMID, and guest name together.
3. Confirm the requested action and its expected impact.
4. Identify the native PVE or PBS recovery path if failure could strand the target.

After execution, retain the returned UPID when present and query the matching task family:

```sh
proxmox-datacenter-manager-client pve task status <remote> <upid> [CONNECTION OPTIONS] --output-format json
proxmox-datacenter-manager-client pbs task status <remote> <upid> [CONNECTION OPTIONS] --output-format json
```

Poll at a bounded interval until the task is terminal, or until the authorized execution window expires. A timeout is an unknown outcome: re-read task and resource state before retrying. Never submit the same mutation merely because the client connection dropped.

## Failure routing

| Evidence | Boundary | Next action |
|---|---|---|
| Binary absent or incompatible major version | Operator host | Correct the official client installation; do not modify PDM |
| TLS pin mismatch | Trust boundary | Stop and independently verify certificate rotation |
| Authentication rejected | PDM identity | Stop and repair the scoped credential or role |
| PDM endpoint unreachable | PDM or management network | Use documented native PVE/PBS break-glass access only if the task requires it |
| PDM reachable, one remote unavailable | Remote authority | Diagnose that remote through its native path |
| Task reaches an unsuccessful terminal result | Target operation | Preserve UPID and error evidence; do not report completion |
