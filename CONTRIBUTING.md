# Contributing to AI RAT Detection Dashboard

Thank you for your interest in contributing to the **AI RAT Detection Dashboard**! We welcome contributions that improve host defense, forensic accuracy, cross-platform stability, and telemetry performance.

---

## Code of Conduct
Please review and adhere to our [Code of Conduct](CODE_OF_CONDUCT.md) in all project interactions.

---

## Development Setup

The project is structured into three primary directories:
- `Core/`: Master Python source code, tests, and build scripts.
- `Windows/`: Windows production installer and portable packages.
- `Linux/`: Linux AppImage and Debian packages.

### Setting Up the Core Environment

1. **Fork and Clone** the repository:
   ```bash
   git clone https://github.com/<your-username>/ai-rat-detection-dashboard.git
   cd ai-rat-detection-dashboard/Core
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv .venv
   # Windows:
   .\.venv\Scripts\Activate.ps1
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   # Standalone Desktop App (pywebview):
   python desktop_app.py
   
   # Or browser mode (Streamlit directly):
   python -m streamlit run app.py
   ```

5. **Run the Test Suite**:
   ```bash
   pytest tests/ -v
   ```

---

## Pull Request Guidelines

1. Create a dedicated feature branch:
   ```bash
   git checkout -b feature/improvement-name
   ```
2. Ensure all changes are made inside `Core/`. Never directly edit generated files in `Windows/` or `Linux/`.
3. Verify that all 33+ automated tests pass with `pytest tests/ -v`.
4. Ensure CPU efficiency guidelines are maintained: monitoring telemetry must remain non-blocking and idle CPU usage must stay below 10%.
5. Adhere to defensive programming principles (e.g., graceful handling of `psutil.AccessDenied` and `psutil.NoSuchProcess`).
6. Submit your PR using the repository pull request template with a concise explanation and validation evidence.
