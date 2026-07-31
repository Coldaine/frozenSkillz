# Skill Tracker

Active skills live under `plugins/` and are listed in `plugins/distribution.json`; gated
skills live in `_incubator/` and are not installable. Promotion = move the skill into a
package, register it in `plugins/distribution.json`, reconcile the marketplace manifests, bump the
version (authority model: `docs/workflows/skill-authority-and-frozen-sync.md`). Quality bar = the `doppler` skill: clear trigger description (~300 chars), verified
content, scripts actually run, no project-specific leakage, progressive disclosure.

## Marketplace lane

| Skill | Status | Next action |
|---|---|---|
| `doppler` | active | None — reference standard. |
| `external-skill-intake` | active | None. |
| `omc-reference` | active | None. |
| `pdm-cli-operations` | active | None — live-qualified 2026-07-20. |
| `codex-thread-organizer` | active | Codex-only dedicated package; direct-rename contract (invocation = authorization; proposal gate removed 2026-07-31). |
| `skill-injector` | registered, dormant/untested | Qualify end-to-end or de-register; internal rename from skill-classifier unfinished. |
| `plugin-authoring-guide` | gated | Rework; re-verify against current Claude Code docs. |
| `mcp-deployment-guide` | gated | Re-verify config paths + `mcp/` templates at repo root. |
| `agent-config-megaref` | gated | Light update; reconcile against `D:\_projects\llm-archiver` (canonical for per-tool config paths). |
| `setup-rules` | gated | Remove the uncertain "claude rules list" line; verify install flow. |
| `gh-common-workflows` | gated | Strip NORTH_STAR/Codex-specific assumptions. |
| `stacked-pr-workflow` | gated | Run the 7 PowerShell helpers or cut it. |
| `skill-manager` | gated | Verify `skills.sh` registry assumptions or cut it. |
| `session-skill-inferencer` | gated | Produced junk auto-skills in May; fix generation quality or cut. |
| `icepanel-api` | gated | Closest to ready: live-validate diagram push, diff hand-transcribed schemas against live OpenAPI, trim description to ~300 chars, rebalance content per owner (less phase-gate execution, more creativity). |

## Personal lane

Gated reference copies of `~/.agents/skills` — never marketplace candidates unless
de-personalized.

| Skill | Next action |
|---|---|
| `chat-history` | De-personalize paths; drop unimplemented gemini extractor from docstring. |
| `retrospective` | Live skill half-deleted ~Jul 16 (SKILL.md gone, scripts/ orphaned) — restore deliberately or delete; then de-personalize. |
| `project-docs` | Gated pending de-personalization. |
| `skill-install` | Verify recipes. |
| `run-opencode` | Fix driver.mjs header comment re: profile writes. |
| `edit-opencode-config` | Fix canonical-root drift. |
| `phantom-substrate-inheritance` | Review. |
| `review-claudemd` | Fix frontmatter name mismatch + duplicate find clause; overlap-check vs `claude-md-enhancer`. |
| `rich-visual-responses` | Keep — regraded 2026-07-31: formatting applied in 23/44 firing sessions vs 2/127 baseline. |
| `insight-extractor` | Add YAML frontmatter; fix contradictory `~/.Codex` vs `~/.claude` paths. |
| `claude-md-enhancer` | Confirm provenance. |
| `nlm-skill` | Confirm provenance. |
| `skill-finder` | Confirm provenance. |
| `google-stitch-ui-designer` | Confirm provenance. |
| `context7-mcp` | Keep but narrow trigger (27/39 fires never call the MCP); add quota-fallback line. |
| `patrickspowerfulpresentations` | Incubating; stays personal. |
| `audio-producer` | Incubating; stays personal. Broadside examples are worked evidence — keep. |

## Intake queue

Kubernetes adopt shortlist (premise corrected 2026-07-23 — coldaine-homelab
reconciles via Flux, not Helmfile; re-scored in
[coldaine-homelab#92](https://github.com/Coldaine/coldaine-homelab/issues/92),
closed 2026-07-25). Every external repo below goes through
`external-skill-intake` before anything is mined or adapted:

- `fluxcd/agent-skills` — adopt-pinned.
- `gitops-cluster-debug` — fork, not adopt raw (hard-requires
  `flux-operator-mcp`/`FluxInstance`; homelab runs plain `flux bootstrap`).
- `kstack` — vendor selectively (ask-before-every-mutation default and 15-minute
  cache don't fit a convergence loop).
- LukasNiessen/kubernetes-skill — take the core workflow (prove-before-mutate).
- Author a thin `k8s-platform-operator` glue skill, seeded from the
  [ionos cluster-api-provider-proxmox AGENTS.md](https://github.com/ionos-cloud/cluster-api-provider-proxmox/blob/main/AGENTS.md);
  implement authored-vs-applied against Flux Kustomizations/HelmReleases, not Helmfile.

Parked regardless of reconciler: whole Aidas dump; kubectl-MCP packs;
clouddrove/Jeffallan/sickn33/wshobson mutate cookbooks; Omni-as-CAPMOX;
kagent apply-after-generate (revisit after CAPI/CAPMOX/Flux is stable).

## Fleet effectiveness review

How grading works: a skill's grade comes from subagents reading transcripts around recent
fires — (1) did the guidance visibly shape the agent's actions, (2) was the owner's next
message acceptance or a correction, and (3) did the session end with an owner-visible
outcome — the owner's *closing* reaction is the ground truth, and self-written tests
passing is not an outcome. AgentsView `health_score` is only a thrash detector
(tool failures / edit churn; 85% of all sessions grade A) — never a success measure. A
"fire" is usually just a SKILL.md read, so editing or studying a skill counts as usage.

**2026-07-28 corpus analysis** (~7,300 sessions; instrument lives in the local
`agent-control-plane` learnings repo — `projects/agent-ceremony-*.md`,
`tools/ceremony_metrics.py`, `tools/classified.csv` = all 308 skills classified.
Machine-local evidence: the verdicts below are the durable record, the corpus is
not rerunnable from this repository):

- **Superpowers pack is the codex-ceremony driver.** Codex is the heaviest skill user
  (60% of sessions read SKILL.md via shell — untagged, so earlier counts missed it); top
  reads are `~/.codex/plugins/cache/` superpowers: `using-superpowers` (622 sessions),
  `verification-before-completion` (306 — the "Iron Law" register). Lever applied
  2026-07-30: operational-mode override in `~/.codex/AGENTS.md`, PR self-review loop
  scoped to substantial changes. If codex still preaches iron laws in ~2 weeks, prune the
  skill from the cache.
- `doppler`, `project-docs`, `chat-history` (trigger narrowed to forensic-only
  2026-07-30), `parallel-web-search`, `canvas`, `create-hook` earn their keep.
- `git-master`: an `oh-my-openagent` built-in, opencode-only — not Codex. Dead since
  Jul 1 (opencode lane fading); its bad numbers came from long thrashy sessions in a
  harness no longer used, and the shipped version has since been rewritten. Ignore.
- `issue-pr-review` zombie fixed 2026-07-30: cursor kept loading it from `_disabled`
  *inside* the discovery root. Quarantine is now `~/.agents/skills-disabled/` (outside
  every scan root) — use it for all future kills.
- Long tail: 46% of all skills fired exactly once; ~10 re-implementations of the same
  planning skill (ralplan/hyperplan/ulw-plan/ultragoal) — consolidate.

**2026-07-31 transcript regrade** of the live 30-day roster (12 skills × 3 recent
sessions each, read by subagents):

- **EARNS:** `babysit` (note: never user-invoked — cursor auto-fires it on "land the
  PRs"-type prompts), `create-skill`, `skill-install`,
  `external-skill-intake`; `rich-visual-responses` — prior "cosmetic cruft" verdict
  **refuted** (23/44 firing sessions apply its formatting vs 2/127 baseline, zero owner
  complaints); `context7-mcp` when used — prior "meta-inflated" verdict **refuted**, real
  doc pulls shaped work, but 27/39 fires load-and-never-use and the service was
  quota-blocked in 10+ sessions → narrow trigger, add quota-fallback line;
  `hangar-logbook` — keep, but revise persistence to markdown-first (owner asked
  verbatim 2026-07-27; it still writes into `.ts` files).
- **IGNORED:** `feature-research` — its sole prescriptive step ran 0 times across all
  examined sessions; pure context tax. **Disabled 2026-07-31** (moved to quarantine).
- **META-ONLY:** `icepanel-api` — recent fires are self-study/rewrite; fold in the
  owner's creativity-vs-phase-gates complaint before promotion.
- **INSUFFICIENT DATA:** `unity` — old "sole mutator" text caused the 2026-07-21 blowup;
  rewritten text unproven, re-grade after a real Editor session. `retrospective` — live
  skill half-deleted ~Jul 16 (SKILL.md gone, `scripts/` orphaned): restore deliberately
  or delete the remnant.
- **Owner-overturned (2026-07-31): `unity-editor-ops` EARNS → NOT PROVEN.** The graded
  "success" session was a 100-tick /loop that ran with Unity/MCP down almost the whole
  time; the batch-mode recipe let it keep generating self-written, self-graded green work
  ("196/196 passed") while nothing owner-visible changed. Owner in-session: "you can
  barely even see the ships"; closing message: "I feel like we never really made any
  progress did we?" Rubric fix baked in below: skill compliance ≠ session success — every
  grade must include an outcome check (owner's closing reaction + something owner-visible
  changed), and self-written tests passing is not an outcome.

## Loose ends

- `mcp/` templates at repo root belong to `mcp-deployment-guide`.
- `docs/stacked-pr-workflow/` supplementary docs belong to `stacked-pr-workflow`.
