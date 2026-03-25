#!/usr/bin/env pwsh
# Extract metadata from SKILL.md frontmatter

param(
    [Parameter(Mandatory=$true)]
    [string]$SkillPath
)

$skillMd = Join-Path $SkillPath "SKILL.md"
if (-not (Test-Path $skillMd)) {
    Write-Error "SKILL.md not found: $skillMd"
    exit 1
}

$content = Get-Content $skillMd -Raw

$metadata = @{}

# Check for frontmatter
if ($content -match '^---\s*\r?\n(.*?)\r?\n---\s*\r?\n') {
    $frontmatter = $matches[1]
    
    # Extract name
    if ($frontmatter -match '^name:\s*(.+)$') {
        $metadata.Name = $matches[1].Trim()
    }
    
    # Extract description
    if ($frontmatter -match '^description:\s*(.+)$') {
        $metadata.Description = $matches[1].Trim()
    } elseif ($frontmatter -match '^description:\s*\|\s*\r?\n((?:\s+.+\r?\n)+)') {
        # Multi-line description with |
        $metadata.Description = $matches[1].Trim() -replace '\s+', ' '
    }
    
    # Extract disable-model-invocation
    $metadata.DisableModelInvocation = $frontmatter -match 'disable-model-invocation:\s*true'
    
    # Extract user-invocable
    $metadata.UserInvocable = -not ($frontmatter -match 'user-invocable:\s*false')
    
    # Extract allowed-tools
    if ($frontmatter -match 'allowed-tools:\s*\[(.*?)\]') {
        $metadata.AllowedTools = $matches[1].Split(',').Trim()
    }
}

# If no name in frontmatter, use directory name
if (-not $metadata.Name) {
    $metadata.Name = Split-Path $SkillPath -Leaf
}

# If no description, use first paragraph of body
if (-not $metadata.Description) {
    $body = $content -replace '^---.*?---\s*', ''
    if ($body -match '^\s*\r?\n\s*(.+?)\r?\n\r?\n') {
        $metadata.Description = $matches[1].Trim()
    }
}

$metadata.Path = $SkillPath

$metadata | ConvertTo-Json
