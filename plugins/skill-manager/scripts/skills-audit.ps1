#!/usr/bin/env pwsh
# Audit installed skills - check structure, extract metadata, find issues.
# Usage: skills-audit.ps1 [-SkillPath <path>] [-Detailed]

param(
    [Parameter()]
    [string]$SkillPath = "",

    [Parameter()]
    [switch]$Detailed
)

$ErrorActionPreference = "Stop"

function Get-SkillMetadata {
    param([string]$Path)

    $skillMd = Join-Path $Path "SKILL.md"
    if (-not (Test-Path -LiteralPath $skillMd)) { return $null }

    $content = Get-Content -LiteralPath $skillMd -Raw
    $meta = [ordered]@{
        Path = $Path
        Name = Split-Path $Path -Leaf
        Description = ""
        DisableModelInvocation = $false
    }

    if ($content -match '(?s)^---\s*\r?\n(.*?)\r?\n---') {
        $frontmatter = $matches[1]
        if ($frontmatter -match '(?m)^name:\s*(.+)$') { $meta.Name = $matches[1].Trim().Trim('"') }
        if ($frontmatter -match '(?m)^description:\s*(.+)$') { $meta.Description = $matches[1].Trim().Trim('"') }
        $meta.DisableModelInvocation = $frontmatter -match 'disable-model-invocation:\s*true'
    }

    $fileCount = @(Get-ChildItem -LiteralPath $Path -Recurse -Force -File -ErrorAction SilentlyContinue).Count
    $lineCount = @(Get-Content -LiteralPath $skillMd -ErrorAction SilentlyContinue).Count
    $meta.HasInstructions = Test-Path -LiteralPath (Join-Path $Path "instructions")
    $meta.HasScripts = Test-Path -LiteralPath (Join-Path $Path "scripts")
    $meta.HasTemplates = Test-Path -LiteralPath (Join-Path $Path "templates")
    $meta.IsMonolithic = ($fileCount -eq 1) -or ($lineCount -gt 200)

    return [pscustomobject]$meta
}

if ($SkillPath) {
    $agents = @(@{ Name = "custom"; Path = $SkillPath })
} else {
    $agents = @(
        @{ Name = "claude-code"; Path = "$env:USERPROFILE\.claude\skills" },
        @{ Name = "codex"; Path = "$env:USERPROFILE\.codex\skills" },
        @{ Name = "shared-agents"; Path = "$env:USERPROFILE\.agents\skills" },
        @{ Name = "gemini"; Path = "$env:USERPROFILE\.gemini\skills" }
    )
}

$skills = @()
foreach ($agent in $agents) {
    if (-not (Test-Path -LiteralPath $agent.Path)) { continue }
    Get-ChildItem -LiteralPath $agent.Path -Directory -Force -ErrorAction SilentlyContinue | ForEach-Object {
        $meta = Get-SkillMetadata $_.FullName
        if ($meta) {
            $meta | Add-Member -NotePropertyName Agent -NotePropertyValue $agent.Name -Force
            $skills += $meta
        }
    }
}

Write-Host "`n=== Skill Audit Summary ===" -ForegroundColor Cyan
Write-Host "Total skills: $($skills.Count)" -ForegroundColor White
$skills | Group-Object Agent | ForEach-Object { Write-Host "  $($_.Name): $($_.Count)" }

Write-Host "`n=== Potential Issues ===" -ForegroundColor Yellow
$issues = @()
foreach ($skill in $skills) {
    if ($skill.IsMonolithic) { $issues += "$($skill.Name): Monolithic or single-file skill" }
    if (-not $skill.HasScripts) { $issues += "$($skill.Name): No scripts folder" }
    if (-not $skill.Description) { $issues += "$($skill.Name): No description in frontmatter" }
}

if ($issues) {
    $issues | ForEach-Object { Write-Host "  WARN $_" -ForegroundColor DarkYellow }
} else {
    Write-Host "  OK No major issues found" -ForegroundColor Green
}

Write-Host "`n=== Installed Skills ===" -ForegroundColor Cyan
$skills |
    Select-Object Agent, Name, HasScripts, HasTemplates, IsMonolithic |
    Sort-Object Agent, Name |
    Format-Table -AutoSize
