
from polygon import RESTClient

def fetch_polygon_data(polygon_api_key: str, ticker: str, date: str):
    # Fetch data from Polygon
    client = RESTClient(polygon_api_key)

    aggs = client.get_aggs(ticker, 1, "day", date, date)

    # Convert Agg objects to dictionaries
    records = [agg.__dict__ for agg in aggs]

    # Convert Agg objects to dict and add date field
    records = []
    for agg in aggs:
        record = agg.__dict__.copy()
        record["date"] = date  # Add a date field for partitioning
        records.append(record)

    return records   

    