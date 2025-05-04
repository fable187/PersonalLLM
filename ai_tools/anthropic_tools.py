import anthropic

import inspect
import json
from typing import get_type_hints

def generate_tool_json(func, description=None):
    """
    Generate Anthropic-compatible JSON schema from a Python function.

    Args:
        func (function): The Python function to introspect.
        description (str, optional): Optional description to override the function's docstring.

    Returns:
        dict: Tool definition JSON.
    """
    sig = inspect.signature(func)
    params = sig.parameters

    properties = {}
    required = []

    type_hints = get_type_hints(func)

    for param_name, param in params.items():
        param_info = {}

        # Determine type
        annotation = type_hints.get(param_name, str)
        type_str = 'string'  # default type

        if annotation == int:
            type_str = 'integer'
        elif annotation == float:
            type_str = 'number'
        elif annotation == bool:
            type_str = 'boolean'

        param_info['type'] = type_str
        param_info['description'] = f'The {param_name} parameter.'

        properties[param_name] = param_info

        # Check if parameter is required (no default provided)
        if param.default == inspect.Parameter.empty:
            required.append(param_name)

    tool_json = {
        "name": func.__name__,
        "description": description if description else inspect.getdoc(func) or "No description provided.",
        "input_schema": {
            "type": "object",
            "properties": properties,
            "required": required
        }
    }

    return tool_json

def call_anthropic():
    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=1000,
        temperature=1,
        system="You are a world-class poet. Respond only with short poems.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Why does chocolate taste good?"
                    }
                ]
            }
        ]
    )
    return message.content

def weather(location):
        """Get current weather information for a location."""
        weather_data = {
            "New York": {"temperature": 72, "condition": "Sunny"},
            "London": {"temperature": 62, "condition": "Cloudy"},
            "Tokyo": {"temperature": 80, "condition": "Partly cloudy"},
            "Paris": {"temperature": 65, "condition": "Rainy"},
            "Sydney": {"temperature": 85, "condition": "Clear"},
            "Berlin": {"temperature": 60, "condition": "Foggy"},
        }
        
        return weather_data.get(location, {"error": f"No weather data available for {location}"})

if __name__ == "__main__":
    print(call_anthropic())

