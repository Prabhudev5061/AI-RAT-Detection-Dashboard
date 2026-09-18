# Core Master Engine — Developer Technical Guide

The `Core/` directory is the **SINGLE MASTER SOURCE CODEBASE** for the AI RAT Detection Dashboard. All features, threat detection heuristics, telemetry collectors, and platform adapters reside here. The `Windows/` and `Linux/` directories are release distributions generated from this master source.

---

## 1. System Architecture

```text
+-----------------------------------------------------------------------------+
|                          DESKTOP RUNTIME CONTAINER                          |
|                             (desktop_app.py)                                |
|   +---------------------------------------------------------------------+   |
|   |                  pywebview Native Desktop Window                    |   |
|   |            (8 Visual Themes via local Streamlit port)               |   |
|   +---------------------------------------------------------------------+   |
+--------------------------------------|--------------------------------------+
                                       | HTTP / WebSocket
+--------------------------------------v--------------------------------------+
|                           STREAMLIT UI ENGINE                               |
|                                (app.py)                                     |
|   +---------------------------------------------------------------------+   |
|   | UI Components (ui/dashboard, ui/cards, ui/charts, ui/tables)        |   |
|   | Theme & Font Injection (ui/styles.py, JetBrains Mono TTF/CSS)       |   |
|   +---------------------------------------------------------------------+   |
+--------------------------------------|--------------------------------------+
                                       | Real-time state query
+--------------------------------------v--------------------------------------+
|                       CENTRAL TELEMETRY COORDINATOR                         |
|                     (services/monitoring_service.py)                        |
|   - Multi-threaded tiered collection daemon (Fast: 1s, Normal: 2s, Slow: 5s) |
|   - Non-blocking microsecond cache snapshots (Host CPU idle < 1%)           |
|   - atexit clean daemon termination handler                                 |
+-------------------|-------------------|-------------------|-----------------+
                    |                   |                   |
                    v                   v                   v
+-----------------------+ +-----------------------+ +-----------------------+
|  MONITORING ENGINE    | |   DETECTION ENGINE    | |   PLATFORM ADAPTERS   |
| (monitoring/*)        | | (detection/*)         | | (platforms/*)         |
| - SystemMonitor (CPU) | | - ProcessAnalyzer     | | - BasePlatformAdapter |
| - ProcessMonitor      | | - NetworkAnalyzer     | | - WindowsPlatform     |
| - NetworkMonitor      | | - RiskEngine          | | - LinuxPlatform       |
| - BehaviorMonitor     | | - Declarative Rules   | | (GPU, sensors, UAC,   |
| - StartupMonitor      | | (MITRE ATT&CK maps)   | |  registry, XDG, etc.) |
+-----------------------+ +-----------------------+ +-----------------------+
                    |                   |                   |
                    +-------------------+-------------------+
                                        |
                                        v
+-----------------------------------------------------------------------------+
|                              DATA & PERSISTENCE                             |
|                                                                             |
|   +-------------------------+                     +---------------------+   |
|   | SQLite Database Engine  |                     | PDF & CSV Reports   |   |
|   | (database/db.py)        |                     | (report_service.py) |   |
|   | - Schema: alerts, logs, |                     | - ReportLab PDF     |   |
|   |   telemetry, settings   |                     | - CSV exports       |   |
|   | - Auto-retention prune  |                     |                     |   |
|   +-------------------------+                     +---------------------+   |
+-----------------------------------------------------------------------------+
```

---

## 2. Directory & Component Breakdown

```text
Core/
├── app.py                          # Streamlit application entrypoint & tab router
├── desktop_app.py                  # Standalone pywebview native window launcher
├── build_windows.py                # Standalone Windows Portable & Inno Setup builder
├── build_linux.py                  # Linux AppImage & Debian package builder
├── requirements.txt                # Production dependency manifest
│
├── assets/                         # Application branding and offline fonts
│   ├── icon.ico                    # Windows icon (multi-resolution 16x16 to 256x256)
│   ├── icon.png                    # Linux / Freedesktop icon
│   └── fonts/                      # Offline JetBrains Mono & JetBrains Mono Nerd Font (TTF)
│
├── config/                         # Configuration management
│   ├── app_config.py               # Singleton configuration provider
│   └── settings.py                 # Persistent settings dataclass
│
├── database/                       # Embedded persistent storage
│   ├── db.py                       # SQLite connection pool and transaction manager
│   └── schema.sql                  # Relational schema (alerts, logs, telemetry, metrics)
│
├── detection/                      # Behavioral detection heuristics & rules
│   ├── process_analyzer.py         # Process hierarchy, masquerading & anomaly analysis
│   ├── network_analyzer.py         # Socket forensics, beaconing & reverse shell checks
│   ├── risk_engine.py              # Composite risk score calculation (0-100 scale)
│   └── rules.py                    # Declarative threat signatures with MITRE mappings
│
├── monitoring/                     # Hardware and system telemetry probes
│   ├── system_monitor.py           # CPU, RAM, Disk, Swap & Network counters
│   ├── process_monitor.py          # Process enumeration and snapshot generation
│   ├── network_monitor.py          # Active TCP/UDP socket collector
│   ├── behavior_monitor.py         # Screen, keystroke and sensor auditing probes
│   └── startup_monitor.py          # Persistence, Registry and Autostart inspection
│
├── platforms/                      # Hardware & OS abstraction layer
│   ├── __init__.py                 # Dynamic adapter factory (get_platform_adapter())
│   ├── base.py                     # BasePlatformAdapter abstract base class
│   ├── windows.py                  # Windows-specific implementation (Registry, UAC, GPU)
│   └── linux.py                    # Linux-specific implementation (XDG, sysfs, WebKit)
│
├── services/                       # Cross-cutting application services
│   ├── monitoring_service.py       # Decoupled tiered background telemetry worker
│   ├── alert_service.py            # Real-time alert dispatch and history tracking
│   ├── logging_service.py          # Structured forensic log manager
│   └── report_service.py           # ReportLab PDF generator and CSV exporter
│
├── ui/                             # User interface presentation components
│   ├── dashboard.py                # Main dashboard view orchestrator
│   ├── cards.py                    # Metric card widgets and summary chips
│   ├── charts.py                   # Plotly charts (time series, radar, gauge)
│   ├── tables.py                   # Filterable data tables with action buttons
│   ├── sidebar.py                  # Navigation sidebar and status indicators
│   └── styles.py                   # 8 Theme stylesheets (Obsidian, Light, Cyberpunk, Matrix, etc.)
│
├── utils/                          # Cross-platform utility functions
│   ├── formatting.py               # Human-readable byte, speed, and time formatters
│   ├── helpers.py                  # Process name sanitizers and platform utilities
│   └── permissions.py              # Privilege check and elevation helpers
│
└── tests/                          # Automated unit and integration test suite (41 tests)
    ├── test_database.py            # SQLite schema, transactions and pruning tests (5 tests)
    ├── test_detection.py           # Threat heuristic and risk scoring tests (6 tests)
    ├── test_lifecycle.py           # Telemetry service lifecycle and monitor tests (2 tests)
    ├── test_monitoring.py          # Telemetry collection and caching tests (7 tests)
    ├── test_platforms.py           # Platform adapter interface and method tests (7 tests)
    ├── test_reports.py             # PDF generation and CSV export tests (2 tests)
    └── test_theme_and_config.py    # Nerd font, 8 themes, contrast & settings tests (12 tests)
```

---

## 3. Communication & Data Flow

1. **Telemetry Collection**:
   - `MonitoringService` runs as a daemon thread.
   - It maintains **tiered background loops**:
     - *Fast Loop (1.0s)*: System CPU, RAM, active network rates.
     - *Normal Loop (2.0s)*: Process table enumeration and socket states.
     - *Slow Loop (5.0s)*: Hardware temperatures, disk space, and startup persistence.
   - Snapshots are cached in memory protected by threading locks. When the UI polls `get_latest_metrics()`, it returns in **< 1 millisecond** without blocking on system calls.

2. **Detection & Risk Evaluation**:
   - Process snapshots from `ProcessMonitor` are passed to `ProcessAnalyzer`.
   - Socket tables from `NetworkMonitor` are passed to `NetworkAnalyzer`.
   - Heuristic results are evaluated against declarative rules in `rules.py`.
   - `RiskEngine` compiles scores across 4 vectors:
     - Process Risk (0-30 pts)
     - Network Risk (0-30 pts)
     - Persistence Risk (0-20 pts)
     - Behavioral/Sensor Risk (0-20 pts)
   - If composite risk exceeds thresholds (Low: 25, Medium: 50, High: 75), `AlertService` triggers an alert and logs to SQLite.

3. **Presentation & Interactivity**:
   - `desktop_app.py` launches a local Streamlit server in a background thread and embeds it inside a native `pywebview` window.
   - Streamlit scripts run reactively; user actions (e.g. killing a suspicious process or generating a PDF) invoke service methods directly.

---

## 4. Platform Abstraction Layer (`platforms/`)

To guarantee clean separation between operating systems:
- All platform interactions must subclass `BasePlatformAdapter` (`platforms/base.py`).
- Use `get_platform_adapter()` to obtain the runtime adapter.

| Method | Windows (`windows.py`) | Linux (`linux.py`) |
| :--- | :--- | :--- |
| `get_gpu_info()` | Queries WMI / DXGI / nvidia-smi | Reads `/sys/class/drm` / nvidia-smi |
| `get_startup_items()` | Inspects Registry Run keys & Startup | Reads `~/.config/autostart` & `/etc/xdg` |
| `get_hardware_temperatures()` | OpenHardwareMonitor / WMI sensor API | Reads `/sys/class/thermal` & `sensors` |
| `is_admin()` | `ctypes.windll.shell32.IsUserAnAdmin()` | `os.geteuid() == 0` |
| `request_admin()` | `ShellExecuteExW` with `runas` | `pkexec` / `sudo` elevation prompt |

---

## 5. Developer Rules & Best Practices

1. **No External AI Runtime Dependencies**:
   - The application must remain fully functional offline. Do not add runtime calls to LLM APIs, cloud models, or local inference servers.
2. **Defensive Error Handling**:
   - Operating system and process queries must always catch `psutil.NoSuchProcess`, `psutil.AccessDenied`, and `psutil.ZombieProcess`.
3. **Telemetry Performance**:
   - Never perform blocking disk I/O, heavy subprocess forks, or network DNS lookups inside the UI rendering loop. Delegate all polling to background workers.
4. **Master Source Integrity**:
   - Always commit changes inside `Core/`. Do not manually edit files in `Windows/` or `Linux/`.

---

## 6. How to Run Tests

The test suite requires no external hardware or elevated privileges:

```bash
# Run all tests with short traceback
pytest tests/ -v --tb=short

# Run with coverage report
pytest tests/ --cov=. --cov-report=term-missing
```

---

## 7. How to Build Distributions

### Building for Windows:
```bash
python build_windows.py
```
- Output: `Windows/Portable/AI-RAT-Detection-Dashboard.exe` and `Windows/Installer/AI-RAT-Detection-Dashboard-Setup.exe`.

### Building for Linux:
```bash
python build_linux.py
```
- Output: `Linux/AppImage/AI-RAT-Detection-Dashboard.AppImage` and `Linux/Debian/ai-rat-detection-dashboard.deb`.
