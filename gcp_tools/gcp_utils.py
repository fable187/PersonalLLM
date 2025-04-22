import os
from google.cloud import secretmanager
from gcp_tools.project_enums import GCPSecret
from google.auth import default
from google.auth.transport.requests import AuthorizedSession
import json

def get_secret( gcp_secret: GCPSecret):
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(request={"name": gcp_secret.NAME})
    payload = response.payload.data.decode("UTF-8") # payload is the entire JSON string

    secrets = json.loads(payload)

    api_key = secrets[secrets_key]
    api_secret = secrets[secrets_value]

    print(f"API Key retrieved") # Handle these securely!
    print(f"API Secret retrieved") # Handle these securely!
    return api_key, api_secret




def get_identity_token(cloud_run_service_url):
    """
    Retrieves an identity token for a given target audience.

    Args:
        cloud_run_service_url (str): Your Cloud Run service URL.

    Returns:
        str: The identity token, or None if an error occurs.
    """
    try:
        credentials, project_id = default()  # Get default credentials
        auth_req = AuthorizedSession(credentials)
        id_token = auth_req.credentials.create_id_token(cloud_run_service_url)
        return id_token
    except Exception as e:
        print(f"Error getting identity token: {e}")
        return None

