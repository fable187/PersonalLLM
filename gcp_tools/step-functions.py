import functions_framework
import requests
from google.cloud import bigquery
from google.cloud import secretmanager
import os
import json
from datetime import datetime

def access_secret_version(project_id, secret_id, version_id="latest"):
    """Access the payload for the given secret version if one exists."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

def get_kraken_data(pair, interval, project_id):
    """Retrieves OHLC data from the Kraken API."""
    secret_id = "KRAKEN_PUB_KEY_READONLY" #replace with your secret name.
    api_key = access_secret_version(project_id, secret_id)
    url = f"https://api.kraken.com/0/public/OHLC?pair={pair}&interval={interval}"
    headers = {"API-Key": api_key}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
    data = response.json()
    return data["result"][pair]

def insert_bigquery(rows, project_id):
    """Inserts data into the BigQuery table."""
    client = bigquery.Client(project=project_id)
    table_id = f"{project_id}.kraken_data.ohlc_data"
    table = client.get_table(table_id)
    errors = client.insert_rows(table, rows)
    if errors:
        print(f"Encountered errors while inserting rows: {errors}")
    else:
        print("Data successfully inserted into BigQuery.")

# @functions_framework.http
# def kraken_to_bigquery(request):
def kraken_to_bigquery():
    """HTTP Cloud Function to ingest Kraken data into BigQuery."""
    # project_id = os.environ.get("GCP_PROJECT")
    project_id = 'trading-app-project-450322'
    print(f"Found project id: {project_id}")
    pair = "XBTUSD"  # Example pair
    interval = 60  # Example interval (minutes)
    try:
        kraken_data = get_kraken_data(pair, interval, project_id)
        rows = []
        for item in kraken_data:
            timestamp = datetime.fromtimestamp(item[0])
            row = {
                "timestamp": timestamp,
                "pair": pair,
                "open": item[1],
                "high": item[2],
                "low": item[3],
                "close": item[4],
                "volume": item[5],
            }
            rows.append(row)
        insert_bigquery(rows, project_id)
        return "Data ingestion successful", 200
    except Exception as e:
        return f"Error: {e}", 500