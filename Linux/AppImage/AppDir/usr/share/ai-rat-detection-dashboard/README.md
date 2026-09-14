# AI RAT Detection Dashboard

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)
![Platform: Windows | Linux](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-blue.svg)
![Release: v1.0.0](https://img.shields.io/badge/Release-v1.0.0-emerald.svg)

A professional, production-grade cross-platform cyber security monitoring suite and Remote Access Trojan (RAT) behavioral detection dashboard. Provides real-time host hardware metrics (CPU, RAM, GPU, Disk, Network I/O), process execution tree analysis, unauthorized socket detection, defensive sensor auditing, and automated forensic reporting.

---

## 1. Project Structure

The project strictly follows a unified three-folder architecture:

```text
AI-RAT-Detection-Dashboard/
│
├── Core/                               # SINGLE MASTER SOURCE CODEBASE
│   ├── app.py                          # Streamlit UI application entrypoint
│   ├── desktop_app.py                  # Standalone native desktop container (pywebview)
│   ├── build_windows.py                # Windows Portable & Inno Setup installer builder
│   ├── build_linux.py                  # Linux AppImage & Debian package builder
│   ├── requirements.txt                # Production Python dependencies
│   ├── assets/                         # Application icons, logos, and bundled offline fonts
│   │   ├── icon.ico                    # Windows icon
│   │   ├── icon.png                    # Linux / Freedesktop icon
│   │   └── fonts/                      # Offline JetBrains Mono font family (Regular & Bold)
│   ├── platforms/                      # Hardware & OS abstraction layer
│   │   ├── base.py                     # BasePlatformAdapter interface
│   │   ├── windows.py                  # Windows Registry, UAC, GPU & sensor adapter
│   │   └── linux.py                    # Linux XDG Autostart, DRM/sysfs GPU & rootless sensor adapter
│   ├── monitoring/                     # Hardware, process, socket & startup collectors
│   ├── detection/                      # Multi-layer behavioral and heuristic threat engines
│   ├── services/                       # Decoupled background telemetry coordinator & PDF reports
│   ├── ui/                             # Dashboard views, cards, charts, and CSS theme engine
│   ├── database/                       # Embedded SQLite storage with automatic pruning
│   ├── config/                         # Configuration and persistent settings manager
│   ├── utils/                          # Formatting, elevation, and helper utilities
│   └── tests/                          # 31/31 Automated pytest suite
│
├── Windows/                            # WINDOWS PRODUCTION BUILDS ONLY
│   ├── Portable/
│   │   ├── AI-RAT-Detection-Dashboard.exe
│   │   ├── Launch-AI-RAT-Detection-Dashboard.bat
│   │   └── AI-RAT-Detection-Dashboard-Windows-x64.zip
│   └── Installer/
│       ├── AI-RAT-Detection-Dashboard-Setup.exe
│       └── installer.iss               # Inno Setup compilation recipe
│
└── Linux/                              # LINUX PRODUCTION BUILDS ONLY
    ├── AppImage/
    │   ├── AI-RAT-Detection-Dashboard.AppImage
    │   ├── build_appimage.sh
    │   └── AppDir/                     # Self-contained Freedesktop AppDir bundle
    └── Debian/
        ├── ai-rat-detection-dashboard.deb
        ├── build_deb.sh
        └── package/                    # Debian control and system hierarchy
```

---

## 2. Development Setup

### Prerequisites
- **Python**: Version 3.10, 3.11, 3.12, 3.13, or 3.14.
- **Git**

### Installation
```bash
# Clone the repository
git clone https://github.com/your-org/AI-RAT-Detection-Dashboard.git
cd AI-RAT-Detection-Dashboard/Core

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux:
source .venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

### Running in Development Mode
```bash
# Option A: Run native desktop window application
python desktop_app.py

# Option B: Run web dashboard directly
streamlit run app.py
```

### Running Automated Test Suite
```bash
pytest tests/
```

---

## 3. Production Build Instructions

### Windows Build Pipeline
From `Core/`, run:
```powershell
python build_windows.py
```
This automatically:
1. Compiles the standalone executable `AI-RAT-Detection-Dashboard.exe` via PyInstaller.
2. Assembles the ready-to-run folder `Windows/Portable/` with `Launch-AI-RAT-Detection-Dashboard.bat`.
3. Creates the distributable archive `Windows/Portable/AI-RAT-Detection-Dashboard-Windows-x64.zip`.
4. Compiles the native Windows installer `Windows/Installer/AI-RAT-Detection-Dashboard-Setup.exe` using Inno Setup (`ISCC.exe`).

### Linux Build Pipeline
From `Core/`, run:
```bash
python3 build_linux.py
```
This automatically:
1. Assembles `Linux/AppImage/AppDir/` with `AppRun`, desktop entry, and `AI-RAT-Detection-Dashboard.AppImage`.
2. Generates the standard Debian package tree in `Linux/Debian/package/` and produces `Linux/Debian/ai-rat-detection-dashboard.deb`.

---

## 4. Key Architectural Highlights

### Low-CPU Telemetry Engine
To solve the common CPU spike issue associated with continuous system polling:
- Telemetry harvesting is decoupled from UI rendering into a dedicated background worker thread (`services/monitoring_service.py`).
- Tiered sampling rates:
  - **Tier 1 (3s)**: Lightweight CPU, RAM, Disk, and Network I/O metrics.
  - **Tier 2 (10s)**: Process enumeration, socket correlation, and threat scoring.
  - **Tier 3 (60s)**: Registry/XDG startup persistence and security sensor checks.
  - **Tier 4 (300s)**: Historical database pruning.
- Read operations from the UI query in-memory snapshot caches in `< 0.1ms`.

### Cross-Platform Hardware Abstraction (`platforms/`)
- **Windows**: Queries Registry persistence (`HKCU\Run`, `HKLM\Run`), audits Windows Event Logs, monitors camera/mic activity via `CapabilityAccessManager`, checks UAC elevation via `IsUserAnAdmin`, and monitors NVIDIA/DXGI GPUs.
- **Linux**: Scans standard XDG Autostart directories (`~/.config/autostart`, `/etc/xdg/autostart`), monitors DRM/sysfs graphics interfaces (`/sys/class/drm`) and `nvidia-smi`, audits video devices rootlessly, and operates with zero root/sudo dependency for standard telemetry.

### 100% Offline JetBrains Mono Typography
- JetBrains Mono (`Regular` and `Bold` TTF) is bundled locally inside `assets/fonts/`.
- Embedded as Base64 data URIs inside the CSS engine (`ui/styles.py`), guaranteeing immediate high-legibility rendering in fully air-gapped environments without external web font requests.

### Multi-Mode Theme System
- Complete CSS variable engine supporting:
  - **Dark Mode**: Cyber SOC-grade high-contrast slate palette (`#0b0f19` background).
  - **Light Mode**: Crisp, ergonomic corporate theme (`#f8fafc` background).
  - **System Mode**: Dynamically synchronizes with the OS appearance.
- User theme choice is persisted across sessions in `data/settings.json`.

---

## 5. Troubleshooting & FAQ

| Issue | Resolution |
| :--- | :--- |
| **Port Conflict (8501 in use)** | The desktop launcher automatically scans and binds the next available port up to 8600. |
| **WebView2 Not Found on Windows** | `desktop_app.py` detects missing WebView2 runtimes and falls back to Microsoft Edge / Chrome in Windows App Mode (`--app=http://127.0.0.1:port`). |
| **Permission Denied on Process Inspection** | Elevated processes (system services) restrict telemetry access for standard users. Launch as Administrator / root to inspect system-owned processes. |

---

## 6. License
Distributed under the MIT License. See [LICENSE](LICENSE) for details.
