param(
  [string]$RepoRoot = '.',
  [string]$Trunk,
  [switch]$AsJson
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$inventoryJson = & "$PSScriptRoot/stack-inventory.ps1" -RepoRoot $RepoRoot -AsJson
$inventory = $inventoryJson | ConvertFrom-Json

if (-not $Trunk) {
  $Trunk = $inventory.preflight.trunk
}
if (-not $Trunk) {
  $Trunk = 'main'
}

$openPrs = @($inventory.openPrs)
if ($openPrs.Count -eq 1 -and $openPrs[0] -and $openPrs[0].PSObject.Properties['value']) {
  $openPrs = @($openPrs[0].value)
}

$audited = @()
foreach ($pr in $openPrs) {
  $base = $null
  $head = $null
  $number = $null
  $title = $null
  $url = $null

  if ($pr.PSObject.Properties['baseRefName']) { $base = $pr.baseRefName }
  if ($pr.PSObject.Properties['headRefName']) { $head = $pr.headRefName }
  if ($pr.PSObject.Properties['number']) { $number = $pr.number }
  if ($pr.PSObject.Properties['title']) { $title = $pr.title }
  if ($pr.PSObject.Properties['url']) { $url = $pr.url }

  $classification = 'unknown'
  $notes = @()

  if ($base -eq $Trunk) {
    $classification = 'targets-trunk'
    $notes += 'PR targets trunk directly.'
  }
  elseif ($base) {
    $classification = 'targets-non-trunk'
    $notes += 'PR targets another branch and may already be part of a stack.'
  }

  $audited += [pscustomobject]@{
    number = $number
    title = $title
    head = $head
    base = $base
    classification = $classification
    notes = $notes
    url = $url
  }
}

$targetsTrunk = @($audited | Where-Object { $_.classification -eq 'targets-trunk' })
$targetsNonTrunk = @($audited | Where-Object { $_.classification -eq 'targets-non-trunk' })

$summary = @()
if ($audited.Count -gt 1 -and $targetsTrunk.Count -eq $audited.Count) {
  $summary += 'All open PRs target trunk. This is a flattened review graph.'
  $summary += 'Now review the diffs semantically: if the work is dependent, restack it; if it is truly independent, leaving it flat is fine.'
}
if ($targetsNonTrunk.Count -gt 0) {
  $summary += 'At least one PR already targets a non-trunk branch. Verify that the parent chain matches the intended review order.'
}
if ($audited.Count -eq 0) {
  $summary += 'No open PRs found.'
}

$result = [pscustomobject]@{
  repoRoot = $inventory.preflight.repoRoot
  trunk = $Trunk
  openPrCount = $audited.Count
  summary = $summary
  prs = $audited
}

if ($AsJson) {
  $result | ConvertTo-Json -Depth 8
  exit 0
}

Write-Output "Repo: $($result.repoRoot)"
Write-Output "Trunk: $($result.trunk)"
Write-Output "Open PR count: $($result.openPrCount)"
if ($summary.Count -gt 0) {
  Write-Output "Summary:"
  $summary | ForEach-Object { Write-Output " - $_" }
}
if ($audited.Count -gt 0) {
  Write-Output ""
  Write-Output "PR base audit:"
  $audited | Format-Table number,head,base,classification,title -AutoSize
}
