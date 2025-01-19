import hashlib
import hmac
import base64
import time
import urllib.parse
import requests


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
    full_url = 'https://api.kraken.com' + url_path
    headers = {
        'API-Key': api_key, 'API-Sign': get_kraken_signature(url_path, data, api_secret)}
    # send request
    response = requests.post(full_url, headers=headers, data=data)
    return response




