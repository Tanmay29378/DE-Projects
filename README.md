# Data engineering portfolio

Portfolio of **end-to-end data pipelines**: Azure lakehouse (Medallion / Databricks) and **AWS** ingestion → S3 → transformation → Redshift / Athena.

## Projects

| Project | Stack | Summary |
|---------|--------|---------|
| [E-commerce analytics platform](spark_project_ecommerce/spark_project_ecommerce/) | Azure ADLS Gen2, Databricks, Unity Catalog, Delta Lake, PySpark, Power BI | Retail analytics — Bronze → Silver → Gold dimensions and facts with reporting layer |
| [Healthcare support analytics — Care Plus](project_care_plus/project_care_plus/) | AWS S3, Lambda-style ETL, Glue patterns, Redshift, Athena, Python | Support tickets & logs: ingest, Parquet processing, warehouse load, analytics SQL |

## Clone

```bash
git clone git@github.com:Tanmay29378/DE-Projects.git
cd DE-Projects
```

Each project README describes layout and scope. Large raw datasets are kept local; sample schemas and env templates are included where relevant.
