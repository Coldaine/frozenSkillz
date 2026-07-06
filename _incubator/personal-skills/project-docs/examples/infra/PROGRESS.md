---
title: homelab-gitops Progress
date: 2026-06-29
status: living
last_confirmed: 2026-06-29
---

# PROGRESS.md

## Current State

Substrate, cluster, and core platform (GitOps controller, ingress, secrets) are
Current: applied and reconciling. Apps run on top. The repo rebuilds the cluster
from `tofu apply` plus bootstrap.

## Active Work

- Bringing up in-cluster S3 (object store). Manifest drafted under `platform/`; not yet applied, so it stays **Planned** in architecture.md until it reconciles.
- Drafting ADR 0003 (object store choice) before applying.

## Blockers

- ADR 0003 is `proposed`, not `accepted`. Do not apply the object store manifest until the decision is recorded, per the no-undocumented-decisions rule.

## Next Session Focus

- Finalize ADR 0003, apply the object store, then flip its row in architecture.md from Planned to Current in the same commit.
- Start the Postgres operator manifest (still Planned).

## Recently Changed

- Migrated ingress to the gateway controller (now Current).

Roll items older than this handoff window into `docs/history/`.
