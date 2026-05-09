# E-commerce analytics platform (Azure · Databricks)

End-to-end analytics lakehouse for **orders, shipments, and returns**: ingest raw operational feeds, refine them through a **Medallion (Bronze → Silver → Gold)** model, and expose **curated dimensions and facts** for reporting.

![Architecture](resources/project_architecture.svg)

## Objective

Deliver a repeatable pattern for **scalable retail analytics**: centralized governance with **Unity Catalog**, reliable incremental processing with **Delta Lake**, and clear separation between raw landing, validated conform layers, and business-ready star-schema style entities Power BI can consume.

## What this project demonstrates

- **Lakehouse design** — External landing on **ADLS Gen2**, managed catalog storage, Bronze / Silver / Gold schemas.
- **Dimensional modeling** — Conformed dimensions (e.g. date, customer, product paths via the dim notebooks) and **facts** for sales behavior.
- **Spark / PySpark engineering** — Transformations, incremental patterns, checkpoints, and structured pipelines suitable for production-style workloads.
- **Analytics handoff** — Gold-layer outputs aligned with **Power BI** reporting (`4_dashboarding/`).

## Tech stack

| Area | Technologies |
|------|----------------|
| Processing | PySpark, Delta Lake |
| Platform | Databricks, Unity Catalog |
| Storage | Azure Data Lake Storage Gen2 |
| Consumption | Power BI (`.pbix`) |

## Repository layout

| Path | Scope |
|------|--------|
| `1_setup/` | Catalog, schemas, raw landing volume |
| `2_medallion_processing_dim/` | Dimension pipelines — Bronze → Silver → Gold |
| `3_medallion_processing_fact/` | Fact pipelines — Bronze → Silver → Gold, daily summaries |
| `4_dashboarding/` | Power BI artifacts |
| `resources/` | Architecture diagrams |
| `samples/` | Small CSV examples illustrating source layout |

## Execution flow

1. **Setup** — Catalog and external volume for landing (`1_setup/`).
2. **Dimensions** — `1_dim_bronze` → `2_dim_silver` → `3_dim_gold`.
3. **Facts** — `1_fact_bronze` → `2_fact_silver` → `3_fact_gold`.
4. **Analytics** — `4_daily_summary.ipynb`, then dashboard layer.

Notebooks are authored for a **Databricks** workspace with **Unity Catalog** and appropriate **Azure storage** access. Cloud paths and widgets should be aligned with **your** environment before execution.

## Data

Source feeds follow an incremental layout (orders, shipments, returns). **Small illustrative files** are provided under `samples/` for schema reference. This repository is intended to showcase **pipeline design and implementation**, not to ship full production datasets.

---

*Synthetic / demo-style data; for portfolio and technical demonstration purposes.*
