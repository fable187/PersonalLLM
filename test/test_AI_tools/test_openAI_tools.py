import os
import unittest
import json
from openai import OpenAI
import pandas as pd
from ai_tools.ai_enum_classes import AICryptoAnalystPrompts
from ai_tools.ai_instagator import AIInstagator

class test_AIInstagator(unittest.TestCase):
    
    def setUp(self):
        self.messages = [
        {"role": "system", "content": AICryptoAnalystPrompts.SYSTEM_PROMPT.value},
        {"role": "user", "content": AICryptoAnalystPrompts.USER_PROMPT.value}
      ]
        self.model = 'gpt-4o-mini'
    
    def test_get_openai_key(self):
        '''test if OpenAI key is set''' 
        api_key = os.getenv("OPENAI_API_KEY")
        assert api_key
        
        
    def test_get_anthropic_key(self):
        '''test if Anthropic key is set''' 
        api_key = os.getenv("ANTHROPIC_API_KEY")
        assert api_key
        
    def test_get_google_key(self):
        '''test if Google key is set''' 
        api_key = os.getenv("GOOGLE_API_KEY")
        assert api_key
        
    def test_create_open_ai_instance(self):
        '''test if OpenAI instance is created''' 
        
        openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
                            
        assert openai
        
    def test_prompt_ai(self):
        '''test if AI can be prompted''' 
        
        ai_instagator = AIInstagator(api_key=os.getenv('OPENAI_API_KEY'))
        ai_response = ai_instagator.prompt_ai(messages=self.messages, model=self.model)
        assert ai_response
        
    def test_ai_response_has_correct_keys(self):
        '''test if AI response has correct keys''' 
        
        ai_instagator = AIInstagator(api_key=os.getenv('OPENAI_API_KEY'))
        ai_response = ai_instagator.prompt_ai(messages=self.messages, model=self.model)
        json_string = ai_response['choices'][0]['message']['content']
        json_obj = json.loads(json_string)
        print(json_obj.keys())
        assert 'cryptos' in json_obj.keys()
        
    def test_convert_response_to_dataframe(self):
        '''test if AI json response can be converted to dataframe''' 
        
        ai_instagator = AIInstagator(api_key=os.getenv('OPENAI_API_KEY'))
        ai_response = ai_instagator.prompt_ai(messages=self.messages, model=self.model)
        ai_response_df = ai_instagator.convert_response_to_dataframe(ai_response)
        assert ['coin_symbol', 'coin_current_price', 'expected_gain_percentage'] == list(ai_response_df.columns)
        
 