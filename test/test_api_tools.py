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

   
    def test_ASSET_INFO(self):
        response = kraken_request(KrakenAPIUrls.ASSET_INFO.value, self.data, self.api_key, self.api_secret)
        self.assertEqual(response.status_code, 200)
        assert response.json()['error'] == []
        
    def test_BALANCE_INFO(self):
        api = krakenex.API(key=self.api_key, secret=self.api_secret)
        response = api.query_private('Balance')
        self.assertEqual(response.status_code, 200)
        assert response.json()['error'] == []
        
    def test_api_key_works(self):
        assert verify_kraken_api(self.api_key, self.api_secret) == True
        
    def test_get_kraken_api(self):
        api = get_kraken_api()
        assert api != None
        assert api.key == self.api_key
        assert api.secret == self.api_secret
        
    def test_trade_crypto(self):
        api = get_kraken_api()
        order_status = trade_crypto(api, 'XBT', 'XRP', 10)
        print('hold')
       
