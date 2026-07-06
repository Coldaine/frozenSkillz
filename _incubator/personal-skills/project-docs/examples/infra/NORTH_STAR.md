---
title: homelab-gitops North Star
date: 2026-06-29
author: (owner)
status: living
last_confirmed: 2026-06-29
---

# homelab-gitops North Star

## The Bet

A single-operator Kubernetes homelab stays maintainable only if the cluster's
desired state lives entirely in this repo and is reconciled by GitOps, so that
"what the repo says" and "what the cluster runs" are the same fact, recoverable
from `git clone` plus one bootstrap.

## In / Out / Shape

- **In:** declarative manifests and IaC for the substrate, the platform, and the apps
- **Out:** a cluster whose running state is reproducible from this repo alone
- **Shape:** a GitOps monorepo (`tofu/` → `talos/` → `platform/` → `apps/`), reconciled by a controller in-cluster
- **Operator:** one person plus coding agents, not a team with a change-advisory board

## Goals

- **G1.** Every change to the cluster is a commit; nothing is configured by hand on a live node.
- **G2.** The repo is recoverable: a bare-metal rebuild is `tofu apply` then bootstrap, no snowflake state.
- **G3.** Decisions that shape the cluster (storage, ingress, secrets, database) are recorded as ADRs, not folklore.

## Anti-Goals

- **A1.** Not a multi-tenant production platform. No SLAs, no on-call rotation, no change board.
- **A2.** Not click-ops. If a fix is applied with `kubectl edit` and not committed, it does not exist and will be reconciled away.
- **A3.** Not a place to vendor every CNCF project. Capabilities are added when an app needs them, not speculatively.

## Pillars

- **P1. Reconciled, not pushed.** The repo is the source of truth; a controller converges the cluster to it. Cost: a change is not "done" until it is committed and reconciled, which is slower than a hotfix.
- **P2. Layered substrate-up.** `tofu` (VMs) under `talos` (Kubernetes) under `platform` (core services) under `apps`. Cost: cross-layer changes touch several directories and an ADR.
- **P3. Manifests are the documentation of state.** Prose docs explain intent and decisions; the manifests are the truth of what runs. Cost: prose must never restate manifest detail, or it drifts.
