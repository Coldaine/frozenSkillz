#!/usr/bin/env pwsh
# Skills CLI wrapper - search, install, list, info
# Usage: skills-cli.ps1 <command> [options]
#   skills-cli.ps1 search <query> [-Limit 10]
#   skills-cli.ps1 install <package> [-Global] [-Yes]
#   skills-cli.ps1 list [-Agent claude-code|codex|kimi]
#   skills-cli.ps1 info <package>

param(
    [Parameter(Mandatory=$true, Position=0)]
    [ValidateSet('search', 'install', 'list', 'info')]
    [string]$Command,
    
    [Parameter(Position=1)]
    [string]$Arg,
    
    [Parameter()]
    [int]$Limit = 10,
    
    [Parameter()]
    [switch]$Global,
    
    [Parameter()]
    [string]$Agent = "*",
    
    [Parameter()]
    [switch]$Yes
)

switch ($Command) {
    'search' {
        if (-not $Arg) { Write-Error "Search requires a query"; exit 1 }
        
        $output = npx skills find $Arg 2>$null
        if (-not $output) { Write-Error "Search failed"; exit 1 }
        
        $skills = @()
        foreach ($line in ($output -split "`r?`n")) {
            if ($line -match '\x1B\[38;5;145m(.+?)\x1B\[0m\s+\x1B\[36m([\d.]+)([K]?)\s+installs') {
                $installs = if ($matches[3] -eq 'K') { [int]([decimal]$matches[2] * 1000) } else { [int]$matches[2] }
                if ($matches[1] -match '^([^/]+)/([^@]+)@(.+)$') {
                    $skills += [PSCustomObject]@{
                        Name = $matches[1]
                        Repo = $matches[2]
                        Skill = $matches[3]
                        FullName = $matches[1] + "/" + $matches[2] + "@" + $matches[3]
                        Installs = $installs
                        InstallCmd = "npx skills add $($matches[0])"
                    }
                }
            }
        }
        $skills | Sort-Object Installs -Descending | Select-Object -First $Limit | Format-Table -AutoSize
    }
    
    'install' {
        if (-not $Arg) { Write-Error "Install requires a package (owner/repo@skill)"; exit 1 }
        
        $cmd = "npx skills add $Arg"
        if ($Global) { $cmd += " -g" }
        if ($Agent -ne "*") { $cmd += " -a $Agent" }
        if ($Yes) { $cmd += " -y" }
        $cmd += " --all"
        
        Write-Host "Running: $cmd" -ForegroundColor Cyan
        Invoke-Expression $cmd
    }
    
    'list' {
        $agents = @(
            @{ Name = "claude-code"; Path = "$env:USERPROFILE\.claude\skills" },
            @{ Name = "codex"; Path = "$env:USERPROFILE\.codex\skills" },
            @{ Name = "kimi"; Path = "$env:USERPROFILE\.agents\skills" }
        )
        
        $results = @()
        foreach ($a in $agents) {
            if ($Agent -ne "*" -and $a.Name -ne $Agent) { continue }
            if (Test-Path $a.Path) {
                Get-ChildItem -Path $a.Path -Directory -ErrorAction SilentlyContinue | ForEach-Object {
                    if (Test-Path (Join-Path $_.FullName "SKILL.md")) {
                        $results += [PSCustomObject]@{ Agent = $a.Name; Skill = $_.Name; Path = $_.FullName }
                    }
                }
            }
        }
        $results | Sort-Object Agent, Skill | Format-Table -AutoSize
    }
    
    'info' {
        if (-not $Arg) { Write-Error "Info requires a package"; exit 1 }
        Write-Host "https://skills.sh/$Arg" -ForegroundColor Cyan
        Write-Host "Install: npx skills add $Arg" -ForegroundColor Green
    }
}
