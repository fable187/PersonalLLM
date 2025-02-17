import os
from google.cloud import secretmanager
from gcp_tools.project_enums import KrakenReadOnlySecret
import json

def get_secret():
    client = secretmanager.SecretManagerServiceClient()
    name = KrakenReadOnlySecret.KEY_LOCATION
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("UTF-8") # payload is the entire JSON string

    secrets = json.loads(payload)

    api_key = secrets["kraken_api_key"]
    api_secret = secrets["kraken_api_secret"]

    print(f"API Key: {api_key}") # Handle these securely!
    print(f"API Secret: {api_secret}") # Handle these securely!
    return api_key, api_secret

