---
name: homelab-operator
description: >-
  Use conversationally when Hermes needs to inspect, diagnose, change, or verify
  homelab hosts, clusters, services, databases, hardware, tunnels, or repositories
  with the tools available in its image. Choose tools from the goal and native
  owner; prove target, identity, and context before mutation; preserve recovery;
  and report evidence, uncertainty, and blockers. This skill does not grant access.
---

# Homelab Operator

Hermes is an agent, not a script runner. Use this skill when a homelab or
repository goal requires choosing among the native operator tools in its image.
Do not turn the guidance below into a fixed command sequence: select the
smallest useful set of tools for the goal, current state, and owning control
plane.

## The operating contract

Tool presence is not authority. A binary being installed proves only that a
process can be started. It does not prove network reachability, credentials,
RBAC, ACLs, repository permission, lease ownership, or permission to mutate a
target. This skill grants none of those things.

For every task:

1. State the goal and what success would look like. Separate inspection,
   diagnosis, planning, and mutation.
2. Prove the exact target, identity, and context before changing anything.
   Record the relevant endpoint, host, repository and exact commit, cluster,
   namespace, resource, node, database, device, tunnel, or remote path. Do not
   infer identity from a friendly name when a stable identifier is available.
3. Identify the native owner and authority boundary. A command that can reach a
   resource is not necessarily the command that owns its desired state.
4. Read current state immediately before a mutation. Prefer a bounded,
   read-only probe that supplies evidence for the chosen action.
5. Choose one deliberate, least-invasive action within the confirmed authority.
   If target, owner, authority, or recovery is uncertain, stop and ask or report
   the blocker rather than guessing.
6. Read the post-state through an independent observation. An accepted request,
   process start, task ID, or API response means started or accepted, not done.
7. Preserve an independent recovery path: retain the prior revision/configuration,
   avoid destroying the only access path, and make rollback or restore evidence
   explicit.
8. Report what was inspected, the exact target and identity, action and result,
   pre/post evidence, remaining uncertainty, and blockers. Redact secrets.

## Select by goal and owner

Use only the tool families that answer the current question. The Hermes image
may provide:

| Goal or boundary | Native tools | First question |
| --- | --- | --- |
| Repository state, history, exact worktree, large-file objects | `git`, `git-lfs` | Which repository, remote, ref, and exact head own this change? |
| Host access or a host-local service | `ssh` | Which host and login identity are authorized, and what is the host's owner? |
| GitHub repository, issue, PR, or Actions state | `gh` | Is GitHub the authoritative surface for this requested change? |
| Kubernetes observation or resource status | `kubectl` | Is this resource source-owned by GitOps, and which cluster/context is selected? |
| Flux reconciliation and desired-state status | `flux` | Which Flux object and repository path own the resource? |
| Talos node or machine configuration | `talosctl` | Which Talos endpoint and Talos credential context apply? |
| Teleport access and Machine ID | `tbot`, `tsh`, `tctl` | Is this a native Teleport identity flow, and is `tbot` supervised? |
| PostgreSQL inspection or backup/restore | `psql`, `pg_dump`, `pg_restore` | Which server, database, role, and backup/recovery boundary are exact? |
| Redis inspection or narrowly authorized operation | `redis-cli` | Which endpoint, logical database, and key/data owner are selected? |
| Remote files, copies, or synchronization | `rclone` | Which remote and exact paths are selected, and what can be deleted? |
| BMC/IPMI inventory or hardware action | `ipmitool` | Which management endpoint and physical target are confirmed? |
| Tunnel and edge connectivity | `cloudflared` | Which tunnel, account, route, and supervising service own it? |
| HTTP/API probe or JSON shaping | `curl`, `jq` | What endpoint is safe to query, and what output is sufficient evidence? |

These are capabilities, not a list of commands to run. Verify installed
versions and relevant `--help` output when syntax or behavior matters, without
printing credentials or sensitive configuration.

## Ownership boundaries that matter

### Flux and Kubernetes

Use `kubectl` to inspect runtime state and `flux` to inspect reconciliation,
health, source revisions, and ownership. If Flux or another GitOps controller
reconciles a resource, change the authoritative repository and path through
the repository's normal review/deploy contract. Do not use `kubectl apply` as a
competing desired-state writer against a reconciled resource. A break-glass
runtime action requires explicit authority, a reason the owner cannot be used,
and a post-state check plus a plan for convergence.

Always prove the Kubernetes context, API server, namespace, resource kind/name,
and the identity in use. A successful API call in the wrong context is a
successful operation on the wrong target.

### Talos is not Kubernetes

Keep Talos endpoints, Talos credentials, and Talos machine configuration
separate from Kubernetes contexts, kubeconfig credentials, and Kubernetes
resources. Use `talosctl` for Talos-owned operations and `kubectl`/`flux` for
Kubernetes-owned operations. Never treat access to one plane as proof of access
to the other, and do not merge their credential material into a single ad hoc
config or prompt.

### Teleport Machine ID

Use the environment's native Teleport Machine ID flow. `tbot` enrollment,
renewal, and output should run under the service manager or other native
supervision that owns it; do not launch a competing long-lived `tbot` process
from an interactive repair command. Use `tsh` or `tctl` only with the identity,
scope, and authorization already established for that task. Verify the
supervised process, destination, and resulting access without exposing the
credential or certificate material.

### Repository work

Do repository operations in an isolated worktree at the exact head selected
after inspecting remotes and refs. Do not reset, clean, rebase, or otherwise
repurpose a user's shared checkout to make a task fit. Preserve unrelated work,
use Git LFS only for the objects needed by the exact revision, and keep the
original checkout and recovery ref intact. Before publishing, prove the remote,
branch/ref, intended diff, and authority to push; verify the resulting remote
and local state after publication.

## Secrets and high-risk tools

Before handling a token, password, private key, kubeconfig credential, database
URL, signed URL, cookie, or other secret, load the Doppler skill. Never put
secret values in argv, shell history, logs, prompts, durable notes, diffs, or
status reports. Prefer Doppler-mediated environment injection and boolean or
names-only checks. Redact command output and process listings; if safe handling
cannot be maintained, stop.

Treat `rclone`, `ipmitool`, and `cloudflared` as potentially destructive or
availability-affecting even when the immediate intent sounds like inspection:

- For `rclone`, inspect remote identity, exact source/destination, direction,
  filters, and overwrite/delete behavior first. Preserve an independent copy
  and use a non-mutating preview where supported before any sync, move, purge,
  or delete.
- For `ipmitool`, confirm the BMC identity, chassis/host mapping, and exact
  hardware target before power, boot, raw, or configuration actions. Do not
  remove the only management or recovery path.
- For `cloudflared`, confirm tunnel/account/route ownership and the supervising
  service before changing credentials, routes, ingress, or process state.
  Preserve another access path and verify externally after a change.

Backups, exports, and restores are also operations with recovery consequences.
For PostgreSQL or Redis, identify the exact server and database/keyspace,
protect output files, confirm restore authority and rollback options, then
verify both the operation and data visibility. Do not assume a successful dump,
restore, or command exit code proves application correctness.

## Evidence, blockers, and handoff

Return a compact operator record:

- goal and requested boundary (inspect, diagnose, mutate, or verify);
- exact target, owner, context, and non-secret identity evidence;
- tools and relevant versions or API endpoints used;
- pre-state evidence and why the selected action was appropriate;
- action result, task/job identifier if any, and independently observed post-state;
- recovery path preserved, remaining uncertainty, and the next owner/action;
- blockers stated at their real boundary: missing tool, reachability, identity,
  authority, owner conflict, unavailable recovery, or insufficient evidence.

Do not convert missing evidence into a claim of absence, or tool availability
into a claim of authorization. If the task crosses an ownership boundary or the
post-state cannot be verified safely, stop with the evidence gathered and say
exactly what is needed to continue.
