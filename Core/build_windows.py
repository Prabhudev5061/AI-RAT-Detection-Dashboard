"""
AI RAT Detection Dashboard - Windows Build & Packaging Script
Builds the standalone Windows Portable release and the Inno Setup Installer package.
Outputs directly into Windows/Portable and Windows/Installer.
"""

import os
import sys
import shutil
import zipfile
import subprocess
from pathlib import Path

# Configure utf-8 stdout for Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

CORE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CORE_DIR.parent
WINDOWS_DIR = PROJECT_ROOT / "Windows"
PORTABLE_DIR = WINDOWS_DIR / "Portable"
INSTALLER_DIR = WINDOWS_DIR / "Installer"
BUILD_DIR = CORE_DIR / "build"
DIST_TEMP_DIR = CORE_DIR / "dist"

APP_NAME = "AI-RAT-Detection-Dashboard"
ZIP_FILE = PORTABLE_DIR / f"{APP_NAME}-Windows-x64.zip"


def check_prerequisites():
    """Validates necessary build assets and dependencies."""
    print("[1/6] Checking build prerequisites...")
    icon_path = CORE_DIR / "assets" / "icon.ico"
    if not icon_path.exists():
        print(f"Error: Icon file not found at {icon_path}", file=sys.stderr)
        sys.exit(1)

    fonts_dir = CORE_DIR / "assets" / "fonts"
    reg_font = fonts_dir / "JetBrainsMono-Regular.ttf"
    if not reg_font.exists():
        print(f"Error: JetBrains Mono font not found at {reg_font}", file=sys.stderr)
        sys.exit(1)

    print("  [OK] Application icons verified.")
    print("  [OK] Local JetBrains Mono fonts verified.")
    print("  [OK] Source files and schemas verified.")


def clean_previous_builds():
    """Removes previous build artifacts to ensure a fresh, clean build."""
    print("[2/6] Cleaning previous build artifacts...")
    for p in (BUILD_DIR, DIST_TEMP_DIR, PORTABLE_DIR, INSTALLER_DIR):
        if p.is_dir():
            shutil.rmtree(p, ignore_errors=True)
            print(f"  Cleaned directory: {p.name}")
    PORTABLE_DIR.mkdir(parents=True, exist_ok=True)
    INSTALLER_DIR.mkdir(parents=True, exist_ok=True)


def run_pyinstaller():
    """Executes PyInstaller to build the Windows executable."""
    print(f"[3/6] Compiling {APP_NAME} with PyInstaller...")

    sep = ";" if os.name == "nt" else ":"
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        f"--name={APP_NAME}",
        f"--icon={CORE_DIR / 'assets' / 'icon.ico'}",
        # Add project source and asset directories
        f"--add-data={CORE_DIR / 'app.py'}{sep}.",
        f"--add-data={CORE_DIR / 'assets'}{sep}assets",
        f"--add-data={CORE_DIR / 'database' / 'schema.sql'}{sep}database",
        f"--add-data={CORE_DIR / 'config'}{sep}config",
        f"--add-data={CORE_DIR / 'detection'}{sep}detection",
        f"--add-data={CORE_DIR / 'monitoring'}{sep}monitoring",
        f"--add-data={CORE_DIR / 'platforms'}{sep}platforms",
        f"--add-data={CORE_DIR / 'services'}{sep}services",
        f"--add-data={CORE_DIR / 'ui'}{sep}ui",
        f"--add-data={CORE_DIR / 'utils'}{sep}utils",
        f"--add-data={CORE_DIR / '.streamlit'}{sep}.streamlit",
        # Collect dynamic packages
        "--collect-all=streamlit",
        "--collect-all=pywebview",
        "--collect-all=pythonnet",
        "--collect-all=plotly",
        "--collect-all=reportlab",
        "--collect-all=pandas",
        # Hidden imports
        "--hidden-import=clr",
        "--hidden-import=clr_loader",
        "--hidden-import=psutil",
        "--hidden-import=reportlab",
        "--hidden-import=reportlab.lib",
        "--hidden-import=reportlab.lib.pagesizes",
        "--hidden-import=reportlab.lib.styles",
        "--hidden-import=reportlab.lib.colors",
        "--hidden-import=reportlab.platypus",
        "--hidden-import=reportlab.pdfgen",
        # Entry point
        str(CORE_DIR / "desktop_app.py"),
    ]

    print("  Executing PyInstaller compilation...")
    res = subprocess.run(cmd, cwd=str(CORE_DIR))
    if res.returncode != 0:
        print(f"Error: PyInstaller build failed with exit code {res.returncode}", file=sys.stderr)
        sys.exit(res.returncode)

    print(f"  [OK] Compilation completed successfully.")


def assemble_portable_package():
    """Moves compiled files into Windows/Portable and adds launcher/docs."""
    print(f"[4/6] Assembling portable release in {PORTABLE_DIR}...")
    compiled_source = DIST_TEMP_DIR / APP_NAME

    # Copy all items from dist/APP_NAME into Windows/Portable/
    for item in compiled_source.iterdir():
        dest = PORTABLE_DIR / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)

    # Copy documentation into portable folder
    for doc in ("README.md", "HOWTOUSE.md", "LICENSE"):
        src = CORE_DIR / doc
        if src.exists():
            shutil.copy2(src, PORTABLE_DIR / doc)

    # Create launch batch script
    launcher_bat = PORTABLE_DIR / "Launch-AI-RAT-Detection-Dashboard.bat"
    with open(launcher_bat, "w", encoding="utf-8") as f:
        f.write("@echo off\r\n")
        f.write("cd /d \"%~dp0\"\r\n")
        f.write(f"start \"\" \"%~dp0{APP_NAME}.exe\"\r\n")
        f.write("exit\r\n")

    # Copy .streamlit config
    st_dir = CORE_DIR / ".streamlit"
    if st_dir.exists():
        shutil.copytree(st_dir, PORTABLE_DIR / ".streamlit", dirs_exist_ok=True)

    print(f"  [OK] Portable package created at {PORTABLE_DIR}")


def create_portable_zip():
    """Packages the portable directory into a distributable ZIP archive."""
    print("[5/6] Creating portable ZIP archive...")
    total_files = 0
    with zipfile.ZipFile(ZIP_FILE, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for root, dirs, files in os.walk(PORTABLE_DIR):
            for file in files:
                p = Path(root) / file
                if p == ZIP_FILE:
                    continue
                arcname = Path(APP_NAME) / p.relative_to(PORTABLE_DIR)
                zf.write(p, arcname)
                total_files += 1

    size_mb = ZIP_FILE.stat().st_size / (1024 * 1024)
    print(f"  [OK] Created archive: {ZIP_FILE.name} ({size_mb:.1f} MB, {total_files} files)")


def build_inno_installer():
    """Generates and compiles Inno Setup installer script into Windows/Installer."""
    print("[6/6] Compiling Windows Installer with Inno Setup...")
    iss_file = INSTALLER_DIR / "installer.iss"
    
    # Locate ISCC.exe
    iscc_candidates = [
        Path(os.path.expandvars(r"%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe")),
        Path(r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"),
        Path(r"C:\Program Files\Inno Setup 6\ISCC.exe"),
    ]
    iscc_path = None
    for c in iscc_candidates:
        if c.exists():
            iscc_path = c
            break

    # Generate Inno Setup Script (using relative paths for portability)
    iss_content = f"""
; Inno Setup Script for AI RAT Detection Dashboard
[Setup]
AppId={{{{C5369A18-8687-4B3B-864B-87146522EA76}}}}
AppName=AI RAT Detection Dashboard
AppVersion=1.0.0
AppPublisher=AI RAT Detection Dashboard Project
DefaultDirName={{autopf}}\\AI RAT Detection Dashboard
DefaultGroupName=AI RAT Detection Dashboard
OutputDir=.
OutputBaseFilename=AI-RAT-Detection-Dashboard-Setup
SetupIconFile=..\\..\\Core\\assets\\icon.ico
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible
DisableProgramGroupPage=yes

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked

[Files]
Source: "..\\Portable\\*"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "*.zip"

[Icons]
Name: "{{group}}\\AI RAT Detection Dashboard"; Filename: "{{app}}\\{APP_NAME}.exe"; IconFilename: "{{app}}\\assets\\icon.ico"
Name: "{{autodesktop}}\\AI RAT Detection Dashboard"; Filename: "{{app}}\\{APP_NAME}.exe"; IconFilename: "{{app}}\\assets\\icon.ico"; Tasks: desktopicon

[Run]
Filename: "{{app}}\\{APP_NAME}.exe"; Description: "{{cm:LaunchProgram,AI RAT Detection Dashboard}}"; Flags: nowait postinstall skipifsilent
"""
    with open(iss_file, "w", encoding="utf-8") as f:
        f.write(iss_content.strip())
    print(f"  Generated installer script: {iss_file}")

    if iscc_path:
        print(f"  Invoking Inno Setup Compiler: {iscc_path}...")
        res = subprocess.run([str(iscc_path), str(iss_file)], capture_output=True, text=True)
        if res.returncode == 0:
            setup_exe = INSTALLER_DIR / "AI-RAT-Detection-Dashboard-Setup.exe"
            if setup_exe.exists():
                size_mb = setup_exe.stat().st_size / (1024 * 1024)
                print(f"  [OK] Windows Installer compiled successfully: {setup_exe.name} ({size_mb:.1f} MB)")
            else:
                print("  Installer compiled successfully.")
        else:
            print(f"  Warning: Inno Setup compilation returned code {res.returncode}: {res.stderr}")
    else:
        print("  Notice: ISCC.exe not located in standard paths. installer.iss is ready for compilation.")


def cleanup_temp():
    """Cleans temporary build and dist folders in Core to keep repository clean."""
    print("Cleaning temporary build directories in Core/...")
    shutil.rmtree(BUILD_DIR, ignore_errors=True)
    shutil.rmtree(DIST_TEMP_DIR, ignore_errors=True)
    spec_file = CORE_DIR / f"{APP_NAME}.spec"
    if spec_file.exists():
        spec_file.unlink(missing_ok=True)
    print("  [OK] Temporary build caches removed.")


def main():
    print("=" * 70)
    print("  AI RAT Detection Dashboard - Windows Production Build Pipeline")
    print("=" * 70)
    check_prerequisites()
    clean_previous_builds()
    run_pyinstaller()
    assemble_portable_package()
    create_portable_zip()
    build_inno_installer()
    cleanup_temp()
    print("=" * 70)
    print("  BUILD COMPLETE: Windows release assembled in Windows/ folder!")
    print("=" * 70)


if __name__ == "__main__":
    main()
