#!/usr/bin/env pwsh
# Dry-run skill state inventory and reconciliation for frozenSkillz.
# This script reads live client skill/config surfaces, but writes only inside
# the frozenSkillz repo when using the "report" command.

param(
    [Parameter(Position = 0)]
    [ValidateSet("inventory", "plan", "report")]
    [string]$Command = "inventory",

    [Parameter()]
    [string]$RepoRoot = "",

    [Parameter()]
    [string]$PolicyPath = "",

    [Parameter()]
    [string]$OutDir = "",

    [Parameter()]
    [switch]$Json
)

$ErrorActionPreference = "Stop"

function Resolve-RepoRoot {
    param([string]$Value)

    if ($Value) {
        return (Resolve-Path -LiteralPath $Value).Path
    }

    return (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..\..\..")).Path
}

function Normalize-PathValue {
    param([string]$Value)

    if (-not $Value) { return "" }
    return $Value.Replace("/", "\")
}

function Get-RelativePathSafe {
    param(
        [string]$BasePath,
        [string]$TargetPath
    )

    try {
        return [System.IO.Path]::GetRelativePath($BasePath, $TargetPath)
    } catch {
        return $TargetPath
    }
}

function Read-JsonFile {
    param([string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) { return $null }
    return Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json
}

function Read-SkillMetadata {
    param(
        [string]$SkillFile,
        [string]$FallbackName
    )

    $meta = [ordered]@{
        name = $FallbackName
        description = ""
        skill_file = $SkillFile
        has_frontmatter = $false
    }

    if (-not (Test-Path -LiteralPath $SkillFile)) {
        return [pscustomobject]$meta
    }

    $content = Get-Content -LiteralPath $SkillFile -Raw
    if ($content -match '(?s)^---\s*\r?\n(.*?)\r?\n---') {
        $meta.has_frontmatter = $true
        $frontmatter = $matches[1]
        if ($frontmatter -match '(?m)^name:\s*["'']?([^"''\r\n]+)["'']?\s*$') {
            $meta.name = $matches[1].Trim()
        }
        if ($frontmatter -match '(?m)^description:\s*(.+?)\s*$') {
            $meta.description = $matches[1].Trim().Trim('"')
        }
    }

    return [pscustomobject]$meta
}

function Get-DirectoryFileCount {
    param([string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) { return 0 }
    return @(Get-ChildItem -LiteralPath $Path -Recurse -Force -File -ErrorAction SilentlyContinue).Count
}

function Get-LinkInfo {
    param([string]$Path)

    $item = Get-Item -LiteralPath $Path -Force -ErrorAction SilentlyContinue
    if (-not $item) {
        return [pscustomobject]@{ link_type = ""; target = "" }
    }

    $target = ""
    if ($item.Target) {
        $target = @($item.Target) -join ";"
    }

    return [pscustomobject]@{ link_type = [string]$item.LinkType; target = $target }
}

function Get-SkillEntriesFromRoot {
    param(
        [string]$Client,
        [string]$RootPath,
        [string]$SourceType,
        [string[]]$DisabledNames = @(),
        [string[]]$EnabledOnly = @(),
        [switch]$RecursiveSkillFiles,
        [switch]$IncludeContainers,
        [switch]$SkipNodeModules
    )

    $entries = @()
    if (-not (Test-Path -LiteralPath $RootPath)) { return $entries }

    $root = (Resolve-Path -LiteralPath $RootPath).Path
    $skillFiles = @()

    if ($RecursiveSkillFiles) {
        $all = Get-ChildItem -LiteralPath $root -Recurse -Force -File -ErrorAction SilentlyContinue |
            Where-Object {
                $_.Name -in @("SKILL.md", "skill.md") -and
                (-not $SkipNodeModules -or $_.FullName -notmatch '\\node_modules\\')
            }
        $skillFiles = @($all)
    } else {
        foreach ($dir in Get-ChildItem -LiteralPath $root -Directory -Force -ErrorAction SilentlyContinue) {
            $skillFile = Join-Path $dir.FullName "SKILL.md"
            if (-not (Test-Path -LiteralPath $skillFile)) {
                $skillFile = Join-Path $dir.FullName "skill.md"
            }
            if (Test-Path -LiteralPath $skillFile) {
                $skillFiles += Get-Item -LiteralPath $skillFile -Force
            } elseif ($IncludeContainers) {
                $link = Get-LinkInfo $dir.FullName
                $entries += [pscustomobject][ordered]@{
                    client = $Client
                    skill_id = $dir.Name
                    declared_name = $dir.Name
                    source_type = $SourceType
                    root = $root
                    path = $dir.FullName
                    skill_file = ""
                    enabled = $null
                    has_skill_file = $false
                    file_count = Get-DirectoryFileCount $dir.FullName
                    link_type = $link.link_type
                    target = $link.target
                    description = ""
                }
            }
        }
    }

    foreach ($file in $skillFiles) {
        $skillDir = Split-Path -Parent $file.FullName
        $fallbackName = Split-Path -Leaf $skillDir
        $meta = Read-SkillMetadata -SkillFile $file.FullName -FallbackName $fallbackName
        $link = Get-LinkInfo $skillDir

        $enabled = $null
        if ($EnabledOnly.Count -gt 0) {
            $enabled = $meta.name -in $EnabledOnly -or $fallbackName -in $EnabledOnly
        } elseif ($DisabledNames.Count -gt 0) {
            $enabled = -not ($meta.name -in $DisabledNames -or $fallbackName -in $DisabledNames)
        }

        $entries += [pscustomobject][ordered]@{
            client = $Client
            skill_id = $fallbackName
            declared_name = $meta.name
            source_type = $SourceType
            root = $root
            path = $skillDir
            skill_file = $file.FullName
            enabled = $enabled
            has_skill_file = $true
            file_count = Get-DirectoryFileCount $skillDir
            link_type = $link.link_type
            target = $link.target
            description = $meta.description
        }
    }

    return $entries
}

function Get-CodexSkillConfig {
    param([string]$ConfigPath)

    $refs = @()
    if (-not (Test-Path -LiteralPath $ConfigPath)) { return $refs }

    $current = [ordered]@{}
    foreach ($line in Get-Content -LiteralPath $ConfigPath) {
        if ($line -match '^\s*\[\[skills\.config\]\]\s*$') {
            if ($current.Count -gt 0) { $refs += [pscustomobject]$current }
            $current = [ordered]@{ source = "codex-config"; path = ""; name = ""; enabled = $null; exists = $null }
            continue
        }
        if ($current.Count -eq 0) { continue }
        if ($line -match '^\s*path\s*=\s*"(.+)"') {
            $current.path = Normalize-PathValue $matches[1]
            $current.exists = Test-Path -LiteralPath $current.path
            if (-not $current.name) {
                $parent = Split-Path -Parent $current.path
                if ($parent) { $current.name = Split-Path -Leaf $parent }
            }
        }
        if ($line -match '^\s*name\s*=\s*"(.+)"') {
            $current.name = $matches[1]
        }
        if ($line -match '^\s*enabled\s*=\s*(true|false)') {
            $current.enabled = [bool]::Parse($matches[1])
        }
    }
    if ($current.Count -gt 0) { $refs += [pscustomobject]$current }
    return $refs
}

function Get-OpencodeSkillReferences {
    param([string]$ConfigRoot)

    $refs = @()
    if (-not (Test-Path -LiteralPath $ConfigRoot)) { return $refs }

    $files = @(
        Join-Path $ConfigRoot "opencode.json"
        Join-Path $ConfigRoot "oh-my-openagent.json"
    ) | Where-Object { Test-Path -LiteralPath $_ }

    foreach ($file in $files) {
        $raw = Get-Content -LiteralPath $file -Raw
        $matches = [regex]::Matches($raw, 'C:\\\\Users\\\\[^"\\]+\\\\\.agents\\\\skills\\\\[^"\\]+')
        foreach ($match in $matches) {
            $path = $match.Value.Replace("\\", "\").TrimEnd("\*")
            $refs += [pscustomobject][ordered]@{
                source = "opencode-config"
                config_file = $file
                path = $path
                exists = Test-Path -LiteralPath $path
            }
        }
    }

    return $refs
}

function Get-GeminiDisabledNames {
    param([string]$SettingsPath)

    $settings = Read-JsonFile $SettingsPath
    if (-not $settings -or -not $settings.skills -or -not $settings.skills.disabled) {
        return @()
    }
    return @($settings.skills.disabled)
}

function Get-Inventory {
    param(
        [string]$RepoRoot,
        [object]$Policy
    )

    $userHome = $env:USERPROFILE
    $geminiDisabled = Get-GeminiDisabledNames (Join-Path $userHome ".gemini\settings.json")
    $entries = @()

    $entries += Get-SkillEntriesFromRoot -Client "claude" -RootPath (Join-Path $userHome ".claude\skills") -SourceType "runtime-local" -IncludeContainers
    $entries += Get-SkillEntriesFromRoot -Client "shared-agents" -RootPath (Join-Path $userHome ".agents\skills") -SourceType "shared-agents" -IncludeContainers
    $entries += Get-SkillEntriesFromRoot -Client "gemini" -RootPath (Join-Path $userHome ".agents\skills") -SourceType "shared-agents" -DisabledNames $geminiDisabled
    $entries += Get-SkillEntriesFromRoot -Client "gemini" -RootPath (Join-Path $userHome ".gemini\skills") -SourceType "runtime-local" -DisabledNames $geminiDisabled -IncludeContainers
    $entries += Get-SkillEntriesFromRoot -Client "codex" -RootPath (Join-Path $userHome ".codex\skills") -SourceType "runtime-local" -IncludeContainers
    $entries += Get-SkillEntriesFromRoot -Client "codex-plugin-cache" -RootPath (Join-Path $userHome ".codex\plugins\cache") -SourceType "client-plugin" -RecursiveSkillFiles -SkipNodeModules
    $entries += Get-SkillEntriesFromRoot -Client "opencode" -RootPath (Join-Path $userHome ".config\opencode") -SourceType "runtime-local" -RecursiveSkillFiles -SkipNodeModules
    $entries += Get-SkillEntriesFromRoot -Client "frozen-published" -RootPath (Join-Path $RepoRoot "plugins") -SourceType "repo-published" -RecursiveSkillFiles -SkipNodeModules
    $entries += Get-SkillEntriesFromRoot -Client "frozen-archived" -RootPath (Join-Path $RepoRoot "removed-needs-rework") -SourceType "repo-archived" -RecursiveSkillFiles -SkipNodeModules

    foreach ($entry in $entries) {
        if ($entry.path -match '\\\.system(\\|$)') { $entry.source_type = "client-system" }
        if ($entry.path -match '\\plugins\\cache\\') { $entry.source_type = "client-plugin" }
        if ($entry.link_type -and $entry.target -match '\\plugins\\frozen-skills\\skills\\') { $entry.source_type = "repo-published-junction" }
    }

    $codexConfig = Get-CodexSkillConfig (Join-Path $userHome ".codex\config.toml")
    $opencodeRefs = Get-OpencodeSkillReferences (Join-Path $userHome ".config\opencode")

    return [pscustomobject][ordered]@{
        generated_at = (Get-Date).ToString("o")
        repo_root = $RepoRoot
        policy_file = if ($Policy) { $Policy.__path } else { "" }
        skills = @($entries | Sort-Object client, declared_name, path)
        config_references = @($codexConfig + $opencodeRefs)
    }
}

function New-Plan {
    param(
        [object]$Inventory,
        [object]$Policy
    )

    $actions = @()
    $skills = @($Inventory.skills)
    $refs = @($Inventory.config_references)

    $geminiPolicy = $Policy.clients.gemini
    if ($geminiPolicy -and $geminiPolicy.enabled_only) {
        $enabledOnly = @($geminiPolicy.enabled_only)
        foreach ($skill in @($skills | Where-Object { $_.client -eq "gemini" -and $_.has_skill_file })) {
            $desired = $skill.declared_name -in $enabledOnly -or $skill.skill_id -in $enabledOnly
            if ($skill.enabled -ne $desired) {
                $actions += [pscustomobject][ordered]@{
                    severity = "drift"
                    client = "gemini"
                    skill = $skill.declared_name
                    action = if ($desired) { "would-enable" } else { "would-disable" }
                    path = $skill.path
                    reason = "Gemini enabled state differs from policy enabled_only list."
                }
            }
        }
    }

    $sharedPolicy = @()
    if ($Policy.clients.shared_agents -and $Policy.clients.shared_agents.allowed) {
        $sharedPolicy = @($Policy.clients.shared_agents.allowed)
    }
    foreach ($skill in @($skills | Where-Object { $_.client -eq "shared-agents" -and $_.has_skill_file })) {
        if ($sharedPolicy.Count -gt 0 -and -not ($skill.declared_name -in $sharedPolicy -or $skill.skill_id -in $sharedPolicy)) {
            $actions += [pscustomobject][ordered]@{
                severity = "review"
                client = "shared-agents"
                skill = $skill.declared_name
                action = "would-mark-review"
                path = $skill.path
                reason = "Shared .agents skill is not listed as an allowed shared skill."
            }
        }
    }

    foreach ($ref in @($refs | Where-Object { $_.path -and $_.exists -eq $false })) {
        $actions += [pscustomobject][ordered]@{
            severity = "broken-reference"
            client = $ref.source
            skill = if ($ref.name) { $ref.name } else { "" }
            action = "would-remove-stale-reference"
            path = $ref.path
            reason = "Configured skill path does not exist."
        }
    }

    $dupes = $skills |
        Where-Object { $_.has_skill_file } |
        Group-Object declared_name |
        Where-Object { $_.Name -and $_.Count -gt 1 }
    foreach ($group in $dupes) {
        $locations = @($group.Group | Sort-Object path -Unique)
        if ($locations.Count -le 1) { continue }
        $sourceTypes = @($locations | Select-Object -ExpandProperty source_type -Unique)
        $actions += [pscustomobject][ordered]@{
            severity = "duplicate"
            client = "multi"
            skill = $group.Name
            action = "would-review-duplicates"
            path = (@($locations | Select-Object -ExpandProperty path) -join "; ")
            reason = "Same declared skill appears in multiple source types: $($sourceTypes -join ', ')."
        }
    }

    return [pscustomobject][ordered]@{
        generated_at = (Get-Date).ToString("o")
        mode = "dry-run"
        actions = @($actions | Sort-Object severity, client, skill, path)
    }
}

function Write-StateReport {
    param(
        [object]$Inventory,
        [object]$Plan,
        [string]$ReportPath
    )

    $lines = @()
    $lines += "# Skill State Dry Run"
    $lines += ""
    $lines += "Generated: $($Inventory.generated_at)"
    $lines += ""
    $lines += "This report is dry-run only. It records observed state and proposed changes; it does not prove that any live client config was changed."
    $lines += ""
    $lines += "## Summary"
    $lines += ""
    foreach ($group in @($Inventory.skills | Group-Object client | Sort-Object Name)) {
        $enabledCount = @($group.Group | Where-Object { $_.enabled -eq $true }).Count
        $disabledCount = @($group.Group | Where-Object { $_.enabled -eq $false }).Count
        $lines += ('- `{0}`: {1} entries; enabled={2} disabled={3}' -f $group.Name, $group.Count, $enabledCount, $disabledCount)
    }
    $lines += ""
    $lines += "## Proposed Dry-Run Actions"
    $lines += ""
    if (@($Plan.actions).Count -eq 0) {
        $lines += "- No drift actions proposed."
    } else {
        foreach ($action in @($Plan.actions)) {
            $lines += ('- **{0}** `{1}` `{2}`: {3} - {4} `{5}`' -f $action.severity, $action.client, $action.skill, $action.action, $action.reason, $action.path)
        }
    }
    $lines += ""
    $lines += "## Config References"
    $lines += ""
    foreach ($ref in @($Inventory.config_references | Sort-Object source, path, name)) {
        $label = if ($ref.path) { $ref.path } else { $ref.name }
        $lines += ('- `{0}`: exists={1} enabled={2} `{3}`' -f $ref.source, $ref.exists, $ref.enabled, $label)
    }

    Set-Content -LiteralPath $ReportPath -Value ($lines -join "`n") -Encoding utf8
}

$repo = Resolve-RepoRoot $RepoRoot
if (-not $PolicyPath) { $PolicyPath = Join-Path $repo "skill-policy.json" }
if (-not $OutDir) { $OutDir = Join-Path $repo "reports" }

$policy = Read-JsonFile $PolicyPath
if ($policy) {
    $policy | Add-Member -NotePropertyName "__path" -NotePropertyValue $PolicyPath -Force
}

$inventory = Get-Inventory -RepoRoot $repo -Policy $policy
$plan = New-Plan -Inventory $inventory -Policy $policy

switch ($Command) {
    "inventory" {
        if ($Json) { $inventory | ConvertTo-Json -Depth 20 }
        else { $inventory.skills | Select-Object client, declared_name, source_type, enabled, path | Format-Table -AutoSize }
    }
    "plan" {
        if ($Json) { $plan | ConvertTo-Json -Depth 20 }
        else { $plan.actions | Format-Table severity, client, skill, action, reason -AutoSize }
    }
    "report" {
        New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
        $lockPath = Join-Path $repo "skill-state.lock.json"
        $reportPath = Join-Path $OutDir "latest-skill-state.md"

        $inventory | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $lockPath -Encoding utf8
        Write-StateReport -Inventory $inventory -Plan $plan -ReportPath $reportPath

        [pscustomobject][ordered]@{
            lock = $lockPath
            report = $reportPath
            dry_run_actions = @($plan.actions).Count
        } | Format-List
    }
}
