# Skill State Dry Run

Generated: 2026-05-19T14:35:58.3086494-05:00

This report is dry-run only. It records observed state and proposed changes; it does not prove that any live client config was changed.

## Summary

- `claude`: 4 entries; enabled=0 disabled=0
- `codex`: 5 entries; enabled=0 disabled=0
- `codex-plugin-cache`: 104 entries; enabled=0 disabled=0
- `frozen-archived`: 24 entries; enabled=0 disabled=0
- `frozen-published`: 7 entries; enabled=0 disabled=0
- `gemini`: 12 entries; enabled=2 disabled=10
- `shared-agents`: 14 entries; enabled=0 disabled=0

## Proposed Dry-Run Actions

- **broken-reference** `codex-config` `box`: would-remove-stale-reference - Configured skill path does not exist. `C:\\Users\\pmacl\\.codex\\plugins\\cache\\openai-curated\\box\\314574a046f21938025ae443f9c6dbbd0c2c9b7a\\skills\\box\\SKILL.md`
- **broken-reference** `codex-config` `develop-web-game`: would-remove-stale-reference - Configured skill path does not exist. `C:\\Users\\pmacl\\.codex\\skills\\develop-web-game\\SKILL.md`
- **broken-reference** `codex-config` `slides`: would-remove-stale-reference - Configured skill path does not exist. `C:\\Users\\pmacl\\.codex\\skills\\codex-primary-runtime\\slides\\SKILL.md`
- **broken-reference** `codex-config` `spreadsheets`: would-remove-stale-reference - Configured skill path does not exist. `C:\\Users\\pmacl\\.codex\\skills\\codex-primary-runtime\\spreadsheets\\SKILL.md`
- **broken-reference** `codex-config` `vercel-agent`: would-remove-stale-reference - Configured skill path does not exist. `C:\\Users\\pmacl\\.codex\\plugins\\cache\\openai-curated\\vercel\\314574a046f21938025ae443f9c6dbbd0c2c9b7a\\skills\\vercel-agent\\SKILL.md`
- **broken-reference** `codex-config` `vercel-api`: would-remove-stale-reference - Configured skill path does not exist. `C:\\Users\\pmacl\\.codex\\plugins\\cache\\openai-curated\\vercel\\314574a046f21938025ae443f9c6dbbd0c2c9b7a\\skills\\vercel-api\\SKILL.md`
- **broken-reference** `codex-config` `vercel-cli`: would-remove-stale-reference - Configured skill path does not exist. `C:\\Users\\pmacl\\.codex\\plugins\\cache\\openai-curated\\vercel\\314574a046f21938025ae443f9c6dbbd0c2c9b7a\\skills\\vercel-cli\\SKILL.md`
- **broken-reference** `codex-config` `vercel-firewall`: would-remove-stale-reference - Configured skill path does not exist. `C:\\Users\\pmacl\\.codex\\plugins\\cache\\openai-curated\\vercel\\314574a046f21938025ae443f9c6dbbd0c2c9b7a\\skills\\vercel-firewall\\SKILL.md`
- **broken-reference** `codex-config` `vercel-flags`: would-remove-stale-reference - Configured skill path does not exist. `C:\\Users\\pmacl\\.codex\\plugins\\cache\\openai-curated\\vercel\\314574a046f21938025ae443f9c6dbbd0c2c9b7a\\skills\\vercel-flags\\SKILL.md`
- **broken-reference** `codex-config` `vercel-functions`: would-remove-stale-reference - Configured skill path does not exist. `C:\\Users\\pmacl\\.codex\\plugins\\cache\\openai-curated\\vercel\\314574a046f21938025ae443f9c6dbbd0c2c9b7a\\skills\\vercel-functions\\SKILL.md`
- **broken-reference** `codex-config` `vercel-queues`: would-remove-stale-reference - Configured skill path does not exist. `C:\\Users\\pmacl\\.codex\\plugins\\cache\\openai-curated\\vercel\\314574a046f21938025ae443f9c6dbbd0c2c9b7a\\skills\\vercel-queues\\SKILL.md`
- **broken-reference** `codex-config` `vercel-sandbox`: would-remove-stale-reference - Configured skill path does not exist. `C:\\Users\\pmacl\\.codex\\plugins\\cache\\openai-curated\\vercel\\314574a046f21938025ae443f9c6dbbd0c2c9b7a\\skills\\vercel-sandbox\\SKILL.md`
- **broken-reference** `codex-config` `vercel-services`: would-remove-stale-reference - Configured skill path does not exist. `C:\\Users\\pmacl\\.codex\\plugins\\cache\\openai-curated\\vercel\\314574a046f21938025ae443f9c6dbbd0c2c9b7a\\skills\\vercel-services\\SKILL.md`
- **broken-reference** `codex-config` `vercel-storage`: would-remove-stale-reference - Configured skill path does not exist. `C:\\Users\\pmacl\\.codex\\plugins\\cache\\openai-curated\\vercel\\314574a046f21938025ae443f9c6dbbd0c2c9b7a\\skills\\vercel-storage\\SKILL.md`
- **broken-reference** `codex-config` `workflow`: would-remove-stale-reference - Configured skill path does not exist. `C:\\Users\\pmacl\\.codex\\plugins\\cache\\openai-curated\\vercel\\314574a046f21938025ae443f9c6dbbd0c2c9b7a\\skills\\workflow\\SKILL.md`
- **drift** `gemini` `insight-extractor`: would-disable - Gemini enabled state differs from policy enabled_only list. `C:\Users\pmacl\.agents\skills\insight-extractor`
- **duplicate** `multi` `chat-history`: would-review-duplicates - Same declared skill appears in multiple source types: shared-agents, runtime-local, repo-archived. `C:\Users\pmacl\.agents\skills\chat-history; C:\Users\pmacl\.claude\skills\chat-history; D:\_projects\frozenSkillz\removed-needs-rework\2026-05-19-agents-skills-corpus-review\skills\chat-history`
- **duplicate** `multi` `Codex-md-enhancer`: would-review-duplicates - Same declared skill appears in multiple source types: shared-agents, repo-archived. `C:\Users\pmacl\.agents\skills\claude-md-enhancer; D:\_projects\frozenSkillz\removed-needs-rework\2026-05-19-agents-skills-corpus-review\skills\claude-md-enhancer`
- **duplicate** `multi` `doc-retrospective`: would-review-duplicates - Same declared skill appears in multiple source types: shared-agents, repo-archived. `C:\Users\pmacl\.agents\skills\review-claudemd; D:\_projects\frozenSkillz\removed-needs-rework\2026-05-19-agents-skills-corpus-review\skills\review-claudemd; D:\_projects\frozenSkillz\removed-needs-rework\2026-05-19-client-skill-cleanup\claude-local-skills-removed\review-claudemd`
- **duplicate** `multi` `google-stitch-ui-designer`: would-review-duplicates - Same declared skill appears in multiple source types: shared-agents, runtime-local, repo-archived. `C:\Users\pmacl\.agents\skills\google-stitch-ui-designer; C:\Users\pmacl\.claude\skills\google-stitch-ui-designer; C:\Users\pmacl\.codex\skills\google-stitch-ui-designer; D:\_projects\frozenSkillz\removed-needs-rework\2026-05-19-agents-skills-corpus-review\skills\google-stitch-ui-designer`
- **duplicate** `multi` `insight-extractor`: would-review-duplicates - Same declared skill appears in multiple source types: shared-agents, repo-archived. `C:\Users\pmacl\.agents\skills\insight-extractor; D:\_projects\frozenSkillz\removed-needs-rework\2026-05-19-agents-skills-corpus-review\skills\insight-extractor; D:\_projects\frozenSkillz\removed-needs-rework\2026-05-19-client-skill-cleanup\claude-local-skills-removed\insight-extractor`
- **duplicate** `multi` `pr-review-dashboard`: would-review-duplicates - Same declared skill appears in multiple source types: shared-agents, repo-archived. `C:\Users\pmacl\.agents\skills\pr-review-dashboard; D:\_projects\frozenSkillz\removed-needs-rework\2026-05-19-agents-skills-corpus-review\skills\pr-review-dashboard`
- **duplicate** `multi` `pr-triage`: would-review-duplicates - Same declared skill appears in multiple source types: shared-agents, repo-archived. `C:\Users\pmacl\.agents\skills\pr-triage; D:\_projects\frozenSkillz\removed-needs-rework\2026-05-19-agents-skills-corpus-review\skills\pr-triage`
- **duplicate** `multi` `pr-visual-summary`: would-review-duplicates - Same declared skill appears in multiple source types: shared-agents, repo-archived. `C:\Users\pmacl\.agents\skills\pr-visual-summary; D:\_projects\frozenSkillz\removed-needs-rework\2026-05-19-agents-skills-corpus-review\skills\pr-visual-summary`
- **duplicate** `multi` `retrospective`: would-review-duplicates - Same declared skill appears in multiple source types: shared-agents, repo-archived. `C:\Users\pmacl\.agents\skills\retrospective; D:\_projects\frozenSkillz\removed-needs-rework\2026-05-19-agents-skills-corpus-review\skills\retrospective; D:\_projects\frozenSkillz\removed-needs-rework\2026-05-19-client-skill-cleanup\claude-local-skills-removed\retrospective`
- **duplicate** `multi` `review-repo-docs`: would-review-duplicates - Same declared skill appears in multiple source types: shared-agents, repo-archived. `C:\Users\pmacl\.agents\skills\review-repo-docs; D:\_projects\frozenSkillz\removed-needs-rework\2026-05-19-agents-skills-corpus-review\skills\review-repo-docs; D:\_projects\frozenSkillz\removed-needs-rework\2026-05-19-client-skill-cleanup\claude-local-skills-removed\review-repo-docs`
- **duplicate** `multi` `skill-finder`: would-review-duplicates - Same declared skill appears in multiple source types: shared-agents, repo-archived. `C:\Users\pmacl\.agents\skills\skill-finder; D:\_projects\frozenSkillz\removed-needs-rework\2026-05-19-agents-skills-corpus-review\skills\skill-finder`
- **review** `shared-agents` `chat-history`: would-mark-review - Shared .agents skill is not listed as an allowed shared skill. `C:\Users\pmacl\.agents\skills\chat-history`
- **review** `shared-agents` `Codex-md-enhancer`: would-mark-review - Shared .agents skill is not listed as an allowed shared skill. `C:\Users\pmacl\.agents\skills\claude-md-enhancer`
- **review** `shared-agents` `doc-retrospective`: would-mark-review - Shared .agents skill is not listed as an allowed shared skill. `C:\Users\pmacl\.agents\skills\review-claudemd`
- **review** `shared-agents` `google-stitch-ui-designer`: would-mark-review - Shared .agents skill is not listed as an allowed shared skill. `C:\Users\pmacl\.agents\skills\google-stitch-ui-designer`
- **review** `shared-agents` `insight-extractor`: would-mark-review - Shared .agents skill is not listed as an allowed shared skill. `C:\Users\pmacl\.agents\skills\insight-extractor`
- **review** `shared-agents` `pr-review-dashboard`: would-mark-review - Shared .agents skill is not listed as an allowed shared skill. `C:\Users\pmacl\.agents\skills\pr-review-dashboard`
- **review** `shared-agents` `pr-triage`: would-mark-review - Shared .agents skill is not listed as an allowed shared skill. `C:\Users\pmacl\.agents\skills\pr-triage`
- **review** `shared-agents` `pr-visual-summary`: would-mark-review - Shared .agents skill is not listed as an allowed shared skill. `C:\Users\pmacl\.agents\skills\pr-visual-summary`
- **review** `shared-agents` `retrospective`: would-mark-review - Shared .agents skill is not listed as an allowed shared skill. `C:\Users\pmacl\.agents\skills\retrospective`
- **review** `shared-agents` `review-repo-docs`: would-mark-review - Shared .agents skill is not listed as an allowed shared skill. `C:\Users\pmacl\.agents\skills\review-repo-docs`

## Config References

- `codex-config`: exists= enabled=False `spreadsheets:Spreadsheets`
- `codex-config`: exists= enabled=False `vercel:ai-generation-persistence`
- `codex-config`: exists= enabled=False `vercel:ai-sdk`
- `codex-config`: exists= enabled=False `vercel:bootstrap`
- `codex-config`: exists= enabled=False `vercel:cms`
- `codex-config`: exists= enabled=False `vercel:cron-jobs`
- `codex-config`: exists=True enabled=False `C:\\Users\\pmacl\\.agents\\skills\\pr-review-dashboard\\SKILL.md`
- `codex-config`: exists=True enabled=False `C:\\Users\\pmacl\\.agents\\skills\\pr-triage\\SKILL.md`
- `codex-config`: exists=True enabled=False `C:\\Users\\pmacl\\.agents\\skills\\pr-visual-summary\\SKILL.md`
- `codex-config`: exists=False enabled=False `C:\\Users\\pmacl\\.codex\\plugins\\cache\\openai-curated\\box\\314574a046f21938025ae443f9c6dbbd0c2c9b7a\\skills\\box\\SKILL.md`
- `codex-config`: exists=False enabled=False `C:\\Users\\pmacl\\.codex\\plugins\\cache\\openai-curated\\vercel\\314574a046f21938025ae443f9c6dbbd0c2c9b7a\\skills\\vercel-agent\\SKILL.md`
- `codex-config`: exists=False enabled=False `C:\\Users\\pmacl\\.codex\\plugins\\cache\\openai-curated\\vercel\\314574a046f21938025ae443f9c6dbbd0c2c9b7a\\skills\\vercel-api\\SKILL.md`
- `codex-config`: exists=False enabled=False `C:\\Users\\pmacl\\.codex\\plugins\\cache\\openai-curated\\vercel\\314574a046f21938025ae443f9c6dbbd0c2c9b7a\\skills\\vercel-cli\\SKILL.md`
- `codex-config`: exists=False enabled=False `C:\\Users\\pmacl\\.codex\\plugins\\cache\\openai-curated\\vercel\\314574a046f21938025ae443f9c6dbbd0c2c9b7a\\skills\\vercel-firewall\\SKILL.md`
- `codex-config`: exists=False enabled=False `C:\\Users\\pmacl\\.codex\\plugins\\cache\\openai-curated\\vercel\\314574a046f21938025ae443f9c6dbbd0c2c9b7a\\skills\\vercel-flags\\SKILL.md`
- `codex-config`: exists=False enabled=False `C:\\Users\\pmacl\\.codex\\plugins\\cache\\openai-curated\\vercel\\314574a046f21938025ae443f9c6dbbd0c2c9b7a\\skills\\vercel-functions\\SKILL.md`
- `codex-config`: exists=False enabled=False `C:\\Users\\pmacl\\.codex\\plugins\\cache\\openai-curated\\vercel\\314574a046f21938025ae443f9c6dbbd0c2c9b7a\\skills\\vercel-queues\\SKILL.md`
- `codex-config`: exists=False enabled=False `C:\\Users\\pmacl\\.codex\\plugins\\cache\\openai-curated\\vercel\\314574a046f21938025ae443f9c6dbbd0c2c9b7a\\skills\\vercel-sandbox\\SKILL.md`
- `codex-config`: exists=False enabled=False `C:\\Users\\pmacl\\.codex\\plugins\\cache\\openai-curated\\vercel\\314574a046f21938025ae443f9c6dbbd0c2c9b7a\\skills\\vercel-services\\SKILL.md`
- `codex-config`: exists=False enabled=False `C:\\Users\\pmacl\\.codex\\plugins\\cache\\openai-curated\\vercel\\314574a046f21938025ae443f9c6dbbd0c2c9b7a\\skills\\vercel-storage\\SKILL.md`
- `codex-config`: exists=False enabled=False `C:\\Users\\pmacl\\.codex\\plugins\\cache\\openai-curated\\vercel\\314574a046f21938025ae443f9c6dbbd0c2c9b7a\\skills\\workflow\\SKILL.md`
- `codex-config`: exists=False enabled=False `C:\\Users\\pmacl\\.codex\\skills\\codex-primary-runtime\\slides\\SKILL.md`
- `codex-config`: exists=False enabled=False `C:\\Users\\pmacl\\.codex\\skills\\codex-primary-runtime\\spreadsheets\\SKILL.md`
- `codex-config`: exists=False enabled=False `C:\\Users\\pmacl\\.codex\\skills\\develop-web-game\\SKILL.md`
- `codex-config`: exists=True enabled=False `C:\\Users\\pmacl\\.codex\\skills\\google-stitch-ui-designer\\SKILL.md`
