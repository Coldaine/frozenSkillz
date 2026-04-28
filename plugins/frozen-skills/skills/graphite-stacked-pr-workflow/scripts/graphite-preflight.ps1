param(
  [string]$RepoRoot = '.',
  [switch]$AsJson
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Test-Tool {
  param([string]$Name)
  $cmd = Get-Command $Name -ErrorAction SilentlyContinue
  if ($null -ne $cmd) { return $cmd.Source }
  return $null
}

function Get-GitHubRepoSlug {
  param([string]$RemoteUrl)
  if (-not $RemoteUrl) { return $null }

  if ($RemoteUrl -match 'github\.com[:/](?<slug>[^/]+/[^/.]+?)(?:\.git)?$') {
    return $Matches.slug
  }

  return $null
}

function Invoke-Git {
  param([string[]]$GitArgs)
  & git -C $RepoRoot @GitArgs 2>$null
}

$gitPath = Test-Tool git
if (-not $gitPath) { throw 'git is required but was not found on PATH.' }

$repoTop = Invoke-Git -GitArgs @('rev-parse','--show-toplevel')
if (-not $repoTop) { throw "Not a git repository: $RepoRoot" }
$repoTop = ($repoTop | Select-Object -First 1).Trim()

$ghPath = Test-Tool gh
$gtPath = Test-Tool gt
$originUrl = (Invoke-Git -GitArgs @('remote','get-url','origin') | Select-Object -First 1)
$repoSlug = Get-GitHubRepoSlug -RemoteUrl $originUrl
$currentBranch = (Invoke-Git -GitArgs @('branch','--show-current') | Select-Object -First 1).Trim()
$statusLines = @(Invoke-Git -GitArgs @('status','--short'))
$hasConflicts = (@(Invoke-Git -GitArgs @('diff','--name-only','--diff-filter=U')).Count -gt 0)

$trunk = $null
$originHead = (Invoke-Git -GitArgs @('symbolic-ref','refs/remotes/origin/HEAD') | Select-Object -First 1)
if ($originHead) {
  $trunk = $originHead.Trim() -replace '^refs/remotes/origin/', ''
}
if (-not $trunk) {
  foreach ($candidate in @('main','master')) {
    $exists = Invoke-Git -GitArgs @('rev-parse','--verify',"refs/heads/$candidate")
    if ($exists) {
      $trunk = $candidate
      break
    }
  }
}

$graphiteConfig = Join-Path $repoTop '.git/.graphite_repo_config'
$graphiteInitialized = Test-Path $graphiteConfig
$ghAuth = $false
if ($ghPath) {
  & gh auth status 1>$null 2>$null
  $ghAuth = ($LASTEXITCODE -eq 0)
}

$result = [pscustomobject]@{
  repoRoot = $repoTop
  currentBranch = $currentBranch
  trunk = $trunk
  gitPath = $gitPath
  ghPath = $ghPath
  repoSlug = $repoSlug
  originUrl = $originUrl
  gtPath = $gtPath
  ghAuthenticated = $ghAuth
  graphiteInitialized = $graphiteInitialized
  graphiteConfigPath = $graphiteConfig
  worktreeDirty = ($statusLines.Count -gt 0)
  hasConflicts = $hasConflicts
}

if ($AsJson) {
  $result | ConvertTo-Json -Depth 4
  exit 0
}

Write-Output "Repo: $($result.repoRoot)"
Write-Output "Current branch: $($result.currentBranch)"
Write-Output "Trunk: $($result.trunk)"
Write-Output "git: $($result.gitPath)"
Write-Output "gh: $($result.ghPath)"
Write-Output "gt: $($result.gtPath)"
Write-Output "gh authenticated: $($result.ghAuthenticated)"
Write-Output "Graphite initialized: $($result.graphiteInitialized)"
Write-Output "Worktree dirty: $($result.worktreeDirty)"
Write-Output "Has conflicts: $($result.hasConflicts)"
