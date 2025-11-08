# Project README — corrected

Short description
This repository implements a small ETL that fetches daily aggregate stock data for a single ticker (currently AAPL) using the Polygon REST API, uploads raw JSON rows to Google BigQuery (partitioned by date), and runs dbt transformations.

Process:
- Extraction: fetches daily aggregates for a single hard-coded ticker via src/fetch_data.py.
- Loading: writes raw JSON rows into partitioned BigQuery tables via src/bigquery_loader.py.
- Orchestration: an Airflow DAG (dags/fetch_and_load_data_dag.py) invokes the ETL and then runs dbt.
- Transformation: dbt project lives in dbt_core/.

Important files
- src/main.py — main ETL entrypoint (calls fetch/load for a single ticker/date).
- src/fetch_data.py — Polygon REST wrapper (daily aggregates).
- src/bigquery_loader.py — BigQuery upload and dataset/table helpers.
- dags/fetch_and_load_data_dag.py — Airflow DAG that triggers the ETL and dbt.
- dbt_core/ — dbt project (models, macros, profiles).
- secrets/ — local credential examples (do not commit secrets to public repos).
- Dockerfile / docker-compose — containerized Airflow + dbt setup.
- Makefile — developer convenience commands.

Configuration / credentials
- POLYGON_API_KEY: set in environment or config (see src/config.py).
- Google credentials: set GOOGLE_APPLICATION_CREDENTIALS to a service account JSON if using BigQuery locally (secrets/gcp-prod-data-service-account-key.json is present locally but should not be committed publicly).
- Check src/config.py for any hard-coded constants used by the ETL (ticker/date).

Quick start — run locally
1. Create venv and install deps:
   make dev
2. Set credentials:
   export POLYGON_API_KEY="your_polygon_key"
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
3. Run a single ETL execution:
   python -m src.main

Quick start — Airflow + dbt (containerized)
1. Build and start containers:
   docker-compose up --build
2. The Airflow DAG file is at dags/fetch_and_load_data_dag.py — it calls the ETL and then runs dbt. Check the DAG id in that file to trigger/schedule via the Airflow UI.

Notes & next steps
- Current implementation processes one hard-coded ticker and a specific date.
- The fetch function returns daily aggregates; there is no minute-level scraping implemented.
- Keep secrets out of source control.

