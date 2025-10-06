
import json
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

def bq_dataset_check(client: bigquery.Client, dataset_id: str):
    # Ensure dataset exists
    dataset_ref = client.dataset(dataset_id)
    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset '{dataset_id}' exists.")
    except NotFound:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"
        client.create_dataset(dataset)
        print(f"✅ Created dataset '{dataset_id}'.")
    
    return dataset_ref


def load_data_to_bq(client: bigquery.Client, dataset_ref, dataset_id: str, table_id: str, data: list):
    # table reference check
    table_ref = dataset_ref.table(table_id)

    # Try to create table if not exists with partitioning
    try:
        client.get_table(table_ref)
        print(f"Table '{table_id}' exists.")

        job_config = bigquery.LoadJobConfig(
            autodetect=True,
            write_disposition="WRITE_APPEND",
            schema_update_options=[bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION]
        )

    except NotFound:
        job_config = bigquery.LoadJobConfig(
            autodetect=True,
            write_disposition="WRITE_APPEND",
            schema_update_options=[bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION],
            time_partitioning=bigquery.TimePartitioning(
                type_=bigquery.TimePartitioningType.DAY,
                field="date",  # Partition by date field
            )
        )
        print(f"✅ Created partitioned table '{table_id}'.")

    # Load JSON data into BigQuery
    load_job = client.load_table_from_json(data, table_ref, job_config=job_config)
    load_job.result()  # Wait for job to complete

    print(f"✅ Uploaded {len(data)} rows to {dataset_id}.{table_id}")