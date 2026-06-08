# Skill Audit — hephastus
**Date:** 2026-06-07

Complete inventory of every LLM agent skill directory found on this machine across all tools.

---

## Summary

| Location | Tool / Context | Skill count |
|---|---|---|
| `~/.claude/skills/` | Claude Code — user | 4 + 1 learned |
| `~\AppData\Roaming\npm\node_modules\oh-my-claude-sisyphus\skills\` | Claude Code — OMC package | 39 |
| `~/.kilo/skills/` | Kilo Code (CLI) | 3 |
| `~/.gemini/antigravity-cli/plugins/Stitch/skills/` | Antigravity CLI | 1 |
| `~/.codex/skills/.system/` | Codex CLI — built-in | 3 |
| `~/.codex/skills/` (user) | Codex CLI — user | 2 + 1 symlink |
| `~/.minimax-agent/projects/.minimax/skills/` | Minimax Agent | 8 |
| `~/.config/goose/skills/` | Goose | 0 (empty) |
| `~/Downloads/KimiClaw/skills/` | KimiClaw | 14 |
| `~/Downloads/skills/` | Downloads — symlinked | 4 symlinks |
| `~/Downloads/skills/downloaded/` | Downloads — downloaded | 7 categories |
| `D:\_projects\coldaine-infra\.claude\skills\` | Project | 3 |
| `D:\_projects\coldaine-infra\skills\frozen\` | Project — frozen snapshot | ~6 |
| `D:\_projects\frozenSkillz\` | **This repo** — active dev | ~10 |
| `D:\_projects\oh-my-openagent\.agents\skills\` | Project | 9 |
| `D:\_projects\oh-my-openagent\.opencode\skills\` | Project — opencode view | 4 |
| `D:\_projects\oh-my-openagent\src\features\builtin-skills\` | Project — builtins | 4 |
| `D:\_projects\ColdReviewer\.agents\skills\` | Project | 7 |
| `D:\_projects\ColdTools\ColdReviewer\.agents\skills\` | Project — duplicate | 7 |
| `D:\_projects\ActuarialKnowledge\.agents\skills\` | Project | 1 |
| `D:\_projects\AgentVisualCrazy\.agents\skills\` | Project | 1 |
| `D:\_projects\llm-archiver\.agents\skills\` | Project | 1 |
| `D:\_projects\IdeaEmergence\.github\skills\` | Project | 1 |
| `D:\_projects\coldaine-ci-source\archive\codebuff\agents\skills\` | Archive | 6 |
| `D:\_projects\hermes-agent\skills\` | Project — large corpus | ~417 md files |

---

## Tool-level skill listings

### Claude Code — user (`~/.claude/skills/`)
- `chat-history`
- `claude-md-enhancer`
- `google-stitch-ui-designer`
- `nlm-skill`
- `omc-learned/phantom-substrate-inheritance` *(learned skill)*

### Claude Code — OMC package (`oh-my-claude-sisyphus`, 39 skills)
ai-slop-cleaner, ask, autopilot, autoresearch, cancel, ccg, configure-notifications, debug, deep-dive, deep-interview, deepinit, external-context, hud, learner, mcp-setup, omc-doctor, omc-reference, omc-setup, omc-teams, plan, project-session-manager, ralph, ralplan, release, remember, sciomc, self-improve, setup, skill, skillify, team, trace, ultragoal, ultraqa, ultrawork, verify, visual-verdict, wiki, writer-memory

### Kilo Code (`~/.kilo/skills/`)
- `agent-md-refactor`
- `google-stitch-ui-designer`
- `grill-me`

### Antigravity CLI (`~/.gemini/antigravity-cli/plugins/Stitch/skills/`)
- `stitch`

### Codex CLI — system (`~/.codex/skills/.system/`)
- `imagegen`
- `openai-docs`
- `plugin-creator`

### Codex CLI — user (`~/.codex/skills/`)
- `codex-primary-runtime`
- `google-stitch-ui-designer`
- `llm-archiver` → symlink to `D:\_projects\coldaine-infra\skills\frozen\plugins\frozen-skills\skills\llm-archiver`

### Minimax Agent (`~/.minimax-agent/projects/.minimax/skills/`)
- `minimax-docx`
- `minimax-pdf`
- `minimax-xlsx`
- `openclaw-doctor`
- `openclaw-install`
- `pocket-init`
- `pptx-generator`
- `windows-env-setup`

### Goose (`~/.config/goose/skills/`)
*Empty — no skills installed.*

### KimiClaw (`~/Downloads/KimiClaw/skills/`)
- `agent-workspace-manager`
- `clean-architecture`
- `deploy-to-vercel`
- `domain-driven-design`
- `filesystem-context`
- `folder-structure-blueprint-generator`
- `ln-646-project-structure-auditor`
- `memory`
- `next-best-practices`
- `project-structure`
- `python-project-structure`
- `scope-appropriate-architecture`
- `vercel-composition-patterns`
- `vercel-react-best-practices`

### Downloads loose skills (`~/Downloads/skills/`)
Symlinks into `~/Downloads/.agents/skills/`:
- `azure-quotas`
- `frontend-design`
- `supabase-postgres-best-practices`
- `vercel-react-best-practices`

Downloaded category dirs (`~/Downloads/skills/downloaded/`):
database, design, devops, pr-review-canvas, productivity, testing, web-dev

---

## Project-level skill listings

### `D:\_projects\coldaine-infra\.claude\skills\`
- `northstar-guardian`
- `plugin-authoring-guide`
- `setup-rules`

### `D:\_projects\coldaine-infra\skills\frozen\plugins\`
*(Snapshot of frozenSkillz incubator as of freeze date)*
- frozen-rules → `setup-rules`
- frozen-skills → `agent-config-megaref`, `gh-common-workflows`, `mcp-deployment-guide`, `plugin-authoring-guide`

### `D:\_projects\frozenSkillz\` — **this repo**
Active (`plugins/`):
- `frozen-skills/skills/doppler`
- `skill-injector/skills/skill-injector`

Incubator (`_incubator/`):
- `frozen-rules/skills/setup-rules`
- `frozen-skills/skills/agent-config-megaref`
- `frozen-skills/skills/gh-common-workflows`
- `frozen-skills/skills/mcp-deployment-guide`
- `frozen-skills/skills/plugin-authoring-guide`
- `frozen-skills/skills/session-skill-inferencer`
- `frozen-skills/skills/stacked-pr-workflow`
- `skill-manager` *(tooling, not a deliverable skill)*

### `D:\_projects\oh-my-openagent` (9 + 4 + 4)
`.agents/skills/`: get-unpublished-changes, github-triage, hyperplan, omomomo, pre-publish-review, publish, remove-deadcode, security-research, work-with-pr

`.opencode/skills/` *(subset)*: github-triage, hyperplan, pre-publish-review, work-with-pr

`src/features/builtin-skills/`: agent-browser, dev-browser, frontend-ui-ux, git-master

### `D:\_projects\ColdReviewer\.agents\skills\` (and identical copy in ColdTools/ColdReviewer)
next-best-practices, next-cache-components, next-upgrade, vercel-composition-patterns, vercel-react-best-practices, vercel-react-native-skills, web-design-guidelines

### One-skill project dirs
| Project | Skill |
|---|---|
| `ActuarialKnowledge/.agents/skills/` | `beads` |
| `AgentVisualCrazy/.agents/skills/` | `align-agent-rules` |
| `llm-archiver/.agents/skills/` | `llm-archiver` |
| `IdeaEmergence/.github/skills/` | `spec-first-delivery` |

### `D:\_projects\coldaine-ci-source\archive\codebuff\agents\skills\`
cleanup, codebuff-agent-factory, refactor-safety, review, review-gate, spec-gap-issue-writer

### `D:\_projects\hermes-agent\skills\` (~417 md files — too large to enumerate)
| Category | Files |
|---|---|
| creative | 259 |
| mlops | 42 |
| research | 21 |
| github | 15 |
| productivity | 15 |
| software-development | 14 |
| media | 7 |
| autonomous-ai-agents | 7 |
| apple | 6 |
| email | 4 |
| gaming | 3 |
| devops | 3 |
| dogfood | 3 |
| red-teaming | 3 |
| mcp | 2 |
| data-science | 2 |
| note-taking | 2 |
| smart-home | 2 |
| social-media | 2 |
| diagramming | 1 |
| domain | 1 |
| gifs | 1 |
| inference-sh | 1 |
| yuanbao | 1 |

---

## Notable observations

- **`google-stitch-ui-designer`** exists independently in 3 tool dirs (`~/.claude/skills/`, `~/.kilo/skills/`, `~/.codex/skills/`) — not symlinked, likely manually copied each time.
- **ColdReviewer skills duplicated** between `D:\_projects\ColdReviewer\.agents\skills\` and `D:\_projects\ColdTools\ColdReviewer\.agents\skills\` — identical 7 skills.
- **`coldaine-infra/skills/frozen`** is a frozen snapshot of content that also lives in `frozenSkillz/_incubator` — two sources of truth for the same skills.
- **`~/.codex/skills/llm-archiver`** is a symlink into coldaine-infra's frozen tree.
- **Opencode** has no user-level skill dir; picks up skills only from project `.opencode/skills/` dirs.
- **Antigravity** has only 1 skill (the Stitch plugin); no user-level skill dir.
- **"QLO"** in conversation = **Kilo Code** (`kilo`/`kilocode` CLI), confirmed installed with 3 skills at `~/.kilo/skills/`.
- **Downloads/01_Projects/SkillReview/** contains 12 skill JSON files — likely exported/candidate skills in a different format from the SKILL.md convention.
