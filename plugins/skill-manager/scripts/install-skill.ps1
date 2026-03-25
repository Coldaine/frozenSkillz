#!/usr/bin/env pwsh
# Install a skill from the registry using Skills CLI
# Usage: install-skill.ps1 -Package "owner/repo@skill" [-Global] [-Agent "claude-code,kimi"]

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Package,
    
    [Parameter()]
    [switch]$Global,
    
    [Parameter()]
    [string]$Agent = "*",
    
    [Parameter()]
    [switch]$Yes
)

$cmd = "npx skills add $Package"

if ($Global) {
    $cmd += " -g"
}

if ($Agent) {
    $cmd += " -a $Agent"
}

if ($Yes) {
    $cmd += " -y"
}

# Add --all flag for convenience (install all skills from package to all agents)
$cmd += " --all"

Write-Host "Executing: $cmd" -ForegroundColor Cyan

Invoke-Expression $cmd

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Skill installed successfully" -ForegroundColor Green
} else {
    Write-Error "Failed to install skill"
    exit 1
}
