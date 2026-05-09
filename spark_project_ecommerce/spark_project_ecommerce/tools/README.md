# Maintainer utilities

## Notebook scrub (`scrub_notebooks.py`)

Clears committed notebook outputs and optionally applies string replacements before pushing to a public remote.

1. Copy `scrub_replacements.example.json` to **`scrub_replacements.local.json`** (gitignored).
2. Add `"from"` / `"to"` pairs as needed.
3. From the repo root:

```bash
python spark_project_ecommerce/spark_project_ecommerce/tools/scrub_notebooks.py
```

If `scrub_replacements.local.json` is missing, only outputs are cleared.
