# Chat-history recovery tooling implementation plan

> Execute this plan completely in `agent/chat-history-recovery-tooling`; do not stop at a design checkpoint.

## Goal

Make `frozenSkillz` the explicit upstream skill authority, promote `chat-history`, add deterministic recovery and outward deployment tooling, document the flow with a rendered README image, validate it, and publish a reviewed pull request.

## Tasks

1. Add failing `unittest` fixtures for parent/child collapse, event/index exclusion, cutoff state, and deployment direction.
2. Promote `_incubator/personal-skills/chat-history` to `plugins/frozen-skills/skills/chat-history` and rewrite the skill around deterministic-first recovery.
3. Implement `conversation_inventory.py` with Codex, Claude Code, and Antigravity adapters; normalized root/child records; coverage reporting; and Markdown/JSON output.
4. Add a provenance-pinned LLM Archiver source registry snapshot plus snapshot generation/drift verification helpers.
5. Add an outward-only deployment/check tool that copies from the repository skill to client roots and refuses reverse synchronization.
6. Rewrite `AGENTS.md`, README, the authority workflow, and tracker. Add Mermaid source and a rendered SVG showing repository-to-runtime flow.
7. Register `chat-history` in all four plugin manifests and align plugin/marketplace versions and descriptions.
8. Run unit tests, sample live inventory, manifest validation, JSON parsing, help/smoke commands, `git diff --check`, and a secret scan.
9. Commit meaningful units, push the branch, open a non-draft PR, self-review the diff, inspect checks/comments/review threads, and address valid findings.
