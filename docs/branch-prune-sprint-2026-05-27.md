# Branch Prune And PR Landing Sprint - 2026-05-27

## Snapshot

- Repository: `Coldaine/frozenSkillz`
- Default branch: `main`
- Snapshot branch: `codex/prune-and-land-sprint-2026-05-27`
- Snapshot base: `origin/main` at `7b9ea8227eff67ceb48cdcfbdf9b7b238bf6d898`
- Remote HEAD: `refs/heads/main`
- GitHub `deleteBranchOnMerge`: `false`, so branch deletion must be explicit.

## Open PRs At Sprint Start

| PR | Head branch | State | Linked issue | Sprint action |
| --- | --- | --- | --- | --- |
| #10 `Add actual MCP JSON configurations and templates` | `add-mcp-configs-and-templates-11418343221340354973` | `CLEAN`, GitGuardian success | closes #9 | Merge first; delete branch after merge. |
| #11 `Add missing documentation for skill-classifier plugin` | `feature/skill-classifier-docs-17147562101257410825` | `CLEAN`, GitGuardian success | closes #6 | Merge after #10; delete branch after merge. |
| #13 `Cross-platform support for plugins and marketplace` | `feature/cross-platform-manifests-15166907834327009249` | `CLEAN`, GitGuardian success | closes #7 | Merge after #11; delete branch after merge. |
| #14 `Add session-skill-inferencer skill` | `add-session-skill-inferencer` | `CLEAN`, GitGuardian success | none | Merge after manifest conflicts from #10/#11/#13 are checked. |
| #12 `Add Graphite Stacked PR Workflow Skill` | `graphite-skill-addition-10799137259279690414` | `CLEAN`, GitGuardian success | closes #8 | Do not merge as-is; supersede with a neutral stacked-PR workflow branch derived from #15/#12. |
| #15 `feat(skills): add graphite-stacked-pr-workflow skill and bump plugin versions` | `detective/audit-2026-04-05` | `CLEAN`, CodeRabbit/GitGuardian/Kilo success, `size:XXL` | none | Do not merge wholesale; split useful stacked-PR workflow content from archive/tooling bulk. |
| #17 `[codex] Publish Doppler skill` | `codex/add-doppler-skill` | `UNSTABLE`, GitGuardian/CodeRabbit success, Kilo cancelled | none | Fix manifest regression, rebase/update after main advances, then land. |
| #18 `docs: add project README` | `docs/add-readme` | `CLEAN`, CodeRabbit/GitGuardian/Kilo success | none | Refresh and land last so README reflects final surface. |

## Open Issues At Sprint Start

| Issue | Title | Sprint action |
| --- | --- | --- |
| #9 | `Add actual MCP configs (not just guides)` | Let #10 close it. |
| #6 | `skill-classifier missing SKILL.md documentation` | Let #11 close it. |
| #7 | `Marketplace is Claude-only, not cross-platform` | Let #13 close it. |
| #8 | `Uncommitted changes on master - graphite skill addition` | Close after the neutral stacked-PR workflow replacement lands. |
| #4 | `Add subagent prompt quality gate hook` | Keep open; needs user/product decision before implementation. |
| #5 | `Replace Gemini Flash backend with faster lightweight LLM` | Keep open; needs backend decision before implementation. |

## Branch Prune Decisions

| Branch | Tip | Evidence | Action |
| --- | --- | --- | --- |
| `origin/main` | `7b9ea8227eff67ceb48cdcfbdf9b7b238bf6d898` | Default branch. | Keep. |
| `master` local | `7b9ea82` | Tracks missing `origin/master`; same commit as `origin/main`. | Delete local branch after sprint worktrees no longer need it. |
| `origin/feature/cross-project-skills-and-rules` | `b04bc2ed54979583a614e6e9515140e00d6e8dee` | Ancestor of `main`; PR #1 was merged. | Delete remote branch. |
| `origin/fix/broken-paths` | `f9dfc9a020b3456837498e97b3132eb4d54f5520` | PR #2 was closed unmerged; diff targets obsolete `.claude/settings.json` and root `skill_classifier.py`. | Delete remote branch after recording this rationale. |
| `origin/claude/add-vercel-agents-7o6gh` | `a00e3746dc095a9f21297fdadccbc690318b3a31` | No open PR; large reference/example import not linked to an active issue. | Delete remote branch unless a final PR/issue check discovers a live dependency. |
| Open PR branches | See PR table. | Branches still back open PRs. | Keep until each PR is merged or closed, then delete. |
| Checked-out branches | `detective/audit-2026-04-05`, `codex/add-doppler-skill` | Active worktrees exist. | Do not delete until worktrees are removed or branches are no longer checked out. |

## Verification Gates

- Before any merge: `gh pr view <n> --json mergeStateStatus,statusCheckRollup,reviewDecision,closingIssuesReferences`.
- After each merge: refresh `origin/main`, re-check the next PR's merge state, and parse touched JSON manifests with `ConvertFrom-Json`.
- For skill-manager or policy changes: run `plugins/skill-manager/scripts/skills-state.ps1 inventory`, `plan`, and `skills-audit.ps1`.
- Before completion: `git diff --check`, open PR/issue list, remote branch list, and local worktree status.
