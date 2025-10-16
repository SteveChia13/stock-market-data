# # 1️⃣ Add this at the very top
# import sys
# import os

# # Adjust paths to where your folders are inside the Docker container
# sys.path.append("/opt/airflow/scripts")
# sys.path.append("/opt/airflow/src")

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime
import subprocess

def fetch_and_load_data():
    import src.main as f
    f.main()

with DAG(
    "fetch_load_dbt_pipeline",
    start_date=datetime(2025, 10, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    fetch_and_load = PythonOperator(
        task_id="fetch_and_load_data",
        python_callable=fetch_and_load_data,
    )

    run_dbt = BashOperator(
        task_id="run_dbt",
        bash_command="cd /opt/airflow/dbt && dbt run --profiles-dir .",
    )

    fetch_and_load >> run_dbt
