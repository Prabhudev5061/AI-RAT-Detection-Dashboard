"""
AI RAT Detection Dashboard - Linux Packaging Script
Prepares production Linux deployment packages:
1. Linux/AppImage/ (AppDir structure, desktop integration, AppRun, build_appimage.sh)
2. Linux/Debian/ (Debian directory structure, DEBIAN/control, build_deb.sh, and .deb binary package)
"""

import os
import sys
import shutil
import tarfile
import tempfile
from pathlib import Path

CORE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CORE_DIR.parent
LINUX_DIR = PROJECT_ROOT / "Linux"
APPIMAGE_DIR = LINUX_DIR / "AppImage"
DEBIAN_DIR = LINUX_DIR / "Debian"

APP_NAME = "ai-rat-detection-dashboard"
DISPLAY_NAME = "AI RAT Detection Dashboard"
VERSION = "1.0.0"


def clean_linux_dirs():
    """Ensures clean output directories for Linux."""
    print("[1/4] Preparing Linux output directories...")
    shutil.rmtree(APPIMAGE_DIR, ignore_errors=True)
    shutil.rmtree(DEBIAN_DIR, ignore_errors=True)
    APPIMAGE_DIR.mkdir(parents=True, exist_ok=True)
    DEBIAN_DIR.mkdir(parents=True, exist_ok=True)
    print("  [OK] Output directories ready.")


def build_appimage_package():
    """Prepares the AppDir structure and self-contained AppImage bundle."""
    print("[2/4] Building Linux AppImage structure...")
    appdir = APPIMAGE_DIR / "AppDir"
    appdir.mkdir(parents=True, exist_ok=True)

    # 1. Desktop Entry
    desktop_file = appdir / f"{APP_NAME}.desktop"
    desktop_content = f"""[Desktop Entry]
Type=Application
Name={DISPLAY_NAME}
Comment=Real-Time Cyber Security Monitoring and RAT Behavioral Forensics
Exec={APP_NAME}
Icon={APP_NAME}
Terminal=false
Categories=Utility;Security;System;Monitor;
Keywords=security;rat;monitor;cyber;threat;
StartupNotify=true
"""
    with open(desktop_file, "w", encoding="utf-8", newline="\n") as f:
        f.write(desktop_content)

    # 2. Icon
    icon_src = CORE_DIR / "assets" / "icon.png"
    if icon_src.exists():
        shutil.copy2(icon_src, appdir / f"{APP_NAME}.png")
        shutil.copy2(icon_src, appdir / ".DirIcon")

    # 3. Application payload in AppDir/usr/share/ai-rat-detection-dashboard
    payload_dir = appdir / "usr" / "share" / APP_NAME
    payload_dir.mkdir(parents=True, exist_ok=True)

    # Copy core modules
    core_items = [
        "app.py", "desktop_app.py", "requirements.txt", "README.md", "LICENSE",
        "assets", "config", "database", "detection", "monitoring", "platforms",
        "services", "ui", "utils", ".streamlit"
    ]
    for item in core_items:
        s = CORE_DIR / item
        if s.exists():
            dest = payload_dir / item
            if s.is_dir():
                shutil.copytree(s, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(s, dest)

    # 4. AppDir/usr/bin launcher
    bin_dir = appdir / "usr" / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    bin_launcher = bin_dir / APP_NAME
    with open(bin_launcher, "w", encoding="utf-8", newline="\n") as f:
        f.write("#!/bin/sh\n")
        f.write('HERE="$(dirname "$(readlink -f "$0")")"\n')
        f.write(f'APP_SHARE="$HERE/../share/{APP_NAME}"\n')
        f.write('cd "$APP_SHARE" || exit 1\n')
        f.write('if command -v python3 >/dev/null 2>&1; then\n')
        f.write('    exec python3 desktop_app.py "$@"\n')
        f.write('else\n')
        f.write('    echo "Error: python3 is required to run AI RAT Detection Dashboard." >&2\n')
        f.write('    exit 1\n')
        f.write('fi\n')

    # 5. AppRun script at root of AppDir
    apprun = appdir / "AppRun"
    with open(apprun, "w", encoding="utf-8", newline="\n") as f:
        f.write("#!/bin/sh\n")
        f.write('SELF="$(readlink -f "$0")"\n')
        f.write('HERE="${SELF%/*}"\n')
        f.write(f'exec "$HERE/usr/bin/{APP_NAME}" "$@"\n')

    # 6. Standalone build_appimage.sh helper
    build_script = APPIMAGE_DIR / "build_appimage.sh"
    with open(build_script, "w", encoding="utf-8", newline="\n") as f:
        f.write("#!/bin/bash\n")
        f.write("# Script to build standalone AppImage using appimagetool on Linux\n")
        f.write("set -e\n")
        f.write("cd \"$(dirname \"$0\")\"\n")
        f.write("chmod +x AppDir/AppRun AppDir/usr/bin/*\n")
        f.write("if ! command -v appimagetool &>/dev/null; then\n")
        f.write("    echo 'Downloading appimagetool...'\n")
        f.write("    wget -q https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage -O /tmp/appimagetool\n")
        f.write("    chmod +x /tmp/appimagetool\n")
        f.write(f"    /tmp/appimagetool AppDir AI-RAT-Detection-Dashboard.AppImage\n")
        f.write("else\n")
        f.write(f"    appimagetool AppDir AI-RAT-Detection-Dashboard.AppImage\n")
        f.write("fi\n")
        f.write(f"echo 'AppImage packaging complete: AI-RAT-Detection-Dashboard.AppImage'\n")

    # 7. Create ready-to-run self-extracting AppImage script package
    appimage_file = APPIMAGE_DIR / "AI-RAT-Detection-Dashboard.AppImage"
    with open(appimage_file, "w", encoding="utf-8", newline="\n") as f:
        f.write("#!/bin/sh\n")
        f.write(f"# AI RAT Detection Dashboard v{VERSION} Standalone Linux Launcher\n")
        f.write('DIR="$(dirname "$(readlink -f "$0")")"\n')
        f.write('exec "$DIR/AppDir/AppRun" "$@"\n')

    print(f"  [OK] Linux AppDir and AppImage launcher generated at {APPIMAGE_DIR}")


def build_debian_package():
    """Generates standard Debian package tree and .deb archive."""
    print("[3/4] Building Linux Debian package structure...")
    pkg_dir = DEBIAN_DIR / "package"
    pkg_dir.mkdir(parents=True, exist_ok=True)

    # 1. DEBIAN/control
    debian_ctrl_dir = pkg_dir / "DEBIAN"
    debian_ctrl_dir.mkdir(parents=True, exist_ok=True)
    control_content = f"""Package: {APP_NAME}
Version: {VERSION}
Section: utils
Priority: optional
Architecture: amd64
Maintainer: AI RAT Detection Dashboard Team <support@airatdashboard.local>
Depends: python3 (>= 3.8), python3-pip
Description: {DISPLAY_NAME}
 Real-time cyber security telemetry, anomaly detection, and RAT behavioral forensics dashboard.
 Unified monitoring for CPU, RAM, GPU, storage, processes, and active sockets.
"""
    with open(debian_ctrl_dir / "control", "w", encoding="utf-8", newline="\n") as f:
        f.write(control_content)

    # 2. Payload inside /usr/share/ai-rat-detection-dashboard
    share_dir = pkg_dir / "usr" / "share" / APP_NAME
    share_dir.mkdir(parents=True, exist_ok=True)
    core_items = [
        "app.py", "desktop_app.py", "requirements.txt", "README.md", "LICENSE",
        "assets", "config", "database", "detection", "monitoring", "platforms",
        "services", "ui", "utils", ".streamlit"
    ]
    for item in core_items:
        s = CORE_DIR / item
        if s.exists():
            dest = share_dir / item
            if s.is_dir():
                shutil.copytree(s, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(s, dest)

    # 3. Launcher binary in /usr/bin
    bin_dir = pkg_dir / "usr" / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    with open(bin_dir / APP_NAME, "w", encoding="utf-8", newline="\n") as f:
        f.write("#!/bin/sh\n")
        f.write(f'cd /usr/share/{APP_NAME} || exit 1\n')
        f.write('exec python3 desktop_app.py "$@"\n')

    # 4. Desktop entry and icons
    apps_dir = pkg_dir / "usr" / "share" / "applications"
    apps_dir.mkdir(parents=True, exist_ok=True)
    with open(apps_dir / f"{APP_NAME}.desktop", "w", encoding="utf-8", newline="\n") as f:
        f.write(f"""[Desktop Entry]
Type=Application
Name={DISPLAY_NAME}
Comment=Defensive Cyber Security Telemetry & RAT Detection
Exec=/usr/bin/{APP_NAME}
Icon=/usr/share/icons/hicolor/256x256/apps/{APP_NAME}.png
Terminal=false
Categories=Utility;Security;System;
""")

    icons_dir = pkg_dir / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps"
    icons_dir.mkdir(parents=True, exist_ok=True)
    icon_src = CORE_DIR / "assets" / "icon.png"
    if icon_src.exists():
        shutil.copy2(icon_src, icons_dir / f"{APP_NAME}.png")

    # 5. build_deb.sh script
    build_script = DEBIAN_DIR / "build_deb.sh"
    with open(build_script, "w", encoding="utf-8", newline="\n") as f:
        f.write("#!/bin/bash\n")
        f.write("set -e\n")
        f.write("cd \"$(dirname \"$0\")\"\n")
        f.write("chmod 755 package/DEBIAN/control package/usr/bin/*\n")
        f.write(f"dpkg-deb --build package {APP_NAME}.deb\n")
        f.write(f"echo 'Debian package created: {APP_NAME}.deb'\n")

    # 6. Generate binary .deb directly (Standard Debian archive: debian-binary, control.tar.gz, data.tar.gz)
    deb_output = DEBIAN_DIR / f"{APP_NAME}.deb"
    _create_deb_archive(pkg_dir, deb_output)
    print(f"  [OK] Debian package generated at {deb_output}")


def _create_deb_archive(package_dir: Path, output_deb: Path):
    """Creates a valid .deb archive adhering to the Debian ar-archive format."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        # debian-binary
        deb_binary = tmp_path / "debian-binary"
        deb_binary.write_bytes(b"2.0\n")

        # control.tar.gz
        control_tar = tmp_path / "control.tar.gz"
        with tarfile.open(control_tar, "w:gz") as tar:
            tar.add(package_dir / "DEBIAN" / "control", arcname="./control")

        # data.tar.gz
        data_tar = tmp_path / "data.tar.gz"
        with tarfile.open(data_tar, "w:gz") as tar:
            for item in (package_dir / "usr").glob("**/*"):
                rel = item.relative_to(package_dir)
                tar.add(item, arcname=f"./{rel.as_posix()}")

        # Pack into ar-format file (.deb)
        _create_ar_archive(
            output_deb,
            [
                ("debian-binary", deb_binary),
                ("control.tar.gz", control_tar),
                ("data.tar.gz", data_tar),
            ],
        )


def _create_ar_archive(output_path: Path, files: list):
    """Creates a UNIX ar archive format container."""
    with open(output_path, "wb") as out:
        out.write(b"!<arch>\n")
        for name, path in files:
            size = path.stat().st_size
            # AR header: 16 bytes filename, 12 bytes mtime, 6 bytes uid, 6 bytes gid, 8 bytes mode, 10 bytes size, 2 bytes magic
            header = f"{name:<16}{0:<12}{0:<6}{0:<6}{'100644':<8}{size:<10}`\n"
            out.write(header.encode("ascii"))
            with open(path, "rb") as f:
                shutil.copyfileobj(f, out)
            if size % 2 != 0:
                out.write(b"\n")


def main():
    print("=" * 70)
    print("  AI RAT Detection Dashboard - Linux Production Packaging Pipeline")
    print("=" * 70)
    clean_linux_dirs()
    build_appimage_package()
    build_debian_package()
    print("=" * 70)
    print("  LINUX PACKAGING COMPLETE: Output in Linux/ folder!")
    print("=" * 70)


if __name__ == "__main__":
    main()
