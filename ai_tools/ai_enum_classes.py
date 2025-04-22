from enum import Enum 
class OpenAIModels(Enum):
    GPT_3_5_TURBO = 'gpt-3.5-turbo'
    GPT_4 = 'gpt-4'
    GPT_4_32K = 'gpt-4-32k'
    GPT_3_5_TURBO_16K = 'gpt-3.5-turbo-16k'
    GPT_4_8K = 'gpt-4-8k'
    GPT_Mini = 'gpt-4o-mini'
    
class AICryptoAnalystPrompts(Enum):
    # 1. ChatGPT
    SYSTEM_PROMPT = 'You are an expert crypto analyst.'
    USER_PROMPT = '''
    give me in json of 10 cryptos expected to rebound in next 24 hours 
    using the kraken naming standards and provide them in a python list without providing any other data or content or response. Provide also a weight
    for each coin, determining how much to invest in each coin. 
    The format should have:  {coin_symbol: 'value', coin_current_price: 'price_amount_USD', expected_gain_percentage: 'percent_float_value', weight: 'weight_float_value'}'''
    
    MESSAGES = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT} ]
    
    
    