from enum import Enum 

class AICryptoAnalystPrompts(Enum):
    # 1. ChatGPT
    SYSTEM_PROMPT = 'You are an expert crypto analyst.'
    USER_PROMPT = '''
    give me in json of 10 cryptos expected to rebound in next 24 hours 
    using the kraken naming standards and provide them in a python list without providing any other data or content or response. Provide also a weight
    for each coin, determining how much to invest in each coin. 
    The format should have:  {coin_symbol: 'value', coin_current_price: 'price_amount', expected_gain_percentage: 'percent_float_value', weight: 'weight_float_value'}'''
    
    
    
    
    