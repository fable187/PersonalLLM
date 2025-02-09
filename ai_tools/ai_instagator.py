import os
import requests
import json
from openai import OpenAI
import pandas as pd
from ai_tools.ai_enum_classes import AICryptoAnalystPrompts, OpenAIModels
from exchange_tools.exchange_tool import KrakenAPIClient, AssetPair, TradeExecutor
from exchange_tools.kraken_tools import get_kraken_api, get_trading_pair_symbol


class AIInstagator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.investment_budget = 100
        
        
    def prompt_ai(self, messages, model):
        ai_response = self.openai.chat.completions.create(
            model=model,
            messages=messages,
            stream=False,
            response_format={"type": "json_object"}
        )
        return json.loads(ai_response.to_json())
    
    
    def convert_response_to_dataframe(self, ai_response):
        json_string = ai_response['choices'][0]['message']['content']
        json_obj = json.loads(json_string)
        return pd.json_normalize(json_obj['cryptos'])
    
    
    
    def buy_crypto(self, crypto_symbol, weight, trade_executor:TradeExecutor):
        # Placeholder for buying crypto
        dollar_amount = self.investment_budget * weight
        trade_executor.execute_trade(crypto_symbol, weight)
    
    def buy_list_cryptos(self, crypto_list):
        for crypto in crypto_list:
            self.buy_crypto(crypto['coin_symbol'], crypto['weight'])
            

        
            


    
    
    
    
    
    