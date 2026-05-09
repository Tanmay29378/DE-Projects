"""
Strip notebook outputs and replace known ADLS storage account names with a placeholder
for safe public GitHub hosting.

Run from repo root:
  python spark_project_ecommerce/spark_project_ecommerce/tools/scrub_notebooks.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Valid Azure storage account shape (3–24 lowercase alphanumeric).
PLACEHOLDER_ACCOUNT = "yourstorageacct"

REPLACEMENTS: tuple[tuple[str, str], ...] = (
    ("ecommcistorage05", PLACEHOLDER_ACCOUNT),
    ("stgcodebadlsdevus001", PLACEHOLDER_ACCOUNT),
)


def _scrub_strings(obj):
    if isinstance(obj, dict):
        return {k: _scrub_strings(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_scrub_strings(v) for v in obj]
    if isinstance(obj, str):
        s = obj
        for old, new in REPLACEMENTS:
            s = s.replace(old, new)
        return s
    return obj


def scrub_notebook(path: Path) -> None:
    nb = json.loads(path.read_text(encoding="utf-8"))
    for cell in nb.get("cells", []):
        cell["outputs"] = []
        cell["execution_count"] = None
    nb = _scrub_strings(nb)
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    notebooks = sorted(root.rglob("*.ipynb"))
    if not notebooks:
        print("No notebooks found under", root)
        return 1
    for p in notebooks:
        scrub_notebook(p)
        print("Scrubbed", p.relative_to(root))
    return 0


if __name__ == "__main__":
    sys.exit(main())
