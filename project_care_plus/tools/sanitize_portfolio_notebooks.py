"""Clear outputs and remove secrets / tutorial attribution from Care Plus portfolio notebooks."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "project_care_plus"

DB_BLOCK_OLD = """# ---------- CONFIG ----------
db_config = {
    "host": "localhost",
    "port": "3306",
    "user": "root",  # change
    "password": "root", # change
    "database": "careplus_support_db"
}

S3_BUCKET = "careplus-data-store" 
S3_PREFIX = "support-tickets/raw/"  
DATE_TRACKER_FILE = "date_tracker.txt"

import os

AWS_CONFIG = {"""

DB_BLOCK_NEW = """# ---------- CONFIG ----------
db_config = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": os.getenv("MYSQL_PORT", "3306"),
    "user": os.getenv("MYSQL_USER", ""),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DATABASE", "careplus_support_db"),
}

S3_BUCKET = os.getenv("S3_BUCKET", "your-s3-bucket")
S3_PREFIX = "support-tickets/raw/"  
DATE_TRACKER_FILE = "date_tracker.txt"

AWS_CONFIG = {"""

REPLACEMENTS: tuple[tuple[str, str], ...] = (
    (
        "### Codebasics Data Engineering Tutorial: Data Ingestion for Logs",
        "### Support logs — incremental upload to S3",
    ),
    (
        'S3_BUCKET = "careplus-data-store" # this should match the exact bucket name you have setup in AWS S2',
        'S3_BUCKET = os.getenv("S3_BUCKET", "your-s3-bucket")  # configure in .env',
    ),
    ("bucket_name = 'careplus-data'", 'bucket_name = os.getenv("S3_BUCKET", "your-s3-bucket")'),
    ("import psycopg2\n\n# Redshift", "import os\nimport psycopg2\n\n# Redshift"),
)

_REDSHIFT_PW = re.compile(r"REDSHIFT_PASSWORD = '[^']*'(?:\s*#.*)?")


def _join_source(cell: dict) -> str:
    src = cell.get("source")
    if isinstance(src, list):
        return "".join(src)
    return src or ""


def _set_source(cell: dict, text: str) -> None:
    if not text:
        cell["source"] = []
        return
    lines = text.split("\n")
    parts: list[str] = []
    for i, ln in enumerate(lines):
        if i < len(lines) - 1:
            parts.append(ln + "\n")
        elif ln:
            parts.append(ln)
    cell["source"] = parts


def scrub_notebook(path: Path) -> None:
    nb = json.loads(path.read_text(encoding="utf-8"))
    for cell in nb.get("cells", []):
        cell["outputs"] = []
        cell["execution_count"] = None
        text = _join_source(cell)
        if not text:
            continue
        if DB_BLOCK_OLD in text:
            text = text.replace(DB_BLOCK_OLD, DB_BLOCK_NEW)
        for old, new in REPLACEMENTS:
            text = text.replace(old, new)
        text = _REDSHIFT_PW.sub('REDSHIFT_PASSWORD = os.getenv("REDSHIFT_PASSWORD", "")', text)
        _set_source(cell, text)
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    if not ROOT.is_dir():
        print("Missing:", ROOT)
        return 1
    for path in sorted(ROOT.rglob("*.ipynb")):
        scrub_notebook(path)
        print("Sanitized", path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
