# E-commerce analytics — Medallion lakehouse (Azure + Databricks)

PySpark / Delta pipelines on **Databricks** with **Unity Catalog**, **external volumes** on **ADLS Gen2**, and a **Bronze → Silver → Gold** layout for dimensions and facts (orders / shipments / returns).

![Architecture](resources/project_architecture.svg)

## What’s in this repo

| Path | Purpose |
|------|---------|
| `1_setup/` | Catalog, schemas, external volume for raw landing |
| `2_medallion_processing_dim/` | Dimension Bronze → Silver → Gold notebooks |
| `3_medallion_processing_fact/` | Fact Bronze → Silver → Gold + daily summary |
| `4_dashboarding/` | Power BI report (`.pbix`) and related assets |
| `resources/` | Architecture diagram (SVG/PNG) and preview image |
| `samples/` | Tiny CSV examples — **schema only**, not production data |

The **`0_data/`** folder (full incremental CSVs) is **gitignored**. Keep it on your machine or object storage; do not commit bulk raw files.

## Prerequisites

- Databricks workspace with Unity Catalog enabled
- Azure Data Lake Storage Gen2 account and containers for:
  - Catalog managed storage (Unity Catalog)
  - Raw landing (`CREATE EXTERNAL VOLUME` pattern)
- Appropriate IAM: storage credentials / UC external locations per your org’s pattern

## Run order

1. `1_setup/setup_catalog.ipynb` — catalog `ecommerce`, schemas `bronze`, `silver`, `gold`
2. `1_setup/setup_raw_external_volume.ipynb` — `raw` schema + external volume for landing
3. Dimensions: `2_medallion_processing_dim/1_dim_bronze.ipynb` → `2_dim_silver.ipynb` → `3_dim_gold.ipynb`
4. Facts: `3_medallion_processing_fact/1_fact_bronze.ipynb` → `2_fact_silver.ipynb` → `3_fact_gold.ipynb`
5. `3_medallion_processing_fact/4_daily_summary.ipynb`

Adjust paths, widgets, and container names to match **your** ADLS layout before running.

## Configuration placeholder

Notebooks use the Azure storage account placeholder **`yourstorageacct`** in:

- Unity Catalog `MANAGED LOCATION` and external volume `LOCATION` URLs
- `dbutils.widgets` defaults and saved widget metadata

Replace **`yourstorageacct`** with your real ADLS Gen2 storage account name (3–24 lowercase letters and digits only) before running. Adjust container names (`uc-data`, `ecomm-raw-data`) if your naming differs.

To re-sanitize notebooks after local runs (clears outputs + restores placeholders), run:

```bash
python spark_project_ecommerce/spark_project_ecommerce/tools/scrub_notebooks.py
```

## Git history

If this repo was ever pushed with real storage account names, those names may still exist in **older commits**. For a public repo, consider [removing sensitive data from Git history](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) or rotating credentials / reviewing Azure storage network rules.

This repo’s `.gitignore` excludes `0_data/` so bulk raw files are not uploaded.

## Sample file layout (landing)

Incremental CSVs are expected under paths consistent with your volume layout, for example:

- `order_items/landing/` — order line items
- `order_shipments/incoming/` — shipments by period
- `order_returns/incoming/` — returns by period

See `samples/` for minimal examples of column shapes.

## Disclaimer

Dataset is **synthetic / demo-style** and used for pipeline and modeling practice only.
