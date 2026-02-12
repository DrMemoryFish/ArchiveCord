$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$iss = Join-Path $PSScriptRoot "installer\DiscordConversationProcessor.iss"
$version = $env:RELEASE_VERSION
if (-not $version) {
    try {
        $tag = (git describe --tags --abbrev=0) 2>$null
        if ($tag) {
            $version = $tag -replace '^v', ''
        }
    } catch {
        $version = $null
    }
}
if (-not $version) {
    throw "Release version not set. Set RELEASE_VERSION or create a tag like v1.0.0."
}

$portableExeName = "ArchiveCord-v$version-win64-portable.exe"
$portableExe = Join-Path $root ("dist\" + $portableExeName)

if (-not (Test-Path $iss)) {
    throw "Inno Setup script not found: $iss"
}

if (-not (Test-Path $portableExe)) {
    Write-Host "Portable EXE not found. Building it first..."
    $env:RELEASE_VERSION = $version
    & (Join-Path $PSScriptRoot "build_portable.ps1")
}

$compiler = $env:INNO_SETUP_COMPILER
if (-not $compiler) {
    $compiler = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
}

if (-not (Test-Path $compiler)) {
    throw "Inno Setup compiler not found. Set INNO_SETUP_COMPILER or install Inno Setup 6."
}

& $compiler /DMyAppVersion=$version $iss

Write-Host "Installer build complete. Check dist_installer\\ for output."
