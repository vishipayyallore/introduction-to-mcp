<#
.SYNOPSIS
    Validate links in repository Markdown using Docker (lychee).

.DESCRIPTION
    Resolves the repository root (two levels above this script: tools/psscripts),
    then runs lycheeverse/lychee in a container against README.md and, when they
    exist, the docs/ and .github/ directories.

    Requires Docker on PATH (for example Docker Desktop on Windows).

.EXAMPLE
    ./tools/psscripts/docs-links.ps1

.EXAMPLE
    pwsh -File ./tools/psscripts/docs-links.ps1 -Verbose
#>
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error 'Docker is required (docker not found on PATH).'
    exit 1
}

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..' '..')).Path

$targets = [System.Collections.ArrayList]@('README.md')
foreach ($dir in @('docs', '.github')) {
    $p = Join-Path $repoRoot $dir
    if (Test-Path -LiteralPath $p -PathType Container) {
        [void]$targets.Add("${dir}/")
    }
}

$dockerArgs = @(
    'run', '--rm',
    '-v', "${repoRoot}:/work:ro",
    '-w', '/work',
    'lycheeverse/lychee:latest',
    '--no-progress',
    '--max-concurrency', '8'
)

if ($VerbosePreference -eq 'Continue') {
    $dockerArgs += '--verbose'
}

$dockerArgs += $targets.ToArray()

Write-Host "Running: docker $($dockerArgs -join ' ')"
& docker @dockerArgs
exit $LASTEXITCODE
