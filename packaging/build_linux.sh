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
DIST_DIR="${ROOT_DIR}/dist"
ONEDIR="${DIST_DIR}/${APP_NAME}"
TAR_ARTIFACT="${DIST_DIR}/ArchiveCord-v${VERSION}-linux-x86_64.tar.gz"
APPIMAGE_ARTIFACT="${DIST_DIR}/ArchiveCord-v${VERSION}-linux-x86_64.AppImage"
APPDIR="${DIST_DIR}/AppDir"

"${PYTHON_BIN}" -m PyInstaller --noconfirm --clean --windowed \
  --name "${APP_NAME}" \
  --add-data "exe/app_logo.ico:exe" \
  app/main.py

if [[ ! -d "${ONEDIR}" ]]; then
  echo "Expected Linux onedir build missing: ${ONEDIR}" >&2
  exit 1
fi

rm -f "${TAR_ARTIFACT}" "${APPIMAGE_ARTIFACT}"
tar -C "${DIST_DIR}" -czf "${TAR_ARTIFACT}" "${APP_NAME}"

rm -rf "${APPDIR}"
mkdir -p "${APPDIR}/usr/lib/${APP_NAME}" "${APPDIR}/usr/share/applications" "${APPDIR}/usr/share/icons/hicolor/scalable/apps"
cp -a "${ONEDIR}/." "${APPDIR}/usr/lib/${APP_NAME}/"

cat > "${APPDIR}/AppRun" <<'EOF'
#!/usr/bin/env bash
HERE="$(dirname "$(readlink -f "$0")")"
cd "$HERE/usr/lib/ArchiveCord"
exec ./ArchiveCord "$@"
EOF
chmod +x "${APPDIR}/AppRun"

cat > "${APPDIR}/ArchiveCord.desktop" <<'EOF'
[Desktop Entry]
Type=Application
Name=ArchiveCord
Exec=ArchiveCord
Icon=ArchiveCord
Categories=Utility;
Terminal=false
EOF

cat > "${APPDIR}/ArchiveCord.svg" <<'EOF'
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="20" fill="#2c8f7a"/>
  <path d="M30 48h68v40H30z" fill="#0f1115"/>
  <circle cx="52" cy="68" r="7" fill="#2c8f7a"/>
  <circle cx="76" cy="68" r="7" fill="#2c8f7a"/>
</svg>
EOF

cp "${APPDIR}/ArchiveCord.desktop" "${APPDIR}/usr/share/applications/ArchiveCord.desktop"
cp "${APPDIR}/ArchiveCord.svg" "${APPDIR}/usr/share/icons/hicolor/scalable/apps/ArchiveCord.svg"

APPIMAGETOOL="${DIST_DIR}/appimagetool-x86_64.AppImage"
curl -fsSL -o "${APPIMAGETOOL}" "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
chmod +x "${APPIMAGETOOL}"
ARCH=x86_64 APPIMAGE_EXTRACT_AND_RUN=1 "${APPIMAGETOOL}" "${APPDIR}" "${APPIMAGE_ARTIFACT}"
chmod +x "${APPIMAGE_ARTIFACT}"

if [[ ! -f "${TAR_ARTIFACT}" ]]; then
  echo "Missing Linux tar.gz artifact: ${TAR_ARTIFACT}" >&2
  exit 1
fi
if [[ ! -f "${APPIMAGE_ARTIFACT}" ]]; then
  echo "Missing Linux AppImage artifact: ${APPIMAGE_ARTIFACT}" >&2
  exit 1
fi

echo "Linux build complete:"
echo "  ${TAR_ARTIFACT}"
echo "  ${APPIMAGE_ARTIFACT}"
