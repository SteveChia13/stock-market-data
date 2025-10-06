import config
from google.cloud import bigquery
from bigquery_loader import bq_dataset_check, load_data_to_bq
from fetch_data import fetch_polygon_data

TICKER = "AAPL"
DATE = "2025-10-01"

PROJECT_ID = "gcp-prod-data"
DATASET_ID = "stock_market_ticker_raw"
TABLE_ID = f"{TICKER.lower()}_raw"


def main():
    print("ETL process starting...")

    # Fetch data via Polygon API
    records = fetch_polygon_data(config.POLYGON_API_KEY, TICKER, DATE)

    # Initialize Bigquery Client
    client_bq = bigquery.Client(project=PROJECT_ID)

    # Check and load data into Bigquery
    dataset_ref = bq_dataset_check(client_bq, DATASET_ID)
    load_data_to_bq(client_bq, dataset_ref, DATASET_ID, TABLE_ID, records)

    print("🎉 ETL complete!")

if __name__ == "__main__":
    main()