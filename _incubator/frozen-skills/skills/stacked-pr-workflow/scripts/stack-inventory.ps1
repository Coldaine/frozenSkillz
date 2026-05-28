param(
  [string]$RepoRoot = '.',
  [switch]$AsJson
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$preflightJson = & "$PSScriptRoot/stack-preflight.ps1" -RepoRoot $RepoRoot -AsJson
$preflight = $preflightJson | ConvertFrom-Json

function Invoke-Git {
  param([string[]]$GitArgs)
  & git -C $RepoRoot @GitArgs
}

$branchesRaw = Invoke-Git -GitArgs @('for-each-ref','--format=%(HEAD)|%(refname:short)|%(upstream:short)|%(objectname:short)|%(committerdate:iso8601)','refs/heads')
$branches = @()
foreach ($line in $branchesRaw) {
  $parts = $line -split '\|', 5
  $branches += [pscustomobject]@{
    isCurrent = ($parts[0] -eq '*')
    branch = $parts[1]
    upstream = $parts[2]
    sha = $parts[3]
    committerDate = $parts[4]
  }
}

$prs = @()
if ($preflight.ghPath -and $preflight.ghAuthenticated -and $preflight.repoSlug) {
  $prJson = & gh pr list --repo $preflight.repoSlug --limit 100 --state open --json number,title,headRefName,baseRefName,isDraft,url 2>$null
  if ($prJson) {
    $prs = $prJson | ConvertFrom-Json
  }
}

$gtLog = $null
$gtInfo = $null
if ($preflight.gtPath -and $preflight.graphiteInitialized) {
  $gtLog = @(& gt --cwd $RepoRoot log short 2>$null)
  $gtInfo = @(& gt --cwd $RepoRoot info --diff --stat 2>$null)
}

$result = [pscustomobject]@{
  preflight = $preflight
  branches = $branches
  openPrs = @($prs)
  graphiteLogShort = $gtLog
  graphiteInfo = $gtInfo
}

if ($AsJson) {
  $result | ConvertTo-Json -Depth 8
  exit 0
}

Write-Output "== Preflight =="
Write-Output "Repo: $($preflight.repoRoot)"
Write-Output "Current branch: $($preflight.currentBranch)"
Write-Output "Trunk: $($preflight.trunk)"
Write-Output "Graphite initialized: $($preflight.graphiteInitialized)"
Write-Output ""
Write-Output "== Local branches =="
$branches | Format-Table -AutoSize

if ($prs.Count -gt 0) {
  Write-Output ""
  Write-Output "== Open PRs =="
  $prs | Format-Table number,title,headRefName,baseRefName,isDraft,url -AutoSize
}

if ($gtLog) {
  Write-Output ""
  Write-Output "== gt log short =="
  $gtLog
}

if ($gtInfo) {
  Write-Output ""
  Write-Output "== gt info --diff --stat =="
  $gtInfo
}
