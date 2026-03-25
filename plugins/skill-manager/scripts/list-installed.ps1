#!/usr/bin/env pwsh
# List all installed skills across agent tools

$agents = @(
    @{ Name = "claude-code"; Path = "$env:USERPROFILE\.claude\skills" },
    @{ Name = "codex"; Path = "$env:USERPROFILE\.codex\skills" },
    @{ Name = "kimi"; Path = "$env:USERPROFILE\.agents\skills" }
)

$results = @()

foreach ($agent in $agents) {
    $skillsPath = $agent.Path
    
    if (-not (Test-Path $skillsPath)) {
        continue
    }
    
    $skills = Get-ChildItem -Path $skillsPath -Directory -ErrorAction SilentlyContinue
    
    foreach ($skill in $skills) {
        $skillMdPath = Join-Path $skill.FullName "SKILL.md"
        
        if (Test-Path $skillMdPath) {
            # Extract name from directory (most reliable)
            $skillName = $skill.Name
            
            # Try to get name from frontmatter
            $content = Get-Content $skillMdPath -Raw -ErrorAction SilentlyContinue
            if ($content -match '^---\s*\r?\n.*?name:\s*(.+?)\s*\r?\n') {
                $skillName = $matches[1].Trim()
            }
            
            $results += [PSCustomObject]@{
                Agent = $agent.Name
                Skill = $skillName
                Path = $skill.FullName
            }
        }
    }
}

# Output as table
$results | Sort-Object Agent, Skill | Format-Table -AutoSize

# Also output raw for piping
$results | ConvertTo-Json -Compress
