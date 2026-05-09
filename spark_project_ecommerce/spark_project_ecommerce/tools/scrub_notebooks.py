"""
Clear all notebook cell outputs (execution_count + outputs).

Optional: replace arbitrary strings before push — configured in a **local** JSON file
that is gitignored, so real Azure resource names never need to live in the repo.

Run from repo root:
  python spark_project_ecommerce/spark_project_ecommerce/tools/scrub_notebooks.py

Setup once (not committed):
  Copy scrub_replacements.example.json -> scrub_replacements.local.json
  Edit "from" / "to" pairs with strings you want stripped from notebooks (e.g. your
  real storage account name -> yourstorageacct).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

LOCAL_CONFIG = Path(__file__).resolve().parent / "scrub_replacements.local.json"
EXAMPLE_CONFIG = Path(__file__).resolve().parent / "scrub_replacements.example.json"


def _load_replacements() -> tuple[tuple[str, str], ...]:
    if not LOCAL_CONFIG.is_file():
        print(
            "Note: no scrub_replacements.local.json — only clearing outputs. "
            f"Copy {EXAMPLE_CONFIG.name} to scrub_replacements.local.json to add string replacements.",
            file=sys.stderr,
        )
        return ()
    data = json.loads(LOCAL_CONFIG.read_text(encoding="utf-8"))
    pairs = []
    for item in data.get("replacements", []):
        f, t = item.get("from"), item.get("to")
        if isinstance(f, str) and isinstance(t, str) and f:
            pairs.append((f, t))
    return tuple(pairs)


def _scrub_strings(obj, replacements: tuple[tuple[str, str], ...]):
    if not replacements:
        return obj
    if isinstance(obj, dict):
        return {k: _scrub_strings(v, replacements) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_scrub_strings(v, replacements) for v in obj]
    if isinstance(obj, str):
        s = obj
        for old, new in replacements:
            s = s.replace(old, new)
        return s
    return obj


def scrub_notebook(path: Path, replacements: tuple[tuple[str, str], ...]) -> None:
    nb = json.loads(path.read_text(encoding="utf-8"))
    for cell in nb.get("cells", []):
        cell["outputs"] = []
        cell["execution_count"] = None
    nb = _scrub_strings(nb, replacements)
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    notebooks = sorted(root.rglob("*.ipynb"))
    if not notebooks:
        print("No notebooks found under", root)
        return 1
    replacements = _load_replacements()
    if replacements:
        print(f"Applying {len(replacements)} replacement pair(s) from scrub_replacements.local.json")
    for p in notebooks:
        scrub_notebook(p, replacements)
        print("Scrubbed", p.relative_to(root))
    return 0


if __name__ == "__main__":
    sys.exit(main())
