# Skill Authority and Outward Deployment

`frozenSkillz` is the durable upstream authoring, review, test, version, and release boundary for the skills it publishes.

## Authority model

The authoritative tree for a published skill is:

```text
plugins/frozen-skills/skills/<skill-name>/
```

Client roots are downstream runtime surfaces:

| Client surface | Role |
|---|---|
| `~/.agents/skills` | Shared runtime installation root. |
| `~/.claude/skills` | Claude Code runtime/compatibility surface. |
| `~/.codex/skills` | Codex runtime/system surface. |
| `~/.cursor/skills`, `~/.gemini/skills`, `~/.kilo/skills` | Tool-specific installed outputs. |
| `_incubator/` | In-repo gated candidates; neither runtime state nor published authority. |

Do not make a local runtime copy the source of a published change. If runtime experience reveals an improvement, reproduce the change in a repository branch, explain why, test it, review it, and deploy the resulting repository tree outward.

## Outward deployment

Check an installed shared copy against the authoritative repository tree:

```powershell
python scripts/deploy_frozen_skill.py chat-history --target-root "$HOME\.agents\skills" --check
```

Deploy a missing or already-matching copy:

```powershell
python scripts/deploy_frozen_skill.py chat-history --target-root "$HOME\.agents\skills"
```

If the destination differs, the command stops. Inspect the delta; preserve any local-only work separately; then use `--force` only when the repository copy is confirmed as the desired replacement. The tool refuses destinations inside the repository skill tree and refuses reverse direction.

## Promotion and publication

Gated skills live under `_incubator/`. Promotion means:

1. Meet the bar in `docs/skill-review/tracker.md`.
2. Move the reviewed skill to `plugins/frozen-skills/skills/`.
3. Add it to all four plugin manifests.
4. Align plugin and marketplace versions/descriptions.
5. Run the skill’s tests and repository manifest checks.
6. Publish from the reviewed repository commit.

## Verification-only feedback

Installed clients may report:

- source commit/version;
- matching or drifted file hashes;
- load success or failure;
- client-specific compatibility failures.

Those reports flow back to the repository as evidence. Installed file contents do not become authority merely because they are newer or live.

## Required checks

```powershell
python -m unittest discover -s tests -v
python scripts/validate_manifests.py
python scripts/verify_llm_archiver_registry.py
git diff --check
```

When manifests change, parse every changed JSON file and verify every `skills[].path` exists.

## Reporting

Every release/deployment change should state:

- repository source path and commit;
- destination roots checked or updated;
- whether drift was found and how it was resolved;
- tests and manifest checks run;
- why the source change was made.
