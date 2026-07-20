[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $CommandArgs
)

$target = $env:PDM_CLI_SSH_TARGET
if ([string]::IsNullOrWhiteSpace($target)) {
    throw 'Set PDM_CLI_SSH_TARGET to the authorized SSH runner for the official PDM client.'
}
if ($target.StartsWith('-') -or $target -notmatch '^[A-Za-z0-9_.-]+@[A-Za-z0-9_.:-]+$') {
    throw 'PDM_CLI_SSH_TARGET must be a user@host value, not SSH options or shell syntax.'
}

$remoteProgram = if ([string]::IsNullOrWhiteSpace($env:PDM_CLI_REMOTE_PROGRAM)) {
    'hermes-pdm'
} else {
    $env:PDM_CLI_REMOTE_PROGRAM
}
if ($remoteProgram -notmatch '^[A-Za-z0-9_./-]+$') {
    throw 'PDM_CLI_REMOTE_PROGRAM must be one executable name or absolute POSIX path.'
}

function ConvertTo-PosixSingleQuoted {
    param([Parameter(Mandatory = $true)][string] $Value)
    $apostrophe = [string][char]39
    $doubleQuote = [string][char]34
    $replacement = $apostrophe + $doubleQuote + $apostrophe + $doubleQuote + $apostrophe
    return $apostrophe + $Value.Replace($apostrophe, $replacement) + $apostrophe
}

if (-not $CommandArgs -or $CommandArgs.Count -eq 0) {
    $CommandArgs = @('help')
}

$remoteCommand = @(
    (ConvertTo-PosixSingleQuoted $remoteProgram)
    $CommandArgs | ForEach-Object { ConvertTo-PosixSingleQuoted $_ }
) -join ' '

& ssh $target $remoteCommand
exit $LASTEXITCODE
