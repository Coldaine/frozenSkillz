# architecture.md

## Architecture Thesis

homelab-gitops is a layered, reconciled Kubernetes homelab. OpenTofu provisions
the VM substrate on Proxmox; Talos Linux turns those VMs into a Kubernetes
cluster; a platform layer installs the shared services (ingress, secrets,
storage, database operator); apps run on top. A GitOps controller reconciles the
repo into the cluster, so the repo is the desired state and the cluster is the
observed state.

## Status Legend

- **Current** — applied to the live cluster (reconciled / present in cluster or remote state).
- **Planned** — decided direction, manifest may exist, not yet applied.
- **Candidate** — plausible option, not decided.
- **Deferred** — intentionally not being built now.

Note: status is about *applied*, not *authored*. A manifest committed to the
tree but not yet reconciled is **Planned**, not Current.

## System Shape

| Area | Status | Approach |
|---|---|---|
| Substrate (`tofu/`) | Current | OpenTofu provisions Proxmox VMs and the Talos boot media |
| Kubernetes (`talos/`) | Current | Talos Linux, declarative machine config, 1 control plane + 2 workers |
| GitOps controller (`platform/`) | Current | Reconciles `platform/` and `apps/` from this repo |
| Ingress + TLS (`platform/`) | Current | Gateway controller with automatic certificates |
| Secrets (`platform/`) | Current | External secrets operator backed by an out-of-cluster store |
| In-cluster S3 (`platform/`) | Planned | Object store for backups and app blobs; manifest drafted, not applied |
| Postgres operator (`platform/`) | Planned | Operator-managed Postgres for stateful apps |
| Offsite backup target | Candidate | Replicate object store to a remote bucket; not decided |
| Service mesh | Deferred | No app needs mTLS or traffic-splitting yet |

## Major Components

| Component | Status | Responsibility | Detail |
|---|---|---|---|
| `tofu/` | Current | VM substrate and boot media | `docs/components/substrate.md` |
| `talos/` | Current | Cluster machine config and bootstrap | `docs/components/talos.md` |
| `platform/` | Current | Shared cluster services | `docs/components/platform.md` |
| `apps/` | Current | Workloads | `docs/components/apps.md` |

## Architectural Invariants

- **Manifests only in implementation directories.** `tofu/`, `talos/`, `platform/`, and `apps/` hold IaC and manifests, never prose docs. Prevents the tree from accreting stale READMEs that drift from the manifests. Documentation lives in the doc homes; a one-line pointer is the only allowed doc file in an implementation directory.
- **No hand-edited live state.** Changes land as commits and are reconciled. Prevents the cluster from diverging into a snowflake the repo can no longer rebuild.
- **Layer order holds.** A layer depends only on the layers below it (`apps` may assume `platform`, never the reverse). Prevents bootstrap cycles.

## ADR Index

| ADR | Status | Summary |
|---|---|---|
| `docs/decisions/0001-talos-over-kubeadm.md` | accepted | Talos for immutable, declarative nodes |
| `docs/decisions/0002-gitops-reconciler.md` | accepted | Reconcile the repo in-cluster rather than push from CI |
| `docs/decisions/0003-in-cluster-s3.md` | proposed | Object store choice for backups and app blobs |

## Open Architecture Questions

- Do we replicate the object store offsite once total stored data exceeds a set threshold, or accept local-only backups?
- Does the Postgres operator own backups, or does the object store layer?

## Links

- Intent and anti-goals: `NORTH_STAR.md`
- Current work: GitHub Issues and/or `docs/plans/`
- Decisions: `docs/decisions/`
