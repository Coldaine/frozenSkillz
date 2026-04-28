param(
  [string]$RepoRoot = '.',
  [string]$Remote = 'origin',
  [string]$Trunk,
  [switch]$AsJson
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Invoke-Git {
  param([string[]]$GitArgs)
  $hadNativePreference = Test-Path Variable:\PSNativeCommandUseErrorActionPreference
  if ($hadNativePreference) {
    $previousNativePreference = $PSNativeCommandUseErrorActionPreference
  }
  try {
    $PSNativeCommandUseErrorActionPreference = $false
    & git -C $RepoRoot @GitArgs 2>$null
  }
  finally {
    if ($hadNativePreference) {
      $PSNativeCommandUseErrorActionPreference = $previousNativePreference
    }
    else {
      Remove-Variable PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue
    }
  }
}

function Test-RemoteRef {
  param([string]$RefName)
  $resolved = Invoke-Git -GitArgs @('rev-parse','--verify',$RefName)
  return [bool]$resolved
}

function Resolve-Commit {
  param([string]$RefName)
  $resolved = Invoke-Git -GitArgs @('rev-parse','--verify',$RefName)
  if (-not $resolved) {
    return $null
  }
  return ($resolved | Select-Object -First 1).Trim()
}

function Ensure-RemoteHeadRef {
  param(
    [string]$RemoteName,
    [string]$HeadName
  )

  $remoteRef = "refs/remotes/$RemoteName/$HeadName"
  if (Test-RemoteRef -RefName $remoteRef) {
    return $remoteRef
  }

  & git -C $RepoRoot fetch --quiet $RemoteName "refs/heads/$HeadName:refs/remotes/$RemoteName/$HeadName" 1>$null 2>$null
  if ($LASTEXITCODE -ne 0) {
    return $null
  }

  if (Test-RemoteRef -RefName $remoteRef) {
    return $remoteRef
  }

  return $null
}

function Get-DiffFiles {
  param(
    [string]$BaseRef,
    [string]$HeadRef
  )
  $files = @(Invoke-Git -GitArgs @('diff','--name-only',"$BaseRef...$HeadRef"))
  return @($files | Where-Object { $_ -and $_.Trim() })
}

$inventoryJson = & "$PSScriptRoot/stack-inventory.ps1" -RepoRoot $RepoRoot -AsJson
$inventory = $inventoryJson | ConvertFrom-Json

if (-not $Trunk) {
  $Trunk = $inventory.preflight.trunk
}
if (-not $Trunk) {
  $Trunk = 'main'
}
$trunkCommit = Resolve-Commit -RefName $Trunk
if (-not $trunkCommit) {
  $trunkCommit = Resolve-Commit -RefName "refs/remotes/$Remote/$Trunk"
}
if (-not $trunkCommit) {
  throw "Could not resolve trunk ref: $Trunk"
}

$openPrs = @($inventory.openPrs)
if ($openPrs.Count -eq 1 -and $openPrs[0] -and $openPrs[0].PSObject.Properties['value']) {
  $openPrs = @($openPrs[0].value)
}

$prs = @()
foreach ($pr in $openPrs) {
  $head = $pr.headRefName
  $base = $pr.baseRefName
  $number = $pr.number
  $title = $pr.title
  $url = $pr.url

  $remoteHead = Ensure-RemoteHeadRef -RemoteName $Remote -HeadName $head
  if (-not $remoteHead) {
    continue
  }

  $headCommit = Resolve-Commit -RefName $remoteHead
  if (-not $headCommit) {
    continue
  }

  $files = Get-DiffFiles -BaseRef $trunkCommit -HeadRef $headCommit
  $prs += [pscustomobject]@{
    number = $number
    title = $title
    head = $head
    base = $base
    url = $url
    remoteRef = $remoteHead
    headCommit = $headCommit
    changedFiles = $files
  }
}

$pairs = @()
for ($i = 0; $i -lt $prs.Count; $i++) {
  for ($j = $i + 1; $j -lt $prs.Count; $j++) {
    $left = $prs[$i]
    $right = $prs[$j]

    & git -C $RepoRoot merge-base --is-ancestor $left.headCommit $right.headCommit 1>$null 2>$null
    $leftAncestorOfRight = ($LASTEXITCODE -eq 0)

    & git -C $RepoRoot merge-base --is-ancestor $right.headCommit $left.headCommit 1>$null 2>$null
    $rightAncestorOfLeft = ($LASTEXITCODE -eq 0)

    $sharedFiles = @($left.changedFiles | Where-Object { $right.changedFiles -contains $_ })
    $sharedCount = $sharedFiles.Count

    $leftOnlyCommits = @(Invoke-Git -GitArgs @('rev-list','--count',"$($right.headCommit)..$($left.headCommit)") | Select-Object -First 1)
    $rightOnlyCommits = @(Invoke-Git -GitArgs @('rev-list','--count',"$($left.headCommit)..$($right.headCommit)") | Select-Object -First 1)

    $relationship = 'independent-or-unclear'
    $reason = 'No ancestry relationship detected.'

    if ($leftAncestorOfRight -and -not $rightAncestorOfLeft) {
      $relationship = 'likely-dependent'
      $reason = "PR #$($right.number) appears to be built on top of PR #$($left.number)."
    }
    elseif ($rightAncestorOfLeft -and -not $leftAncestorOfRight) {
      $relationship = 'likely-dependent'
      $reason = "PR #$($left.number) appears to be built on top of PR #$($right.number)."
    }
    elseif ($sharedCount -gt 0) {
      $relationship = 'overlap-without-clear-ancestry'
      $reason = 'The branches touch some of the same files but no strict ancestry relation was proven.'
    }

    $pairs += [pscustomobject]@{
      leftPr = $left.number
      leftHead = $left.head
      rightPr = $right.number
      rightHead = $right.head
      leftAncestorOfRight = $leftAncestorOfRight
      rightAncestorOfLeft = $rightAncestorOfLeft
      leftOnlyCommitCount = [int]($leftOnlyCommits[0] | ForEach-Object { $_.ToString().Trim() })
      rightOnlyCommitCount = [int]($rightOnlyCommits[0] | ForEach-Object { $_.ToString().Trim() })
      sharedFileCount = $sharedCount
      sharedFiles = $sharedFiles
      relationship = $relationship
      reason = $reason
    }
  }
}

$result = [pscustomobject]@{
  repoRoot = $inventory.preflight.repoRoot
  trunk = $Trunk
  analyzedPrCount = $prs.Count
  prs = $prs | Select-Object number,title,head,base,url
  pairwiseAnalysis = $pairs
}

if ($AsJson) {
  $result | ConvertTo-Json -Depth 8
  exit 0
}

Write-Output "Repo: $($result.repoRoot)"
Write-Output "Trunk: $($result.trunk)"
Write-Output "Analyzed PR count: $($result.analyzedPrCount)"
Write-Output ""
Write-Output "Pairwise dependency inference:"
if ($pairs.Count -eq 0) {
  Write-Output "No analyzable PR pairs found."
  exit 0
}

$pairs | Format-Table leftPr,rightPr,relationship,leftAncestorOfRight,rightAncestorOfLeft,sharedFileCount -AutoSize
Write-Output ""
foreach ($pair in $pairs) {
  Write-Output "#$($pair.leftPr) vs #$($pair.rightPr): $($pair.reason)"
}
