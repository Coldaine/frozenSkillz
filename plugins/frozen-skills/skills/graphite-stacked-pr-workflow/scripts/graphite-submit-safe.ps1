param(
  [string]$RepoRoot = '.',
  [switch]$Stack,
  [switch]$Draft,
  [switch]$Cli,
  [switch]$NoEdit,
  [switch]$Execute
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$preflightJson = & "$PSScriptRoot/graphite-preflight.ps1" -RepoRoot $RepoRoot -AsJson
$preflight = $preflightJson | ConvertFrom-Json

if (-not $preflight.gtPath) {
  throw 'gt is not installed on PATH.'
}
if (-not $preflight.graphiteInitialized) {
  throw 'Graphite is not initialized in this repo. Run gt init first.'
}
if ($preflight.hasConflicts) {
  throw 'The repo has merge/rebase conflicts. Resolve them before submit.'
}

$args = @('--cwd', $RepoRoot, 'submit')
if ($Stack) { $args += '--stack' }
if ($Draft) { $args += '--draft' }
if ($Cli) { $args += '--cli' }
if ($NoEdit) { $args += '--no-edit' }

if (-not $Execute) {
  $dryArgs = @($args + '--dry-run')
  Write-Output "Running dry run:"
  Write-Output "gt $($dryArgs -join ' ')"
  & gt @dryArgs
  exit $LASTEXITCODE
}

Write-Output "Executing:"
Write-Output "gt $($args -join ' ')"
& gt @args
exit $LASTEXITCODE
