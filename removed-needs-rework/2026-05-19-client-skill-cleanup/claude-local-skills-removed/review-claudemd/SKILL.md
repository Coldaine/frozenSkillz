---
name: doc-retrospective
description: Generalized retrospective improvement of project documentation using AI conversation history and web research.
---

# Doc Retrospective

Analyze AI CLI conversation history to improve project documentation with web-researched best practices.

## Step 1: Discover documentation files

Find all documentation files in the project:

```bash
find . -maxdepth 3 \( -name "*.md" -o -name "CLAUDE.md" -o -name "AGENTS.md" -o -name "README*" -o -name "docs" -type d \) -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null | head -50
```

Common files to check:
- `./CLAUDE.md` - Claude Code project instructions
- `./AGENTS.md` - OpenClaw/通用 agent instructions  
- `./README.md` - Project overview
- `./docs/` - Documentation directory
- `~/.claude/CLAUDE.md` - Global Claude settings
- `~/.claude/AGENTS.md` - Global agent settings

## Step 2: Discover AI CLI histories

Find conversation histories from multiple AI CLI tools:

```bash
# Claude Code
CLAUDE_DIR="$HOME/.claude/projects"
# Codex CLI  
CODEX_DIR="$HOME/.codex"
# Gemini CLI
GEMINI_DIR="$HOME/.gemini"
# OpenClaw
OPENCLAW_DIR="$HOME/.openclaw"

# Find project folder (path with slashes replaced by dashes)
PROJECT_PATH=$(pwd | sed 's|/|-|g' | sed 's|^-||')

echo "=== Claude Code ===" && ls -lt "$CLAUDE_DIR/-${PROJECT_PATH}"/*.jsonl 2>/dev/null | head -10
echo "=== Codex ===" && ls -lt "$CODEX_DIR/history/"* 2>/dev/null | head -10
echo "=== Gemini ===" && ls -lt "$GEMINI_DIR/"*.json 2>/dev/null | head -10
echo "=== OpenClaw ===" && ls -lt "$OPENCLAW_DIR/history/"* 2>/dev/null | head -10
```

## Step 3: Detect tech stack

```bash
# Look for project config files to identify tech stack
ls *.json *.toml *.yaml *.yml Gemfile Podfile Package.swift 2>/dev/null | head -10
cat package.json Cargo.toml Gemfile Podfile 2>/dev/null | head -30
```

## Step 4: Extract conversations

```bash
SCRATCH=/tmp/doc-retro-$(date +%s)
mkdir -p "$SCRATCH"

# Extract Claude Code conversations
for f in $(ls -t "$CLAUDE_DIR/-${PROJECT_PATH}"/*.jsonl 2>/dev/null | head -20); do
  basename=$(basename "$f" .jsonl)
  cat "$f" | jq -r '
    if .type == "user" then
      "USER: " + (.message.content // "")
    elif .type == "assistant" then
      "ASSISTANT: " + ((.message.content // []) | map(select(.type == "text") | .text) | join("\n"))
    else empty end
  ' 2>/dev/null | grep -v "^ASSISTANT: $" > "$SCRATCH/$(basename)-claude.txt"
done

# Extract Codex conversations
for f in $(ls -t "$CODEX_DIR/history/"*.md 2>/dev/null | head -10); do
  cp "$f" "$SCRATCH/$(basename "$f")-codex.txt" 2>/dev/null
done

ls -lhS "$SCRATCH"
```

## Step 5: Web research with parallel subagents

Launch multiple Haiku subagents to research best practices:

**Agent 1 - AI CLI Agent Patterns:**
```
Research best practices for AI CLI agent configuration files (AGENTS.md, CLAUDE.md, system prompts).
Find:
1. Recommended structure and sections
2. Common mistakes to avoid
3. Optimal length and density
4. Essential vs optional components
Search for: "AGENTS.md best practices", "CLAUDE.md template", "AI agent system prompt optimization"
Return: Bullet points of actionable recommendations with sources.
```

**Agent 2 - Tech Stack Documentation:**
```
Research documentation best practices for [DETECTED_TECH_STACK].
Look at official docs, style guides, and community standards.
Find:
1. Recommended documentation structure
2. Essential files every project should have
3. Common documentation anti-patterns
4. Tools and generators used by the community
Return: Bullet points specific to this tech stack.
```

**Agent 3 - Conversation Analysis Prep:**
```
Read the conversation files in: [SCRATCH_DIR]
Analyze for:
1. Repeated questions that suggest missing documentation
2. Patterns of confusion or miscommunication
3. Tasks that took longer than expected due to context gaps
4. Tools or techniques discovered during conversation
Return: Specific documentation gaps with examples.
```

## Step 6: Analyze with Sonnet subagents

Batch conversations by size and launch parallel Sonnet agents:

**Prompt template:**
```
Read:
1. Documentation files to review:
[DOC_FILES]
2. Best practices research: [will be added]
3. Conversations: [CONVOS]

TASK: Analyze conversations against existing documentation to find improvements.

Find and output as bullet points:

## Instructions Violated
- Existing rules that weren't followed (quote the rule, show where it was violated)

## Documentation Gaps
- Patterns that should be documented but aren't
- Repeated questions that documentation could answer

## Suggested Improvements - By File
For each doc file, specific improvements:
[FILENAME]: [specific bullet points]

## Tech Stack Best Practices
- How this project could better document for its stack
- Tools/linters/generators to recommend

Be specific. Quote from conversations where helpful.
```

Batch by size:
- Large (>100KB): 1-2 per agent
- Medium (10-100KB): 3-5 per agent  
- Small (<10KB): 5-10 per agent

## Step 7: Aggregate findings

Combine all subagent outputs into:

```
# Documentation Retrospective

## Summary
[2-3 sentence overview of findings]

## Priority Improvements

### HIGH - Documentation Gaps (broken workflows)
[BULLETS]

### MEDIUM - Pattern Improvements  
[BULLETS]

### LOW - Nice to Have
[BULLETS]

## Suggested Changes by File

### [FILENAME]
**Current state:** [brief description]
**Suggested change:**
```[lang]
[proposed new content]
```

### [FILENAME]
...
```

## Step 8: Apply or Draft Changes

Ask user preference:
1. **Draft only** - Output proposed changes for review
2. **Apply** - Make changes directly (with backup)
3. **Interactive** - Review each change before applying

For apply mode:
```bash
# Backup originals
cp -r ./*.md /tmp/doc-retro-backup-$(date +%s)/ 2>/dev/null
cp ~/.claude/CLAUDE.md /tmp/doc-retro-backup-$(date +%s)/global-claude.md 2>/dev/null
```

Then apply changes using Edit tool.

## Alternative: Auto-Apply Mode

For confident, low-risk changes:
- Adding missing sections
- Fixing typos/formatting
- Reinforcing existing patterns
- Adding discovered tools to references

Requires user confirmation. Flag any structural changes for manual review.

(End of file)
