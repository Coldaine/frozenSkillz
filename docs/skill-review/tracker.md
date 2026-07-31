# Skill Tracker

Active skills live under `plugins/` and are listed in `plugins/distribution.json`; gated
skills live in `_incubator/` and are not installable. Promotion = move the skill into a
package, register it in `distribution.json`, reconcile the marketplace manifests, bump the
version. Quality bar = the `doppler` skill: clear trigger description (~300 chars), verified
content, scripts actually run, no project-specific leakage, progressive disclosure.

## Marketplace lane

| Skill | Status | Next action |
|---|---|---|
| `doppler` | active | None — reference standard. |
| `external-skill-intake` | active | None. |
| `omc-reference` | active | None. |
| `pdm-cli-operations` | active | None — live-qualified 2026-07-20. |
| `codex-thread-organizer` | active | Codex-only dedicated package. |
| `skill-injector` | registered, dormant/untested | Qualify end-to-end or de-register; internal rename from skill-classifier unfinished. |
| `plugin-authoring-guide` | gated | Rework; re-verify against current Claude Code docs. |
| `mcp-deployment-guide` | gated | Re-verify config paths + `mcp/` templates at repo root. |
| `agent-config-megaref` | gated | Light update; reconcile against `D:\_projects\llm-archiver` (canonical for per-tool config paths). |
| `setup-rules` | gated | Remove the uncertain "claude rules list" line; verify install flow. |
| `gh-common-workflows` | gated | Strip NORTH_STAR/Codex-specific assumptions. |
| `stacked-pr-workflow` | gated | Run the 7 PowerShell helpers or cut it. |
| `skill-manager` | gated | Verify `skills.sh` registry assumptions or cut it. |
| `session-skill-inferencer` | gated | Produced junk auto-skills in May; fix generation quality or cut. |
| `icepanel-api` | gated | Closest to ready: live-validate diagram push, diff hand-transcribed schemas against live OpenAPI, trim description to ~300 chars. |

## Personal lane

Gated reference copies of `~/.agents/skills` — never marketplace candidates unless
de-personalized.

| Skill | Next action |
|---|---|
| `chat-history` | De-personalize paths; fix `while read` missing `-r` in extract-chats.sh; drop unimplemented gemini extractor from docstring. |
| `retrospective` | De-personalize. |
| `project-docs` | Gated pending de-personalization. |
| `skill-install` | Verify recipes. |
| `run-opencode` | Fix driver.mjs header comment re: profile writes. |
| `edit-opencode-config` | Fix canonical-root drift. |
| `phantom-substrate-inheritance` | Review. |
| `review-claudemd` | Fix frontmatter name mismatch + duplicate find clause; overlap-check vs `claude-md-enhancer`. |
| `rich-visual-responses` | Review — corpus analysis says cosmetic effect only. |
| `insight-extractor` | Add YAML frontmatter; fix contradictory `~/.Codex` vs `~/.claude` paths. |
| `claude-md-enhancer` | Confirm provenance. |
| `nlm-skill` | Confirm provenance. |
| `skill-finder` | Confirm provenance. |
| `google-stitch-ui-designer` | Confirm provenance. |
| `context7-mcp` | Likely redundant with `~/.claude/rules/context7.md` — decide keep/drop. |
| `patrickspowerfulpresentations` | Incubating; stays personal. |
| `audio-producer` | Incubating; stays personal. Broadside examples are worked evidence — keep. |

## Intake queue

Helmfile/Kubernetes adopt shortlist (2026-07-21):

- helmfile/helmfile — mine the diff/doctor and intentional-apply language only.
- LukasNiessen/kubernetes-skill — take the core workflow (prove-before-mutate).
- Author a thin `k8s-platform-operator` glue skill, seeded from the ionos
  cluster-api-provider-proxmox AGENTS.md.

Parked / do not adopt: Flux-based skills — wrong reconciler.

## Fleet effectiveness review

Corpus analysis of ~7,300 sessions across all agents (2026-07-28; instrument and full
findings live in `D:\_projects\agent-control-plane` — `projects/agent-ceremony-*.md`,
`tools/ceremony_metrics.py`). Rerun the scorecard after any intervention below and record
the verdict change here. Verdicts:

- **Superpowers pack is the codex-ceremony driver.** Codex is the heaviest skill user
  (60% of sessions read SKILL.md files via shell — untagged, so earlier counts missed it),
  and its top reads are the superpowers pack in `~/.codex/plugins/cache/`:
  `using-superpowers` (622 sessions), `verification-before-completion` (306 — the
  "Iron Law" evidence register). Lever: operational-mode override in `~/.codex/AGENTS.md`
  (**not yet applied**) or prune the skill from the cache.
- **Net-negative:** `git-master` (opencode; 5× failure signals, −27 health — slim it),
  `shared/ulw-plan` (22× loop in one session), `issue-pr-review` (killed 2026-07-28),
  `code-review` (7× edit churn).
- **Earning their keep:** `doppler`, `project-docs`, `chat-history` (content good; trigger
  breadth was the problem — narrowing **not yet applied**), `parallel-web-search`, `canvas`,
  `create-hook`.
- **Cruft:** `rich-visual-responses` (cosmetic), `context7-mcp` (counts inflated by
  meta-review sessions), 46% of all skills fired exactly once, ~10 re-implementations of
  the same planning skill (ralplan/hyperplan/ulw-plan/ultragoal) — consolidate.

## Loose ends

- Root `README.md`/`CLAUDE.md` still describe the pre-gate lineup and the old
  `skill-classifier` name.
- `mcp/` templates at repo root belong to `mcp-deployment-guide`.
- `docs/stacked-pr-workflow/` supplementary docs belong to `stacked-pr-workflow`.
