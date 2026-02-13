#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

VERSION="${1:-${RELEASE_VERSION:-}}"
if [[ -z "${VERSION}" ]]; then
  if TAG="$(git describe --tags --abbrev=0 2>/dev/null)"; then
    VERSION="${TAG#v}"
  fi
fi
if [[ -z "${VERSION}" ]]; then
  echo "Release version not set. Pass it as argument, set RELEASE_VERSION, or create a tag like v1.0.0." >&2
  exit 1
fi

PYTHON_BIN="${ROOT_DIR}/.venv/bin/python"
if [[ ! -x "${PYTHON_BIN}" ]]; then
  echo "Virtualenv not found. Create it with: python3 -m venv .venv" >&2
  exit 1
fi

APP_NAME="ArchiveCord"
APP_BUNDLE="dist/${APP_NAME}.app"
ZIP_ARTIFACT="dist/ArchiveCord-v${VERSION}-macos-universal.zip"
DMG_ARTIFACT="dist/ArchiveCord-v${VERSION}-macos-universal.dmg"

"${PYTHON_BIN}" -m PyInstaller --noconfirm --clean --windowed \
  --name "${APP_NAME}" \
  --add-data "exe/app_logo.ico:exe" \
  app/main.py

if [[ ! -d "${APP_BUNDLE}" ]]; then
  echo "Expected app bundle missing: ${APP_BUNDLE}" >&2
  exit 1
fi

rm -f "${ZIP_ARTIFACT}" "${DMG_ARTIFACT}"
ditto -c -k --keepParent "${APP_BUNDLE}" "${ZIP_ARTIFACT}"
hdiutil create -volname "${APP_NAME}" -srcfolder "${APP_BUNDLE}" -ov -format UDZO "${DMG_ARTIFACT}"

if [[ ! -f "${ZIP_ARTIFACT}" ]]; then
  echo "Missing macOS ZIP artifact: ${ZIP_ARTIFACT}" >&2
  exit 1
fi
if [[ ! -f "${DMG_ARTIFACT}" ]]; then
  echo "Missing macOS DMG artifact: ${DMG_ARTIFACT}" >&2
  exit 1
fi

echo "macOS build complete:"
echo "  ${ZIP_ARTIFACT}"
echo "  ${DMG_ARTIFACT}"
