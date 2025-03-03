import unittest
from exchange_tools.exchange_tool import KrakenAPIClient, AssetPair, TradeExecutor
import pandas as pd
from exchange_tools.kraken_tools import get_kraken_api, get_trading_pair_symbol
class TestExchangeTools(unittest.TestCase):
    
    def setUp(self):
        self.kraken_api = KrakenAPIClient(get_kraken_api())
    
    def test_get_kraken_api(self):
        
        self.assertIsInstance(self.kraken_api, KrakenAPIClient)
    
    def test_fetch_assets(self):
        assets = self.kraken_api.fetch_assets()
        print(assets)
        self.assertIsInstance(assets, dict)
        
    def test_fetch_asset_history(self):
        assets = self.kraken_api.fetch_assets()
        asset_pair = AssetPair('XBT', 'USD', assets)
        pair_symbol = asset_pair.get_pair_symbol()
        asset_history = self.kraken_api.fetch_asset_history(pair_symbol, 1690000000, 1690000000)
        print(asset_history)
        assert 'XXBTZUSD' in asset_history
    
    def test_fetch_ticker(self):
        assets = self.kraken_api.fetch_assets()
        asset_pair = AssetPair('XBT', 'USD', assets)
        pair_symbol = asset_pair.get_pair_symbol()
        ticker = self.kraken_api.fetch_ticker(pair_symbol)
        ticket_df = pd.json_normalize(ticker)
        print(ticket_df)
        self.assertIn('a', ticker)
        
    def test_get_trading_pair_symbol(self):
        assets = self.kraken_api.fetch_assets()
        asset_pair = get_trading_pair_symbol('XBT', 'XRP')
        print(asset_pair)
        self.assertIsInstance(asset_pair, str)
    
    @unittest.skip("Skipping test_place_order for now")
    def test_place_order(self):
        
        asset_pair = get_trading_pair_symbol('XBT', 'XRP')
        order_result = self.kraken_api.place_order(asset_pair, 'buy', 10)
        print(order_result)
        self.assertIn('txid', order_result)
        
    def test_get_balance(self):
        balance = self.kraken_api.get_balance()
        print(balance)
        self.assertIn('XXBT', balance)

    def test_get_ohlc(self):
        assets = self.kraken_api.fetch_assets()
        asset_pair = AssetPair('XBT', 'USD', assets)
        pair_symbol = asset_pair.get_pair_symbol()
        ticker = self.kraken_api.get_ohlc(pair_symbol)
        ticket_df = pd.json_normalize(ticker)
        print(ticket_df)
        self.assertIn('a', ticker)
    