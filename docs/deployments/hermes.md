# Hermes

Hermes is a standing service that consumes reviewed skills from this repository. It is a **runtime**, not a client: it has no packaging format and no plugin manifest, so it is not part of the `--consumer` enum. See [`../workflows/skill-authority-and-frozen-sync.md`](../workflows/skill-authority-and-frozen-sync.md) → **Skill Consumer Shapes**.

## How it consumes skills

The deploy script lives in `Coldaine/coldaine-homelab` at `deployments/hermes/sync-frozen-skills.sh` and runs as root. It:

1. clones or updates this repository at `/srv/hermes/repos/frozenSkillz`;
2. materializes the skill set into `/srv/hermes/skill-sets/hermes-ops`; and
3. exposes that directory to the `hermes` container at `/opt/frozen-skills` as a read-only external skill directory.

Hermes reads bare `SKILL.md` directories from that path. Nothing renders a client package for it.

It consumes exactly `doppler` and `pdm-cli-operations`, expressed as the consumer-less `hermes-ops` deployment in `plugins/distribution.json`.

## Invocation

```sh
python3 scripts/sync_frozen_skills.py --check --deployment hermes-ops --destination /srv/hermes/skill-sets/hermes-ops --prune
python3 scripts/sync_frozen_skills.py --apply --deployment hermes-ops --destination /srv/hermes/skill-sets/hermes-ops --prune
```

`--destination` and `--prune` are mandatory for a deployment. Passing `--consumer` alongside `--deployment hermes-ops` is an error: the deployment declares no consumer because Hermes is not a client.

## Pin status

The pin rule itself is in [`../workflows/skill-authority-and-frozen-sync.md`](../workflows/skill-authority-and-frozen-sync.md) → **Pinning From a Production Consumer**. Hermes enforces it mechanically: the deploy script refuses to proceed unless its pinned commit is reachable from a fetched `refs/remotes/origin` ref, exiting 69 otherwise. The consumer checked this before the repository wrote the rule down.

Current pin `da5ae4eeb4acf9470e84dfa7877663c7d666a734` is reachable from exactly one ref, `origin/fix/validate-skill-frontmatter` — an unmerged branch whose pull request (#44) is closed. Repointing it is an edit in `coldaine-homelab` and is blocked until deployment support lands on `main`.
