from __future__ import annotations

import sys
from pathlib import Path

# Ensure the in-repo Python package can be imported without installation.
REPO = Path(__file__).resolve().parents[1]
PYTHON_DIR = REPO / "python"
for candidate in (str(REPO), str(PYTHON_DIR)):
    if candidate not in sys.path:
        sys.path.insert(0, candidate)
