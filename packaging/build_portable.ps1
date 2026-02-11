$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $root

$venvPython = Join-Path $root ".venv\\Scripts\\python.exe"
if (-not (Test-Path $venvPython)) {
    throw "Virtualenv not found. Create it with: python -m venv .venv"
}

$icon = Join-Path $root "exe\app_logo.ico"
if (-not (Test-Path $icon)) {
    throw "Icon not found: $icon"
}

& $venvPython -m PyInstaller --noconfirm --clean --onefile --windowed `
    --name "DiscordConversationProcessor" `
    --icon "$icon" `
    --add-data "$icon;exe" `
    app\main.py

if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller failed with exit code $LASTEXITCODE. Install it with: pip install -r requirements-dev.txt"
}

Write-Host "Portable build complete: $root\dist\DiscordConversationProcessor.exe"
