#!/usr/bin/env pwsh
# Check if a skill directory has proper progressive disclosure structure

param(
    [Parameter(Mandatory=$true)]
    [string]$SkillPath
)

if (-not (Test-Path $SkillPath)) {
    Write-Error "Skill path not found: $SkillPath"
    exit 1
}

$skillMd = Join-Path $SkillPath "SKILL.md"
if (-not (Test-Path $skillMd)) {
    Write-Error "SKILL.md not found in: $SkillPath"
    exit 1
}

$structure = @{
    HasSkillMd = $true
    HasInstructions = Test-Path (Join-Path $SkillPath "instructions")
    HasScripts = Test-Path (Join-Path $SkillPath "scripts")
    HasTemplates = Test-Path (Join-Path $SkillPath "templates")
    HasExamples = Test-Path (Join-Path $SkillPath "examples")
    HasReferences = Test-Path (Join-Path $SkillPath "references")
    FileCount = (Get-ChildItem $SkillPath -Recurse -File).Count
    SkillMdLines = (Get-Content $skillMd).Count
}

# Determine if monolithic
$structure.IsMonolithic = $structure.FileCount -eq 1 -or $structure.SkillMdLines -gt 200

# Output
$structure | ConvertTo-Json
