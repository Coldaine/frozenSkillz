#!/usr/bin/env pwsh
# Get detailed info about a skill from skills.sh
# Usage: get-skill-info.ps1 -Package "owner/repo@skill"

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Package
)

# Validate format
if (-not ($Package -match '^[^/]+/[^@]+@.+$')) {
    Write-Error "Invalid package format. Expected: owner/repo@skill"
    exit 1
}

$url = "https://skills.sh/$Package"
$apiUrl = $url -replace 'https://skills.sh/', 'https://api.skills.sh/skills/'

try {
    # Try to fetch from API first
    $response = Invoke-RestMethod -Uri $apiUrl -Method GET -ErrorAction SilentlyContinue
    
    if ($response) {
        $info = [PSCustomObject]@{
            Name = $response.name
            FullName = $Package
            Description = $response.description
            Source = $response.source_url
            InstallCount = $response.install_count
            InstallCommand = "npx skills add $Package"
            Url = $url
            UpdatedAt = $response.updated_at
        }
        $info | ConvertTo-Json -Depth 3
        exit 0
    }
} catch {
    # API failed, return basic info
}

# Fallback to basic info
$parts = $Package -split '@'
$repoPart = $parts[0]
$skillName = $parts[1]

$basicInfo = [PSCustomObject]@{
    Name = $skillName
    FullName = $Package
    Description = "Skill: $skillName from $repoPart"
    Source = "https://github.com/$repoPart"
    InstallCommand = "npx skills add $Package"
    Url = $url
}

$basicInfo | ConvertTo-Json -Depth 3
