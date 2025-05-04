import os
import unittest
import json
from openai import OpenAI
import pandas as pd
from ai_tools.ai_enum_classes import AICryptoAnalystPrompts, OpenAIModels
from ai_tools.ai_instagator import AIInstagator
from ai_tools.anthropic_tools import *


class test_AnthropicToolkit(unittest.TestCase):
    
    def setUp(self):
        self.messages = AICryptoAnalystPrompts.MESSAGES.value
        self.model = OpenAIModels.GPT_Mini.value


    def test_call_anthropic(self):
        from anthropic.types.text_block import TextBlock
        content:list = call_anthropic()
        content_text:TextBlock = content[0]
        print(content_text.text)
       
    def test_generate_tool_json(self):
        from ai_tools.anthropic_tools import weather, generate_tool_json
        expected_schema = {
            "name": "weather",
            "description": "Get current weather information for a location.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The location parameter."
                    }
                },
                "required": ["location"]
            }
        }

        result = generate_tool_json(weather)

        assert result == expected_schema, f"Test failed! Expected: {expected_schema}, got: {result}"
    
    def test_chattool(self):
        from ai_tools.anthropic_chat_tool import main
        main()

    def test_chattool_mytool(self):
        from ai_tools.anthropic_chat_mytools import main
        main()