import config
import json
from polygon import RESTClient
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

client = RESTClient(config.POLYGON_API_KEY)
TICKER = "AAPL"
DATE = "2025-10-02"

# -----------------------------
# 1. Fetch data from Polygon
# -----------------------------
aggs = client.get_aggs(TICKER, 1, "day", DATE, DATE)

# Convert Agg objects to dictionaries
agg_dicts = [agg.__dict__ for agg in aggs]

# Convert Agg objects to dict and add date field
agg_dicts = []
for agg in aggs:
    record = agg.__dict__.copy()
    record["date"] = DATE  # Add a date field for partitioning
    agg_dicts.append(record)

# -----------------------------
# 2. BigQuery Sandbox setup
# -----------------------------
PROJECT_ID = "gcp-prod-data"
DATASET_ID = "stock_market_ticker_raw"
TABLE_ID = f"{TICKER.lower()}_raw"

client_bq = bigquery.Client(project=PROJECT_ID)

# -----------------------------
# 3. Ensure dataset exists
# -----------------------------
dataset_ref = client_bq.dataset(DATASET_ID)
try:
    client_bq.get_dataset(dataset_ref)
    print(f"Dataset '{DATASET_ID}' exists.")
except NotFound:
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "US"
    client_bq.create_dataset(dataset)
    print(f"✅ Created dataset '{DATASET_ID}'.")

# -----------------------------
# 4. Prepare table reference
# -----------------------------
table_ref = dataset_ref.table(TABLE_ID)

# -----------------------------
# 5. Configure partitioned table
# -----------------------------
# Try to create table if not exists with partitioning
try:
    client_bq.get_table(table_ref)
    print(f"Table '{TABLE_ID}' exists.")
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

    # Load JSON schema to create table with correct schema
    client_bq.load_table_from_json(agg_dicts, table_ref, job_config=job_config).result()

    print(f"✅ Created partitioned table '{TABLE_ID}'.")

# -----------------------------
# 6. Load JSON data into BigQuery
# -----------------------------
job_config = bigquery.LoadJobConfig(
    autodetect=True,
    write_disposition="WRITE_APPEND",
    schema_update_options=[bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION]
)

load_job = client_bq.load_table_from_json(agg_dicts, table_ref, job_config=job_config)
load_job.result()  # Wait for job to complete

print(f"✅ Uploaded {len(agg_dicts)} rows to {DATASET_ID}.{TABLE_ID}")