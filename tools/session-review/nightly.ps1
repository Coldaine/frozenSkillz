# Nightly session review driver.
#
#   .\nightly.ps1                       # grade up to config.cap ungraded skill-firing sessions
#   .\nightly.ps1 -Sessions "id1,id2"   # explicit sessions (calibration)
#
# Trusts parsed stdout over letta exit codes (known spurious libuv abort on Windows).

param(
    [string]$Sessions = ""
)

$ErrorActionPreference = "Stop"
$here = $PSScriptRoot
$cfg = Get-Content (Join-Path $here "config.json") -Raw | ConvertFrom-Json
if ($cfg.agent_id -match "PENDING") { throw "config.json agent_id is not set — create the cloud reviewer agent first." }

# Rubric = the Prompt section of reviewer-prompt.md
$doc = Get-Content (Join-Path $here "reviewer-prompt.md") -Raw
$rubric = ($doc -split "## Prompt", 2)[1]
$rubric = ($rubric -split "## Calibration set", 2)[0].Trim()

python (Join-Path $here "skill_versions.py")
$condArgs = if ($Sessions) { @("--sessions", $Sessions) } else { @("--new", "--cap", "$($cfg.cap)") }
$files = python (Join-Path $here "condense.py") @condArgs | Where-Object { $_ -like "*.json" }
if (-not $files) { Write-Host "nothing to grade"; exit 0 }

$gradesDir = Join-Path $here "grades"
New-Item -ItemType Directory -Force $gradesDir | Out-Null
$gradesFile = Join-Path $gradesDir ("{0:yyyy-MM}.jsonl" -f (Get-Date))
$statePath = Join-Path $here "state.json"
$state = if (Test-Path $statePath) { Get-Content $statePath -Raw | ConvertFrom-Json -AsHashtable } else { @{ graded = @{} } }

foreach ($f in $files) {
    $traj = Get-Content $f -Raw
    $sid = ($traj | ConvertFrom-Json).session_id
    Write-Host "grading $sid"
    $prompt = $rubric + "`n`nSession to grade:`n```json`n" + $traj + "`n```"
    $raw = $prompt | letta -a $cfg.agent_id -p --new --output-format json --max-turns 6 2>$null | Out-String
    $verdict = $null
    try {
        $outer = $raw | ConvertFrom-Json
        $inner = $outer.result -replace '(?s)^.*?```json\s*', '' -replace '(?s)```.*$', ''
        $verdict = $inner | ConvertFrom-Json
    } catch {
        Write-Warning "unparseable verdict for $sid — raw saved to .work"
        Set-Content -Path (Join-Path $here ".work" "FAILED-$([regex]::Replace($sid,'[^A-Za-z0-9_-]','_')).txt") -Value $raw
        continue
    }
    $record = $verdict | ConvertTo-Json -Depth 8 -Compress
    Add-Content -Path $gradesFile -Value $record
    if ($verdict.mutation_candidate) {
        $prop = "`n## $sid ($(Get-Date -Format yyyy-MM-dd))`n`n" +
                "Skill context: $(($verdict.skills | ForEach-Object name) -join ', ')`n`n" +
                "$($verdict.mutation_candidate)`n"
        Add-Content -Path (Join-Path $here "proposals.md") -Value $prop
    }
    $state.graded[$sid] = (Get-Date -Format yyyy-MM-dd)
}

$state | ConvertTo-Json -Depth 4 | Set-Content $statePath
Write-Host "done — grades in $gradesFile"
