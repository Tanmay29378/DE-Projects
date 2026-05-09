# DE-Projects

Personal data-engineering portfolio: end-to-end pipelines, medallion-style lakehouse patterns, and supporting notebooks.

## Projects

| Project | Stack | Description |
|--------|--------|-------------|
| [`spark_project_ecommerce/spark_project_ecommerce`](spark_project_ecommerce/spark_project_ecommerce/) | Azure ADLS Gen2, Databricks, Unity Catalog, Delta Lake, PySpark | E-commerce orders, shipments, and returns — Bronze → Silver → Gold dimensions and facts |

Additional pipelines may be added alongside this folder over time.

## Clone

```bash
git clone git@github.com:Tanmay29378/DE-Projects.git
cd DE-Projects
```

## Note on data

Large raw / incremental CSV dumps are **not** committed. Each project README describes expected layouts and includes small **`samples/`** files for schema reference only.
