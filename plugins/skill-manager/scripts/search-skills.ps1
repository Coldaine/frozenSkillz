#!/usr/bin/env pwsh
# Search skills.sh registry using the Skills CLI
# Usage: search-skills.ps1 -Query "pr review" [-Limit 10]

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Query,
    
    [Parameter()]
    [int]$Limit = 10
)

# Run skills find and capture output
$output = npx skills find $Query 2>$null

if (-not $output) {
    Write-Error "Failed to search skills registry. Is 'skills' CLI available?"
    exit 1
}

# Parse the ANSI-formatted output
$skills = @()
$lines = $output -split "`r?`n"

foreach ($line in $lines) {
    # Match skill lines with ANSI escape codes
    # ESC[38;5;145mowner/repo@skillESC[0m ESC[36mN installsESC[0m
    # ESC = 0x1B = \x1B in regex
    if ($line -match '\x1B\[38;5;145m(.+?)\x1B\[0m\s+\x1B\[36m([\d.]+)([K]?)\s+installs') {
        $skillRef = $matches[1]
        $installNum = [decimal]$matches[2]
        $suffix = $matches[3]
        
        # Convert K suffix to thousands
        if ($suffix -eq 'K') {
            $installs = [int]($installNum * 1000)
        } else {
            $installs = [int]$installNum
        }
        
        # Parse owner/repo@skill format
        if ($skillRef -match '^([^/]+)/([^@]+)@(.+)$') {
            $skills += [PSCustomObject]@{
                FullName = $skillRef
                Owner = $matches[1]
                Repo = $matches[2]
                Skill = $matches[3]
                Installs = $installs
                InstallCommand = "npx skills add $skillRef"
                Url = "https://skills.sh/$skillRef"
            }
        }
    }
}

# Sort by installs (popularity) and limit
$skills = $skills | Sort-Object -Property Installs -Descending | Select-Object -First $Limit

# Output as JSON for machine consumption
$skills | ConvertTo-Json -Depth 3
