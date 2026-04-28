param(
  [string]$RepoRoot = '.',
  [switch]$AsJson
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$inventoryJson = & "$PSScriptRoot/stack-inventory.ps1" -RepoRoot $RepoRoot -AsJson
$inventory = $inventoryJson | ConvertFrom-Json

$trunk = $inventory.preflight.trunk
$currentBranch = $inventory.preflight.currentBranch
$openPrs = @($inventory.openPrs)
if ($openPrs.Count -eq 1 -and $openPrs[0] -and $openPrs[0].PSObject.Properties['value']) {
  $openPrs = @($openPrs[0].value)
}
$nonTrunkBasePrs = @(
  $openPrs | Where-Object {
    $_ -and
    $_.PSObject.Properties['baseRefName'] -and
    $_.baseRefName -and
    $_.baseRefName -ne $trunk
  }
)

$scenario = 'greenfield-stack'
$reason = 'No open PR graph issues were detected. Start with the clean-stack workflow unless the current branch is semantically mixed.'
$nextDocs = @(
  'docs/experimentation/graphite-scenario-router.md',
  'plugins/frozen-skills/skills/graphite-stacked-pr-workflow/workflows/greenfield-stack.md'
)

if ($openPrs.Count -gt 1 -and $nonTrunkBasePrs.Count -gt 0) {
  $scenario = 'messy-pr-graph'
  $reason = 'Multiple open PRs already exist and at least one is based on a non-trunk branch. Audit and repair the PR graph before changing more code.'
  $nextDocs = @(
    'docs/experimentation/graphite-scenario-router.md',
    'plugins/frozen-skills/skills/graphite-stacked-pr-workflow/workflows/messy-pr-graph.md'
  )
}
elseif ($openPrs.Count -gt 1) {
  $scenario = 'messy-pr-graph'
  $reason = 'Multiple open PRs exist. Even if they all target trunk today, verify whether they should actually form a stack instead of parallel review branches.'
  $nextDocs = @(
    'docs/experimentation/graphite-scenario-router.md',
    'plugins/frozen-skills/skills/graphite-stacked-pr-workflow/workflows/messy-pr-graph.md'
  )
}
elseif ($openPrs.Count -eq 1 -and $currentBranch -and $currentBranch -ne $trunk) {
  $scenario = 'greenfield-or-messy-branch'
  $reason = 'One active branch/PR exists. If it contains one clean story, use greenfield. If it contains multiple stories, switch to messy-branch repair.'
  $nextDocs = @(
    'docs/experimentation/graphite-scenario-router.md',
    'plugins/frozen-skills/skills/graphite-stacked-pr-workflow/workflows/greenfield-stack.md',
    'plugins/frozen-skills/skills/graphite-stacked-pr-workflow/workflows/messy-branch-to-stack.md'
  )
}
elseif ($currentBranch -and $currentBranch -ne $trunk) {
  $scenario = 'greenfield-or-messy-branch'
  $reason = 'You are on a non-trunk branch with no existing PR graph pressure. Decide whether the branch is already clean or needs slicing.'
  $nextDocs = @(
    'docs/experimentation/graphite-scenario-router.md',
    'plugins/frozen-skills/skills/graphite-stacked-pr-workflow/workflows/greenfield-stack.md',
    'plugins/frozen-skills/skills/graphite-stacked-pr-workflow/workflows/messy-branch-to-stack.md'
  )
}

$result = [pscustomobject]@{
  repoRoot = $inventory.preflight.repoRoot
  trunk = $trunk
  currentBranch = $currentBranch
  openPrCount = $openPrs.Count
  recommendedScenario = $scenario
  reason = $reason
  nextDocs = $nextDocs
}

if ($AsJson) {
  $result | ConvertTo-Json -Depth 6
  exit 0
}

Write-Output "Repo: $($result.repoRoot)"
Write-Output "Current branch: $($result.currentBranch)"
Write-Output "Trunk: $($result.trunk)"
Write-Output "Open PR count: $($result.openPrCount)"
Write-Output "Recommended scenario: $($result.recommendedScenario)"
Write-Output "Reason: $($result.reason)"
Write-Output "Next docs:"
$result.nextDocs | ForEach-Object { Write-Output " - $_" }
