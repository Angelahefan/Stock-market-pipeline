# Stock Market Data Pipeline

End-to-end data engineering project.

## Architecture

Sources
- Yahoo Finance API

↓

Ingestion
- Python
- Provider pattern
- Retry
- Fallback

↓

Storage
- DuckDB

↓

Transformation
- dbt

↓

Warehouse
- Snowflake

↓

Orchestration
- Airflow

↓

AI Layer
- LLM Tool Calling
