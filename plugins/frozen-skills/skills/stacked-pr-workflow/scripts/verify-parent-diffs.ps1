param(
  [string]$RepoRoot = '.',
  [Parameter(Mandatory = $true)]
  [string[]]$Branches,
  [string]$Trunk,
  [switch]$AsJson
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Invoke-Git {
  param([string[]]$GitArgs)
  & git -C $RepoRoot @GitArgs 2>$null
}

if (-not $Trunk) {
  $originHead = (Invoke-Git -GitArgs @('symbolic-ref','refs/remotes/origin/HEAD') | Select-Object -First 1)
  if ($originHead) {
    $Trunk = $originHead.Trim() -replace '^refs/remotes/origin/', ''
  }
}
if (-not $Trunk) { $Trunk = 'main' }

$reports = @()
$parent = $Trunk
foreach ($branch in $Branches) {
  $commitLines = @(Invoke-Git -GitArgs @('log','--oneline',"$parent..$branch"))
  $diffStat = @(Invoke-Git -GitArgs @('diff','--stat',"$parent...$branch"))
  $reports += [pscustomobject]@{
    parent = $parent
    branch = $branch
    commitCount = $commitLines.Count
    hasIncrementalWork = ($commitLines.Count -gt 0)
    commits = $commitLines
    diffStat = $diffStat
  }
  $parent = $branch
}

if ($AsJson) {
  $reports | ConvertTo-Json -Depth 8
  exit 0
}

foreach ($report in $reports) {
  Write-Output "== $($report.parent) -> $($report.branch) =="
  Write-Output "Incremental commits: $($report.commitCount)"
  if (-not $report.hasIncrementalWork) {
    Write-Output "WARNING: no incremental commits detected."
  }
  if ($report.commits.Count -gt 0) {
    Write-Output "-- commits --"
    $report.commits
  }
  if ($report.diffStat.Count -gt 0) {
    Write-Output "-- diffstat --"
    $report.diffStat
  }
  Write-Output ""
}
