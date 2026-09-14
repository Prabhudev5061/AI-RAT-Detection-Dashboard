# Detection Rules Catalogue & Heuristic Specifications

This document defines the formal behavioral detection rules implemented within the AI-RAT-Detection-Dashboard.

---

## Detection Rules Table

| Rule ID | Rule Name | Severity | Risk Weight | Heuristic Description |
| :--- | :--- | :--- | :--- | :--- |
| `RULE_001` | **Executable in Suspicious Path** | HIGH | 30 | Process binary resides within writable user directories: `AppData\Local\Temp`, `AppData\Roaming`, `Windows\Temp`, `Users\Public`, `$Recycle.Bin`, or `ProgramData\Temp`. |
| `RULE_002` | **Known RAT / Backdoor Port Usage** | HIGH | 35 | Process socket binds to or establishes connections with ports historically associated with RATs, backdoors, or reverse shells (e.g. 4444, 5555, 1337, 31337, 1604, 1177, 65432). |
| `RULE_003` | **Suspicious Parent-Child Process Chain** | CRITICAL | 40 | A script interpreter or command shell (`cmd.exe`, `powershell.exe`, `wscript.exe`, `mshta.exe`) was spawned by an unexpected parent such as Microsoft Word, Excel, PowerPoint, Outlook, or `svchost.exe`. |
| `RULE_004` | **Abnormal Process Resource Consumption** | MEDIUM | 15 | Process CPU or RAM utilization spikes above 80.0%, indicating potential cryptomining, Denial of Service, or aggressive exfiltration. |
| `RULE_005` | **High Outbound Connection Burst** | MEDIUM | 25 | A single process maintains 10 or more concurrent external ESTABLISHED sockets, characteristic of botnet C2 polling, data exfiltration, or scanning. |
| `RULE_006` | **Suspicious Startup Persistence** | HIGH | 35 | Windows Registry Run key or Startup folder shortcut points to an executable residing in temporary, user-writable directories. |
| `RULE_007` | **Active Remote Access Software** | MEDIUM | 20 | Process name matches known remote desktop or remote management software (e.g., AnyDesk, TeamViewer, VNC Server, RustDesk). |

---

## Risk Scoring Formula

The aggregate host risk score is computed dynamically across all telemetry vectors:

$$\text{Composite Risk} = \min(100, \max(5, (\text{Max Process Score} \times 0.5) + (\text{Network Score} \times 0.3) + (\text{Startup Score} \times 0.2)))$$

- **LOW (0 – 24)**: Healthy host status. Routine processes.
- **MEDIUM (25 – 49)**: Minor anomalies or remote administration tools present.
- **HIGH (50 – 74)**: Elevated threat vector (suspicious paths, unexpected ports).
- **CRITICAL (75 – 100)**: Malicious process spawn or multiple compounding threat indicators.
