import hashlib
import hmac
import base64
import time
import urllib.parse
import requests
import krakenex

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
    



