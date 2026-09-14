# Contributing to AI RAT Detection Dashboard

Thank you for your interest in contributing to the **AI RAT Detection & System Network Monitoring Dashboard**! We welcome contributions that improve host defense, forensic accuracy, and telemetry performance.

---

## Code of Conduct
We expect all contributors to maintain a respectful, welcoming, and harassment-free environment for everyone.

---

## Development Setup

1. **Fork and Clone** the repository:
   ```bash
   git clone https://github.com/<your-username>/ai-rat-detection-dashboard.git
   cd ai-rat-detection-dashboard/Core
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .\.venv\Scripts\Activate.ps1
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Tests**:
   ```bash
   pytest tests/ -v
   ```

---

## Pull Request Guidelines

1. Create a dedicated feature branch:
   ```bash
   git checkout -b feature/my-feature-name
   ```
2. Ensure all existing tests pass and add unit tests for new functionality in `tests/`.
3. Adhere to defensive programming principles (handle `psutil.AccessDenied`, `psutil.NoSuchProcess`).
4. Avoid introducing large heavy frontend frameworks or unnecessary dependencies.
5. Submit your PR with a clear summary of changes and validation steps.
