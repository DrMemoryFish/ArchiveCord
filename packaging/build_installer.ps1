$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$iss = Join-Path $PSScriptRoot "installer\DiscordConversationProcessor.iss"
$portableExe = Join-Path $root "dist\DiscordConversationProcessor.exe"

if (-not (Test-Path $iss)) {
    throw "Inno Setup script not found: $iss"
}

if (-not (Test-Path $portableExe)) {
    Write-Host "Portable EXE not found. Building it first..."
    & (Join-Path $PSScriptRoot "build_portable.ps1")
}

$compiler = $env:INNO_SETUP_COMPILER
if (-not $compiler) {
    $compiler = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
}

if (-not (Test-Path $compiler)) {
    throw "Inno Setup compiler not found. Set INNO_SETUP_COMPILER or install Inno Setup 6."
}

& $compiler $iss

Write-Host "Installer build complete. Check dist_installer\\ for output."
