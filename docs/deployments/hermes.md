# Hermes

Hermes is a standing service that consumes reviewed skills from this repository. It is a **runtime**, not a client: it has no packaging format and no plugin manifest, so it is not part of the `--consumer` enum. See [`../workflows/skill-authority-and-frozen-sync.md`](../workflows/skill-authority-and-frozen-sync.md) → **Skill Consumer Shapes**.

## How it consumes skills

The deploy script lives in `Coldaine/coldaine-homelab` at `deployments/hermes/sync-frozen-skills.sh` and runs as root. It:

1. clones or updates this repository at `/srv/hermes/repos/frozenSkillz`;
2. materializes the skill set into `/srv/hermes/skill-sets/hermes-ops`; and
3. exposes that directory to the `hermes` container at `/opt/frozen-skills` as a read-only external skill directory.

Hermes reads bare `SKILL.md` directories from that path. Nothing renders a client package for it.

The post-promotion `hermes-ops` profile is defined to consume exactly `doppler`, `pdm-cli-operations`, and `homelab-operator` in `plugins/distribution.json`. `homelab-operator` provides conversational guidance for selecting and safely using the native homelab/repository tools; it does not grant access or provision those tools. The currently deployed homelab pin remains older until the homelab deployment is explicitly updated and synchronized.

## Tool ownership

Tool installation and Hermes image composition are owned by the homelab
repository and deployment, not by frozenSkillz. This document records the
skill-consumption contract; it does not claim that tools or live provisioning
are present or have been performed. Hermes may use a tool only when the image,
runtime identity, network reachability, and native authorization prove that it
is available for the requested operation.

## Invocation

```sh
python3 scripts/sync_frozen_skills.py --check --deployment hermes-ops --destination /srv/hermes/skill-sets/hermes-ops --prune
python3 scripts/sync_frozen_skills.py --apply --deployment hermes-ops --destination /srv/hermes/skill-sets/hermes-ops --prune
```

`--destination` and `--prune` are mandatory for a deployment. Passing `--consumer` alongside `--deployment hermes-ops` is an error: the deployment declares no consumer because Hermes is not a client.

## Pin status

The pin rule itself is in [`../workflows/skill-authority-and-frozen-sync.md`](../workflows/skill-authority-and-frozen-sync.md) → **Pinning From a Production Consumer**. Hermes enforces it mechanically: the deploy script refuses to proceed unless its pinned commit is reachable from a fetched `refs/remotes/origin` ref, exiting 69 otherwise. The consumer checked this before the repository wrote the rule down.

Current pin `da5ae4eeb4acf9470e84dfa7877663c7d666a734` is reachable from exactly one ref, `origin/fix/validate-skill-frontmatter` — an unmerged branch whose pull request (#44) is closed. Repointing it is an edit in `coldaine-homelab`; until that happens, this promotion is not live in Hermes. This frozenSkillz change does not claim that live Hermes provisioning or synchronization has occurred.
