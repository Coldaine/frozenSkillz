#!/usr/bin/env pwsh
# Audit installed skills - check structure, extract metadata, find issues
# Usage: skills-audit.ps1 [-SkillPath <path>] [-Detailed]

param(
    [Parameter()]
    [string]$SkillPath = "",
    
    [Parameter()]
    [switch]$Detailed
)

function Get-SkillMetadata($path) {
    $skillMd = Join-Path $path "SKILL.md"
    if (-not (Test-Path $skillMd)) { return $null }
    
    $content = Get-Content $skillMd -Raw
    $meta = @{ Path = $path; Name = Split-Path $path -Leaf }
    
    if ($content -match '^---\s*\r?\n(.*?)\r?\n---') {
        $fm = $matches[1]
        if ($fm -match '^name:\s*(.+)') { $meta.Name = $matches[1].Trim() }
        if ($fm -match '^description:\s*(.+)') { $meta.Description = $matches[1].Trim() }
        $meta.DisableModelInvocation = $fm -match 'disable-model-invocation:\s*true'
    }
    
    # Check structure
    $meta.HasInstructions = Test-Path (Join-Path $path "instructions")
    $meta.HasScripts = Test-Path (Join-Path $path "scripts")
    $meta.HasTemplates = Test-Path (Join-Path $path "templates")
    $meta.IsMonolithic = ((Get-ChildItem $path -Recurse -File).Count -eq 1) -or ((Get-Content $skillMd).Count -gt 200)
    
    return $meta
}

# Find all skills
$agents = @(
    @{ Name = "claude-code"; Path = "$env:USERPROFILE\.claude\skills" },
    @{ Name = "codex"; Path = "$env:USERPROFILE\.codex\skills" },
    @{ Name = "kimi"; Path = "$env:USERPROFILE\.agents\skills" }
)

$skills = @()
foreach ($a in $agents) {
    if (-not (Test-Path $a.Path)) { continue }
    Get-ChildItem -Path $a.Path -Directory -ErrorAction SilentlyContinue | ForEach-Object {
        $meta = Get-SkillMetadata $_.FullName
        if ($meta) {
            $meta.Agent = $a.Name
            $skills += $meta
        }
    }
}

# Summary
Write-Host "`n=== Skill Audit Summary ===" -ForegroundColor Cyan
Write-Host "Total skills: $($skills.Count)" -ForegroundColor White
$skills | Group-Object Agent | ForEach-Object { Write-Host "  $($_.Name): $($_.Count)" }

# Issues
Write-Host "`n=== Potential Issues ===" -ForegroundColor Yellow
$issues = @()
foreach ($s in $skills) {
    if ($s.IsMonolithic) { $issues += "$($s.Name): Monolithic (no progressive disclosure)" }
    if (-not $s.HasScripts) { $issues += "$($s.Name): No scripts folder" }
    if (-not $s.Description) { $issues += "$($s.Name): No description in frontmatter" }
}
if ($issues) { $issues | ForEach-Object { Write-Host "  ⚠ $_" -ForegroundColor DarkYellow } }
else { Write-Host "  ✓ No major issues found" -ForegroundColor Green }

# Output table
Write-Host "`n=== Installed Skills ===" -ForegroundColor Cyan
$skills | Select-Object Agent, Name, @{N="HasScripts";E={$_.HasScripts}}, @{N="HasTemplates";E={$_.HasTemplates}}, @{N="Monolithic";E={$_.IsMonolithic}} | Format-Table -AutoSize
