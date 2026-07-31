# Platform Direction

**Current path (adopted 2026-07-31):** [REFINED-V1.md](REFINED-V1.md) — persist
and manage agent configuration with three surfaces and nothing else:

```text
frozenSkillz Git          project Git                 each machine
─────────────────         ──────────────────          ──────────────────
reviewed reusable         committed native            runtime / secrets
skills + manifests        agent config for            + managed skill copies
+ incubator mirrors       THAT repo                   from sync script
```

**Operator workflow:** [../workflows/project-agent-config.md](../workflows/project-agent-config.md)
— commit the native files each project's clients actually read.

**Skill sync:** [../workflows/skill-authority-and-frozen-sync.md](../workflows/skill-authority-and-frozen-sync.md)
— reviewed skills flow to `~/.agents/skills` via `scripts/sync_frozen_skills.py`.

## Non-goals (v1 is done without these)

Obot/observation sinks, `machine.yaml`, `frozenctl`, a managed MCP proxy, a
five-client conformance matrix, cross-repo update automation, a GHCR skill
catalog, or any required project meta-manifest (`.agents/config.yaml`).
Reversing any of these requires explicitly reopening the corresponding RV1
decision in REFINED-V1 — do not reintroduce them incrementally.

## Where the July 16 planning pack went

The full control-plane evidence pack (`evidence/`, 14 files) and the three phase
plans (`plans/01–03`) were deliberately removed from `main` on 2026-07-31: they
described a system REFINED-V1 rejects, and their bulk re-anchored agents on
control-plane thinking. They remain permanently available in git history —
[PR #49](https://github.com/Coldaine/frozenSkillz/pull/49), last present at
commit `069aeea`. Recover them from there if a deferred decision (managed
proxy, observation transport, root security) is ever genuinely reopened.

Repository authority is routed by the root `AGENTS.md`; nothing in this
directory overrides the tracker, workflows, or manifests.
