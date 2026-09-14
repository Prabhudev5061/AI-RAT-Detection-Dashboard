# HOWTOUSE - User and Operator Guide

This guide explains how to install, configure, operate, and troubleshoot the **AI RAT Detection Dashboard**.

---

## Table of Contents
1. [Prerequisites & System Requirements](#1-prerequisites--system-requirements)
2. [Installation](#2-installation)
3. [Starting the Application](#3-starting-the-application)
4. [Navigating the Dashboard Interface](#4-navigating-the-dashboard-interface)
5. [Understanding Dashboard Cards & Telemetry](#5-understanding-dashboard-cards--telemetry)
6. [Understanding Risk Levels & Threat Scoring](#6-understanding-risk-levels--threat-scoring)
7. [Using Live Monitor](#7-using-live-monitor)
8. [Using Process Analysis](#8-using-process-analysis)
9. [Using Network Monitor](#9-using-network-monitor)
10. [Using Defensive Security Tools](#10-using-defensive-security-tools)
11. [Event Logs & Auditing](#11-event-logs--auditing)
12. [Generating & Exporting Reports (CSV & PDF)](#12-generating--exporting-reports-csv--pdf)
13. [Application Settings & Refresh Intervals](#13-application-settings--refresh-intervals)
14. [Administrator Permissions & Elevation](#14-administrator-permissions--elevation)
15. [Troubleshooting & FAQs](#15-troubleshooting--faqs)
16. [Stopping the Application](#16-stopping-the-application)

---

## 1. Prerequisites & System Requirements
- **Operating System**: Windows 10 (64-bit), Windows 11, or Windows Server.
- **Python**: Version 3.10 through 3.14.
- **RAM**: Minimum 2 GB free memory.
- **Disk**: 200 MB free disk space for dependencies and logs.

---

## 2. Installation

1. Open PowerShell or Command Prompt.
2. Clone the repository and navigate into it:
   ```bash
   git clone https://github.com/<your-username>/AI-RAT-Detection-Dashboard.git
   cd AI-RAT-Detection-Dashboard
   ```
3. Create and activate your Python virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
4. Verify required packages are installed:
   ```powershell
   pip install -r requirements.txt
   ```

---

## 3. Starting the Application

### Option A: Standalone Windows Executable (Recommended for End Users)
If using the compiled standalone distribution:
1. Navigate to `dist/AI-RAT-Detection-Dashboard/`.
2. Double-click **`AI-RAT-Detection-Dashboard.exe`** (or `Launch-AI-RAT-Detection-Dashboard.bat`).
3. The application will launch in a native, hardware-accelerated Windows desktop window with no external dependencies required.

To build the executable from source at any time:
```powershell
python build_desktop.py
```

### Option B: Native Desktop Window via Python
To run the native desktop shell using Python:
```powershell
python desktop_app.py
```

### Option C: Browser / Server Mode
To launch the dashboard inside your default web browser:
```powershell
streamlit run app.py
```
Open your web browser to **`http://localhost:8501`**.

---

## 4. UI Theme Customization (Dark, Light, System)

The application supports three display themes:
- **Dark Mode**: High-density Security Operations Center (SOC) dark interface with glowing cyber accents and deep contrast.
- **Light Mode**: High-contrast, clean professional white interface designed for bright workspaces.
- **System Default**: Automatically syncs with your Windows system preference (light or dark).

### How to Switch Themes:
1. **From the Sidebar**: Locate the **🎨 UI Theme** dropdown in the navigation sidebar and select `Dark`, `Light`, or `System`.
2. **From Settings**: Navigate to **Settings** in the sidebar, choose your desired theme under **Appearance & Interface**, and click **💾 Save Preferences**.
3. All UI cards, sparklines, Plotly telemetry history graphs, and tables instantly adapt to the selected theme. Your choice is automatically persisted in `data/settings.json`.

---

## 4. Navigating the Dashboard Interface

The left sidebar provides one-click access to the main security modules:
- **Dashboard**: High-level SOC view with overview telemetry, sparklines, history graphs, and modular panels.
- **Live Monitor**: Granular real-time hardware gauges and network throughput rates.
- **Process Analysis**: Searchable inventory of all running processes with risk classification.
- **Network Monitor**: Active socket connections, remote IP mapping, and suspicious port flags.
- **Security Tools**: Startup program audits, hardware sensor privacy, and host diagnostics.
- **Event Logs**: Chronological security event table with severity filtering.
- **Reports**: On-demand generation of executive PDF reports and raw CSV telemetry tables.
- **Settings**: Adjust refresh intervals (3s, 5s, 10s, 30s) and prune database records.

---

## 5. Understanding Dashboard Cards & Telemetry

### Top Summary Cards:
- **CPU Usage**: Displays current host CPU utilization percentage and recent 15-point sparkline.
- **RAM Usage**: Displays current physical memory utilization percentage and sparkline.
- **Disk Usage**: Displays main system drive utilization (`C:\`).
- **Total Processes**: Displays current number of active system processes.

### Telemetry History Charts:
- Four synchronized Plotly graphs showing CPU %, RAM %, Disk %, and Network Throughput (Bytes Sent/Received per second).

### Grid Panels:
- **Top Active Processes**: Highlights the highest CPU-consuming executables.
- **Startup Programs**: Audits Windows Registry `Run` keys and user startup directories.
- **Parent-Child Process Relationship**: Visualizes execution chains to spot anomalous command spawns.
- **Active Network Connections**: Shows current TCP/UDP sockets and remote IPs.
- **Suspicious Port Detection**: Flags any socket bound to known RAT or backdoor ports.
- **Security Status**: Defensive sensor auditing for Camera, Microphone, Screen Recording, and Remote Administration Tools.
- **AI Prediction**: Rule-based threat verdict with circular risk score gauge (0–100%).
- **Event Timeline**: Recent security events categorized by severity.
- **AI Recommendations**: Actionable security hardening steps tailored to detected conditions.

---

## 6. Understanding Risk Levels & Threat Scoring

The risk engine computes an explainable score between **0 and 100**:

| Level | Score Range | Color | Meaning |
| :--- | :--- | :--- | :--- |
| **LOW** | 0 – 24 | Emerald Green | Clean system behavior; routine background processes. |
| **MEDIUM** | 25 – 49 | Yellow / Amber | Minor anomalies, high resource bursts, or remote tool activity. |
| **HIGH** | 50 – 74 | Orange | Suspicious paths (e.g. Temp/AppData), unknown backdoors, or anomalous spawns. |
| **CRITICAL** | 75 – 100 | Vivid Red | Multiple compounded indicators or known RAT communication ports. |

> **Transparency Note**: The dashboard never makes unsubstantiated claims. Every elevated score includes specific forensic reasons (e.g., *Executable located in AppData\Local\Temp*).

---

## 7. Using Live Monitor
Navigate to **Live Monitor** in the sidebar. This page displays continuous resource allocation details, including exact memory usage in gigabytes, storage capacity breakdowns, and real-time network traffic throughput.

---

## 8. Using Process Analysis
Navigate to **Process Analysis**:
- Use the **Filter by Process Name or PID** text box to search for any running program.
- If elevated risk processes exist, an alert banner will highlight them at the top of the page.
- Inspect the full directory path to verify if an executable is located in legitimate folders (`Program Files`, `System32`) or suspicious writable locations (`Temp`, `AppData`).

---

## 9. Using Network Monitor
Navigate to **Network Monitor**:
- Use the **Filter by Socket State** dropdown to filter for `ESTABLISHED` connections or listening ports (`LISTEN`).
- Any connections utilizing known suspicious RAT ports (e.g., 4444, 5555, 3389, 5900) will appear highlighted in the red threat banner.

---

## 10. Using Defensive Security Tools
Navigate to **Security Tools**:
- **Startup Programs Audit**: Review all applications configured to launch on Windows startup. Look out for unverified binaries or unusual script extensions (`.vbs`, `.bat`).
- **Sensor Privacy Telemetry**: Check whether any background application currently holds an active camera or microphone stream.
- **Host Diagnostics**: Review local machine names, username context, and privilege boundaries.

---

## 11. Event Logs & Auditing
Navigate to **Event Logs**:
- Filter by severity: `ALL`, `INFO`, `WARNING`, `HIGH`, `CRITICAL`.
- Adjust the **Max Events** slider to retrieve up to 200 historical events from the local SQLite database.

---

## 12. Generating & Exporting Reports (CSV & PDF)
Navigate to **Reports**:
1. **Executive PDF Report**: Click **Generate & Download PDF Report**. The application generates a publication-ready PDF document including threat scores, active process lists, suspicious ports, and recommendations. Once generated, click **⬇️ Download Generated PDF**.
2. **Metrics CSV Export**: Click **⬇️ Export Metrics History (CSV)** to download historical hardware telemetry.
3. **Events CSV Export**: Click **⬇️ Export Event Logs (CSV)** to download the complete event log.

---

## 13. Application Settings & Refresh Intervals
Navigate to **Settings**:
- Adjust the **Auto Refresh Interval** (default is 5 seconds).
- Click **🧹 Prune Historical Database Records** to clean older telemetry entries while preserving recent records.

---

## 14. Administrator Permissions & Elevation
- When started as a standard user, the dashboard displays **⚠️ Standard User** in the sidebar. Standard monitoring functions normally, but certain core Windows processes (e.g., PID 4 `System`, `svchost.exe`) will display `[Access Denied (Requires Admin)]` for their binary path.
- To enable complete inspection of all system processes:
  1. Right-click PowerShell and choose **Run as Administrator**.
  2. Start the dashboard from that elevated terminal.
  3. The sidebar will indicate **🛡️ Elevated (Admin)**.

---

## 15. Troubleshooting & FAQs

### Q: The port 8501 is already in use.
**A**: Specify an alternative port when launching:
```powershell
streamlit run app.py --server.port 8502
```

### Q: Why does Camera or Microphone show "Monitoring limited"?
**A**: Certain versions of Windows or custom security policies restrict non-system processes from querying the CapabilityAccessManager registry key. The application reports "Monitoring limited" rather than giving a false positive or false negative.

### Q: How do I run automated unit tests?
**A**: Execute:
```powershell
python -m pytest tests/ -v
```

---

## 16. Stopping the Application
In the terminal where Streamlit is running, press **`Ctrl + C`** to gracefully shut down the server.

