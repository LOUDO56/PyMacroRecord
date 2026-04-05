#!/usr/bin/env bash
set -e

APP_NAME="PyMacroRecord"
APP_ID="io.github.LOUDO56.PyMacroRecord"
ARCH=$(uname -m)
APPDIR="${APP_NAME}.AppDir"
APPIMAGETOOL_URL="https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-${ARCH}.AppImage"
APPIMAGETOOL="./appimagetool.AppImage"
VERSION=$(python3 -c "import re; print(re.search(r'\"([\d.]+)\"', open('src/utils/version.py').read()).group(1))")
UPDATE_INFO="gh-releases-zsync|LOUDO56|PyMacroRecord|latest|PyMacroRecord-*${ARCH}.AppImage.zsync"

echo ">>> Building version ${VERSION} with cx_Freeze..."
python setup_cx.py build
BUILD_DIR=$(find build -maxdepth 1 -name "exe.*" | head -1)

echo ">>> Preparing AppDir..."
rm -rf "${APPDIR}"
mkdir -p "${APPDIR}/usr/bin"
cp -r "${BUILD_DIR}/." "${APPDIR}/usr/bin/"

mkdir -p "${APPDIR}/usr/share/icons/hicolor/256x256/apps"
convert "src/assets/logo.ico" -thumbnail 256x256 \
    "${APPDIR}/usr/share/icons/hicolor/256x256/apps/${APP_ID}.png" 2>/dev/null \
    || cp "src/assets/logo.ico" "${APPDIR}/usr/share/icons/hicolor/256x256/apps/${APP_ID}.png"
cp "${APPDIR}/usr/share/icons/hicolor/256x256/apps/${APP_ID}.png" "${APPDIR}/${APP_ID}.png"

DESKTOP_CONTENT="[Desktop Entry]
Name=${APP_NAME}
Exec=${APP_NAME}
Icon=${APP_ID}
Type=Application
Categories=Utility;
X-AppImage-Version=${VERSION}"

mkdir -p "${APPDIR}/usr/share/applications"
echo "${DESKTOP_CONTENT}" > "${APPDIR}/usr/share/applications/${APP_ID}.desktop"
echo "${DESKTOP_CONTENT}" > "${APPDIR}/${APP_ID}.desktop"

mkdir -p "${APPDIR}/usr/share/metainfo"
DATE=$(date +%Y-%m-%d)
cat > "${APPDIR}/usr/share/metainfo/${APP_ID}.appdata.xml" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<component type="desktop-application">
  <id>${APP_ID}</id>
  <name>${APP_NAME}</name>
  <summary>Free macro recorder for Linux and Windows</summary>
  <metadata_license>MIT</metadata_license>
  <project_license>GPL-3.0</project_license>
  <developer id="io.github.LOUDO56">
    <name>LOUDO56</name>
  </developer>
  <launchable type="desktop-id">${APP_ID}.desktop</launchable>
  <description>
    <p>PyMacroRecord is a free macro recorder. Record mouse and keyboard actions and replay them.</p>
  </description>
  <url type="homepage">https://github.com/LOUDO56/PyMacroRecord</url>
  <releases>
    <release version="${VERSION}" date="${DATE}"/>
  </releases>
  <content_rating type="oars-1.1"/>
  <supports>
    <control>pointing</control>
    <control>keyboard</control>
  </supports>
</component>
EOF

cat > "${APPDIR}/AppRun" <<'EOF'
#!/usr/bin/env bash
HERE="$(dirname "$(readlink -f "$0")")"
export LD_LIBRARY_PATH="${HERE}/usr/bin/lib:${HERE}/usr/bin:${LD_LIBRARY_PATH}"
unset WAYLAND_DISPLAY
export DISPLAY="${DISPLAY:-:0}"
export GDK_BACKEND=x11
exec "${HERE}/usr/bin/PyMacroRecord" "$@"
EOF
chmod +x "${APPDIR}/AppRun"

if [ ! -f "${APPIMAGETOOL}" ]; then
    echo ">>> Downloading appimagetool..."
    curl -Lo "${APPIMAGETOOL}" "${APPIMAGETOOL_URL}"
    chmod +x "${APPIMAGETOOL}"
fi

echo ">>> Creating AppImage..."
ARCH="${ARCH}" "${APPIMAGETOOL}" --no-appstream -u "${UPDATE_INFO}" \
    "${APPDIR}" "${APP_NAME}-${VERSION}-${ARCH}.AppImage"

if command -v zsyncmake &>/dev/null; then
    echo ">>> Generating zsync..."
    zsyncmake "${APP_NAME}-${VERSION}-${ARCH}.AppImage"
fi

echo ""
echo "Done: ${APP_NAME}-${VERSION}-${ARCH}.AppImage"
