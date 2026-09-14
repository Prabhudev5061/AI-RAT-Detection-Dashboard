# Troubleshooting & Operational Resolution Guide

## 1. Port 8501 Already in Use
**Symptom**: Streamlit fails to start, displaying an error that port 8501 is bound by another service.  
**Resolution**: Run Streamlit specifying an explicit alternate port:
```powershell
streamlit run app.py --server.port 8502
```

---

## 2. Process Binary Path Shows `[Access Denied (Requires Admin)]`
**Symptom**: Certain Windows core processes (e.g. `System`, `Registry`, `svchost.exe`, `csrss.exe`) display `[Access Denied]` in the executable path column.  
**Explanation**: Windows NT kernel prevents non-elevated user accounts from opening process handles with `PROCESS_QUERY_INFORMATION` rights for system-level tokens.  
**Resolution**:
1. Open PowerShell by right-clicking and selecting **Run as Administrator**.
2. Run `streamlit run app.py`.
3. The dashboard will automatically detect elevation and display **Elevated (Admin)** in the sidebar, granting full access to privileged paths.

---

## 3. SQLite Database Locked Error (`database is locked`)
**Symptom**: Intermittent `sqlite3.OperationalError: database is locked`.  
**Explanation**: High write concurrency on non-WAL SQLite databases.  
**Resolution**:
- The application automatically initializes the database with `PRAGMA journal_mode=WAL;` and a 10.0-second timeout.
- If running multiple instances on the same file, ensure background processes do not hold uncommitted transactions.
- You can prune database records via the **Settings** menu.

---

## 4. Scapy / Raw Packet Capture Permissions
**Symptom**: Scapy warnings or failure to capture raw promiscuous packets.  
**Explanation**: Windows requires Npcap (or WinPcap) with Administrator elevation for raw layer-2 packet sniffing.  
**Resolution**:
- The application relies primarily on native Windows socket telemetry via `psutil.net_connections`, which requires no external drivers or kernel packet filters.
- Scapy is utilized defensively where supported, falling back gracefully to socket-level telemetry if Npcap is absent.

---

## 5. Camera / Microphone Status Shows "Monitoring limited"
**Symptom**: Sensor indicators display "Monitoring limited".  
**Explanation**: Windows Privacy consent keys (`CapabilityAccessManager\ConsentStore`) may be restricted by Group Policy or corporate endpoint protection.  
**Resolution**:
- This is by design: the dashboard will never fabricate a false "Clean" report when telemetry is restricted. Running as Administrator may grant read access to restricted HKLM subkeys.
