"""
AI RAT Detection Dashboard - Global Pytest Configuration and Path Setup
Ensures the Core master source directory is automatically discovered on sys.path
across all test execution environments (local, CLI, and GitHub Actions CI).
"""

import sys
from pathlib import Path

# Explicitly ensure Core directory is first in sys.path
CORE_DIR = Path(__file__).resolve().parent
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))
