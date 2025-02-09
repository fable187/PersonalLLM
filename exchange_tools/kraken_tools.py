import hashlib
import hmac
import base64
import time
import urllib.parse
import requests
import krakenex
import os
from common.exceptions import *

def get_kraken_api():
    api_key = os.environ.get('KRAKEN_PUB')
    api_secret = os.environ.get('KRAKEN_SEC')
    api = krakenex.API(key=api_key, secret=api_secret)
    return api


def get_kraken_signature(url_path, data, secret):
    
    # encode API data
    postdata = urllib.parse.urlencode(data)
    # hash it
    encoded = (str(data['nonce']) + postdata).encode()
    message = url_path.encode() + hashlib.sha256(encoded).digest()
    # sign it
    mac = hmac.new(base64.b64decode(secret),
                   message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()

def kraken_request(url_path, data, api_key, api_secret):
    # headers
    sign = get_kraken_signature(url_path, data, api_secret)
    headers = {
        
        'API-Key': api_key, 
        'API-Sign': sign}
    # send request
    response = requests.post(url_path, headers=headers, data=data)
    return response

def verify_kraken_api(api_key, api_secret):
    # Initialize the Kraken API client
    api = krakenex.API(key=api_key, secret=api_secret)
    
    try:
        # Attempt to retrieve your account balance
        response = api.query_private('Balance')
        
        if response.get('error'):
            print(f"Error: {response['error']}")
            return False
        else:
            print("API key and secret are working correctly.")
            return True
    except Exception as e:
        print(f"An exception occurred: {e}")
        return False
    

    
def get_trading_pair_symbol(crypto_a: str, crypto_b: str) -> str:
    """
    Retrieve the Kraken trading pair symbol for two given cryptocurrencies.

    Args:
        crypto_a (str): The base cryptocurrency symbol (e.g., 'BTC').
        crypto_b (str): The quote cryptocurrency symbol (e.g., 'USD').

    Returns:
        str: The Kraken trading pair symbol (e.g., 'XXBTZUSD').

    Raises:
        ValueError: If the trading pair is not found.
    """
    # Kraken API endpoint for tradable asset pairs
    url = 'https://api.kraken.com/0/public/AssetPairs'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get('error'):
            raise Exception(f"API Error: {data['error']}")

        asset_pairs = data.get('result', {})

        # Normalize input symbols to uppercase
        crypto_a = crypto_a.upper()
        crypto_b = crypto_b.upper()

        # Search for the matching asset pair
        for pair, details in asset_pairs.items():
            altname = details.get('altname', '')
            if altname == f"{crypto_a}{crypto_b}" or altname == f"{crypto_b}{crypto_a}":
                return pair

        raise ValueError(f"Trading pair for {crypto_a}/{crypto_b} not found.")

    except requests.RequestException as e:
        raise Exception(f"HTTP Request failed: {e}")
    
    
    
    


