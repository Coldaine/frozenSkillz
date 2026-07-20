# Official PDM client commands

The authoritative references are the Proxmox Datacenter Manager
[client description](https://pdm.proxmox.com/docs/sysadmin.html#proxmox-datacenter-manager-client),
[command syntax](https://pdm.proxmox.com/docs/command-syntax.html#proxmox-datacenter-manager-client),
and [package repository instructions](https://pdm.proxmox.com/docs/installation.html#debian-package-repositories).

## Contents

- [Installation boundary](#installation-boundary)
- [Environment launcher](#environment-launcher)
- [Raw client login](#raw-client-login)
- [Authority](#authority)
- [Discovery and evidence](#discovery-and-evidence)
- [Guest lifecycle and snapshots](#guest-lifecycle-and-snapshots)
- [Migration](#migration)
- [Task completion](#task-completion)
- [Failure routing](#failure-routing)

## Installation boundary

The executable is `proxmox-datacenter-manager-client`. First check:

```sh
command -v proxmox-datacenter-manager-client
dpkg-query -W -f='${Package} ${Version}\n' proxmox-datacenter-manager-client
```

Install it only on a compatible Debian amd64 operator host from an official Proxmox PDM repository. Use the repository channel selected for that environment and the official signed keyring; do not silently enable `pdm-test`. Install only the client package, not a PDM server meta-package. Record the installed package version and confirm its major version matches the PDM server.

Proxmox does not publish a native Windows build. On Windows, use the bundled PowerShell bridge to an environment-owned Linux runner that already exposes the official client. Do not add WSL or a local container solely for this skill.

## Environment launcher

Prefer an environment launcher such as `hermes-pdm` when the owning repository provides one:

```sh
hermes-pdm --output-format json remote list
hermes-pdm --output-format json resources
```

The launcher contract is:

- retrieve the environment-selected identity without printing its credential;
- retain the official client's persistent ticket cache separately from other identities;
- seed only an independently verified TLS fingerprint;
- invoke `proxmox-datacenter-manager-client` exactly once for the requested command;
- preserve stdout, stderr, and the client exit code; and
- impose no hidden read-only policy on an identity whose declared role is execution.

On Windows, set the SSH runner and call the bundled bridge:

```powershell
$env:PDM_CLI_SSH_TARGET = 'operator@pdm-client-runner'
& "$HOME/.agents/skills/pdm-cli-operations/scripts/pdm.ps1" --output-format json remote list
```

`PDM_CLI_REMOTE_PROGRAM` defaults to `hermes-pdm` and may name another single executable or absolute POSIX path. The bridge rejects option-like SSH targets and shell syntax in the remote program.

## Raw client login

Global connection options precede the subcommand. Ordinary commands load a cached ticket; they do not use a supplied password to log in automatically.

```sh
export XDG_CONFIG_HOME='<protected-state>/config'
export XDG_CACHE_HOME='<protected-state>/cache'
install -d -m 0700 "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME/proxmox-datacenter-client"
printf '%s %s\n' '<pdm-host>' '<sha256-hex-without-colons>' \
  > "$XDG_CACHE_HOME/proxmox-datacenter-client/fingerprints"

proxmox-datacenter-manager-client \
  --host '<pdm-host>' \
  --port 8443 \
  --user '<user-id>' \
  --password-command '<secret-manager command that writes only the password>' \
  login

proxmox-datacenter-manager-client \
  --host '<pdm-host>' \
  --port 8443 \
  --user '<user-id>' \
  --output-format json \
  remote list
```

For 1.1.6, `--fingerprint` parses but noninteractive `login` does not insert it into the verifier cache. The cache line is `<host> <64 SHA-256 hex characters>`; derive it only from an independently verified colon-delimited fingerprint. Stop on mismatch. Remove this workaround only after a newer installed client proves `--fingerprint` works.

Do not use `--password-file` unless the owning environment creates it with mode `0600`, deletes it on every exit path, and never places it on a shared or committed filesystem. PDM API token IDs are not accepted by the 1.1.6 CLI `--user` schema.

## Authority

PDM 1.1.6 has built-in `NoAccess`, `Auditor`, and `Administrator` roles; it cannot create a custom role. `Auditor` is an inspection role. A mutation requires `Administrator` on the applicable path, normally scoped to the relevant `/resource` subtree, plus sufficient permissions in the backing remote credential. The environment owns the identity and ACL choice; the skill must not substitute a different identity or turn an execution role into inspection-only behavior.

## Discovery and evidence

`<pdm>` below means the environment launcher or the raw client plus its global connection options.

```sh
<pdm> --output-format json remote list
<pdm> --output-format json resources
<pdm> --output-format json pve node list <remote>
<pdm> --output-format json pve resources <remote> [vm|storage|node|sdn]
<pdm> --output-format json pve qemu list <remote> [--node <node>]
<pdm> --output-format json pve lxc list <remote> [--node <node>]
<pdm> --output-format json pve qemu config <remote> <vmid> --node <node> --state active
<pdm> --output-format json pve lxc config <remote> <vmid> --node <node> --state active
<pdm> --output-format json pve task list <remote>
<pdm> --output-format json pbs datastore list <remote>
<pdm> --output-format json pbs snapshot list <remote> <datastore>
<pdm> --output-format json pbs task list <remote>
```

In 1.1.6 the fleet command is `resources`, not `resources list`. Guest configuration defaults to pending state, so specify `--state active` for current configuration evidence. Runtime state comes from the guest list or `pve resources`, not the configuration response.

## Guest lifecycle and snapshots

Read current guest state and active configuration immediately before execution. Confirm remote, node, VMID, and guest name together. Prefer graceful `shutdown`; `stop` is abrupt.

```sh
# QEMU lifecycle
<pdm> --output-format json pve qemu start <remote> <vmid> --node <node>
<pdm> --output-format json pve qemu shutdown <remote> <vmid> --node <node>
<pdm> --output-format json pve qemu stop <remote> <vmid> --node <node>

# LXC lifecycle
<pdm> --output-format json pve lxc start <remote> <vmid> --node <node>
<pdm> --output-format json pve lxc shutdown <remote> <vmid> --node <node>
<pdm> --output-format json pve lxc stop <remote> <vmid> --node <node>

# QEMU snapshots
<pdm> --output-format json pve qemu snapshot list <remote> <vmid> --node <node>
<pdm> --output-format json pve qemu snapshot create <remote> <vmid> <snapname> --node <node> [--description <text>] [--vmstate <boolean>]
<pdm> --output-format json pve qemu snapshot delete <remote> <vmid> <snapname> --node <node>
<pdm> --output-format json pve qemu snapshot rollback <remote> <vmid> <snapname> --node <node> [--start <boolean>]

# LXC snapshots
<pdm> --output-format json pve lxc snapshot list <remote> <vmid> --node <node>
<pdm> --output-format json pve lxc snapshot create <remote> <vmid> <snapname> --node <node> [--description <text>]
<pdm> --output-format json pve lxc snapshot delete <remote> <vmid> <snapname> --node <node>
<pdm> --output-format json pve lxc snapshot rollback <remote> <vmid> <snapname> --node <node> [--start <boolean>]
```

Rollback is destructive. For rollback, abrupt stop, or another action that can materially strand a workload, identify the native recovery path before execution.

## Migration

Same-remote migration uses a target node. Live 1.1.6 help incorrectly labels `<target>` as a remote ID even though the command is a same-cluster node migration.

```sh
# QEMU, same remote
<pdm> --output-format json pve qemu migrate <remote> <vmid> <target-node> \
  --node <source-node> [--online <boolean>] [--force <boolean>] \
  [--with-local-disks <boolean>] [--map-storage FROM:TO,...] \
  [--bwlimit <KiB/s>] [--migration-network <CIDR>] \
  [--migration-type secure|insecure]

# LXC, same remote
<pdm> --output-format json pve lxc migrate <remote> <vmid> <target-node> \
  --node <source-node> [--online <boolean>] [--restart <boolean>] \
  [--timeout <seconds>] [--map-storage FROM:TO,...] [--bwlimit <KiB/s>]
```

Cross-remote migration requires explicit bridge and storage mappings. Begin qualification with a stopped disposable guest, an unused target VMID, and `--delete false`.

```sh
# QEMU, cross remote
<pdm> --output-format json pve qemu remote-migrate \
  <source-remote> <vmid> <target-remote> \
  --map-bridge FROM:TO,... --map-storage FROM:TO,... \
  [--node <source-node>] [--target-vmid <vmid>] \
  [--online <boolean>] [--delete <boolean>] [--bwlimit <KiB/s>]

# LXC, cross remote
<pdm> --output-format json pve lxc remote-migrate \
  <source-remote> <vmid> <target-remote> \
  --map-bridge FROM:TO,... --map-storage FROM:TO,... \
  [--node <source-node>] [--target-vmid <vmid>] \
  [--online <boolean>] [--restart <boolean>] [--timeout <seconds>] \
  [--delete <boolean>] [--bwlimit <KiB/s>]
```

Do not use insecure migration merely for convenience. Capture storage, network, source, target, and deletion semantics before submission.

## Task completion

PDM client 1.1.6 automatically waited for the live-tested snapshot create and delete operations. Despite `--output-format json`, it emitted a wrapped UPID followed by a non-JSON terminal `TaskStatus`. Require `status: Stopped` and `exitstatus: Some("OK")`, then verify resource state.

When only a UPID is returned, use the complete remote-prefixed identifier such as `pve:<remote>!UPID:...`; passing only the inner `UPID:...` produced `bad remote id in remote upid` in 1.1.6.

```sh
<pdm> --output-format json pve task status <remote> '<pve:remote!UPID:...>'
<pdm> --output-format json pbs task status <remote> '<pbs:remote!UPID:...>'
```

Poll at a bounded interval while `status` is `running`. Success requires `status=stopped` and `exitstatus=OK`; missing or non-`OK` exit status is unsuccessful or indeterminate. A timeout, transport loss, malformed response, or missing task is an unknown outcome. Re-query the same task and current resource state before considering a retry. The 1.1.6 CLI exposes task status but not the PDM task-log endpoint.

## Failure routing

| Evidence | Boundary | Next action |
|---|---|---|
| Binary absent or incompatible major version | Operator host | Correct the official client installation; do not modify PDM |
| TLS pin mismatch or login certificate failure | Trust boundary | Stop and independently verify the presented certificate |
| Authentication rejected | PDM identity | Repair the environment-selected credential |
| Inspection succeeds but mutation is unauthorized | PDM or backing-remote ACL | Correct the declared executor role; do not redefine the task as read-only |
| Ordinary command is unauthorized after a password option | Client session | Run explicit `login` with the same persistent XDG cache |
| PDM endpoint unreachable | PDM or management network | Use documented native PVE/PBS access only when the task requires break-glass work |
| PDM reachable but one remote is unavailable | Remote authority | Diagnose that remote through its native path |
| Task stops with non-`OK` exit status | Target operation | Preserve the wrapped UPID and error evidence; do not report completion |
