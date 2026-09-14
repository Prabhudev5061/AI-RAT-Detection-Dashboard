# System Architecture & Technical Design

## 1. Architectural Overview
The **AI RAT Detection Dashboard** is built around an asynchronous-capable, decoupled pipeline designed for Windows hosts. It is divided into five core layers:

```
+-------------------------------------------------------------+
|                      Streamlit Web UI                       |
|   (Dashboard, Live Monitor, Processes, Network, Reports)   |
+-------------------------------------------------------------+
                              |
+-------------------------------------------------------------+
|                     Monitoring Service                      |
|           (Coordinator, Event Trigger, Dispatcher)          |
+-------------------------------------------------------------+
           |                      |                      |
+--------------------+ +--------------------+ +--------------------+
|   System Monitor   | |  Process Monitor   | |  Network Monitor   |
| (CPU, RAM, Disk, IO)| | (Tree, Paths, PIDs) | |(Sockets, RAT Ports)|
+--------------------+ +--------------------+ +--------------------+
           |                      |                      |
+-------------------------------------------------------------+
|                      Detection Engine                       |
|      (Rules Catalogue, Process Analyzer, Network Analyzer)  |
+-------------------------------------------------------------+
                              |
+-------------------------------------------------------------+
|                     Data & Persistence                      |
|         (SQLite3 WAL Engine, ReportLab PDF, CSV Engine)     |
+-------------------------------------------------------------+
```

---

## 2. Core Components

### A. Monitoring Subsystem (`monitoring/`)
- **SystemMonitor**: Samples hardware metrics using `psutil`. Collects total CPU utilization percentage, virtual memory breakdown, storage consumption on system root, process counts, and aggregate network I/O bytes.
- **ProcessMonitor**: Uses `psutil.process_iter` with defensive exception handling (`NoSuchProcess`, `AccessDenied`, `ZombieProcess`). Maps parent-child PID associations into an in-memory graph.
- **NetworkMonitor**: Samples IPv4/IPv6 TCP and UDP sockets using `psutil.net_connections(kind="inet")`. Resolves remote IP endpoints and correlates sockets to process names.
- **StartupMonitor**: Queries Windows Registry Run subkeys (`HKCU\Run`, `HKLM\Run`, `RunOnce`) via Python's native `winreg` library and audits startup folders.
- **BehaviorMonitor**: Interrogates Windows `CapabilityAccessManager\ConsentStore` registry entries to check active hardware streams for webcams and microphones without intrusive kernel hooks.

### B. Detection & Risk Subsystem (`detection/`)
- **Detection Rules (`rules.py`)**: Central repository of detection heuristics, severities, and weights.
- **ProcessAnalyzer (`process_analyzer.py`)**: Evaluates process paths against suspicious temporary and user-writable locations, checks for anomalous process hierarchies (e.g. Office applications spawning command shells), and inspects resource consumption.
- **NetworkAnalyzer (`network_analyzer.py`)**: Audits socket ports against a known signature catalogue of RAT/C2 ports (e.g. 4444, 5555, 3389, 5900, 1337) and detects high-volume outbound socket bursts.
- **RiskEngine (`risk_engine.py`)**: Computes a unified 0–100 composite risk score. Includes an extensible `.predict()` interface for future integration of pre-trained machine learning models.

### C. Alert & Logging Subsystem (`services/`)
- **AlertService**: Implements state-based deduplication and configurable cooldown timers (default 60s) to prevent repetitive alerts for ongoing background processes.
- **LoggingService**: Standard Python logging with rotating file handlers (5 MB chunks) and immediate SQLite table persistence.

### D. Data Storage (`database/`)
- **SQLite3 Database**: Operates in Write-Ahead Logging (WAL) mode with `PRAGMA synchronous = NORMAL`.
- **Optimization**: Indexes on `timestamp`, `severity`, and `risk_level` ensure fast queries even when querying across thousands of telemetry points.
- **Pruning Engine**: Bounded data retention automatically caps tables to 5,000 records.

### E. Reporting Pipeline (`services/report_service.py`)
- **CSV Generator**: Exports metric and event tables as comma-separated values.
- **ReportLab PDF Engine**: Compiles styled executive reports including color-coded risk assessment cards, process listings, network connection tables, and security recommendations.
