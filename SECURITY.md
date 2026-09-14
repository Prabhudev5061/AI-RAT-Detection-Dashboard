# Security Policy

## Defensive Monitoring Purpose
The **AI RAT Detection Dashboard** is designed strictly as a defensive host security auditing, telemetry visualization, and educational threat analysis platform.

It does **NOT** contain or support offensive capabilities:
- No remote code execution or command injection mechanisms
- No credential harvesting, keylogging, or screen scraping
- No packet injection, network tampering, or payload delivery
- No unauthorized persistence installation

All monitoring operations read standard operating system metrics, socket tables, and process metadata through standard OS APIs and Python's `psutil` library.

---

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

---

## Reporting a Vulnerability

If you discover a security vulnerability or unintended privilege leak in this project:
1. Please do **NOT** open a public GitHub issue.
2. Report the vulnerability privately via GitHub Security Advisories or by emailing project maintainers.
3. Include:
   - Description of the issue
   - Clear steps to reproduce safely
   - Potential impact on host security or system stability
4. Maintainers will review, triage, and patch the issue promptly.
