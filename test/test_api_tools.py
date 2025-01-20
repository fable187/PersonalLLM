import unittest
import requests
from api_tools.url_enums import KrakenAPIUrls
import time
from api_tools.kraken_tools import *
import pandas as pd
import os
class TestApiTools(unittest.TestCase):

    def setUp(self):
        self.api_key = os.environ.get('KRAKEN_PUB')
        self.api_secret = os.environ.get('KRAKEN_SEC')
        self.data = {'nonce': str(int(time.time() * 1000))}
        self.test_endpoint = "/0/private/TradesHistory"

    def test_kraken_request(self):
        
        response = kraken_request(KrakenAPIUrls.TRADE_HISTORY.value, self.data, self.api_key, self.api_secret)
        self.assertEqual(response.status_code, 200)
        assert response.json()['error'] == []
        df = pd.json_normalize(response.json(), max_level=1)
        self.assertEqual(df.empty, False)
        
    def test_ASSET_INFO(self):
        response = kraken_request(KrakenAPIUrls.ASSET_INFO.value, self.data, self.api_key, self.api_secret)
        self.assertEqual(response.status_code, 200)
        assert response.json()['error'] == []
        
    def test_BALANCE_INFO(self):
        response = kraken_request(KrakenAPIUrls.ACCOUNT_BALANCE.value, self.data, self.api_key, self.api_secret)
        df = pd.json_normalize(response.json(), max_level=1)
        assert response.json()['error'] == []
        self.assertEqual(df.empty, False)
        
    def test_api_key_works(self):
        assert verify_kraken_api(self.api_key, self.api_secret) == True
