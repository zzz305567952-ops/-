"""Shared pytest configuration for offline-friendly test runs.

The execution environment used by the agent may not have access to PyPI.  These
helpers keep the repository root importable and let individual test modules skip
cleanly when optional runtime dependencies are not installed.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
