import os
import re
import json
import sqlite3
from typing import Any, List, Tuple, Dict
from anthropic import Anthropic


class Tool:
    """
    Abstract base class for all tools.
    (No changes needed here)
    """
    name: str
    description: str
    input_schema: Dict[str, Any]

    def schema(self) -> Dict[str, Any]:
        """Return the tool definition schema for Anthropic."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
        }

    def execute(self, **kwargs) -> Any:
        """Execute the tool's action. Must be implemented by subclasses."""
        raise NotImplementedError("Tool execution not implemented.")


class ToolRegistry:
    """
    Registry for managing available tools.
    (No changes needed here)
    """
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """Register a tool instance with its name."""
        self._tools[tool.name] = tool

    def get_manifest(self) -> List[Dict[str, Any]]:
        """Generate the full tools manifest for Anthropic."""
        return [tool.schema() for tool in self._tools.values()]

    def execute(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a registered tool by name with provided arguments."""
        if name not in self._tools:
            raise ValueError(f"Tool '{name}' is not registered.")
        return self._tools[name].execute(**arguments)


class WeatherTool(Tool):
    """
    Tool for retrieving mock weather data.
    (No changes needed here)
    """
    name = "get_weather"
    description = "Get current weather information for a location."
    input_schema = {
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City name or address."}
        },
        "required": ["location"]
    }

    def execute(self, location: str) -> Dict[str, Any]:
        # In a real implementation, call an external API here
        # Using a slightly more robust mock data structure
        data = {
            "NY": {"temp": 75, "cond": "Sunny"},
            "London": {"temp": 62, "cond": "Cloudy"},
            "Tokyo": {"temp": 80, "cond": "Partly cloudy"},
        }
        return data.get(location, {"error": f"unknown location: {location}"})


class QueryDbTool(Tool):
    """
    Tool for executing SQL queries against a SQLite database.
    (No changes needed here)
    """
    name = "query_db"
    description = "Execute a SQL query against a sqlite database."
    input_schema = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "The SQL query to execute."},
            "db_path": {"type": "string", "description": "Path to the sqlite database file.", "default": "example.db"}
        },
        "required": ["query"]
    }

    def execute(self, query: str, db_path: str = "example.db") -> List[Tuple[Any, ...]]:
        # Basic check for database existence
        if not os.path.exists(db_path):
            # Create a dummy DB if it doesn't exist for testing
            print(f"Database '{db_path}' not found. Creating a dummy database.")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
            cursor.execute("INSERT INTO users (name) VALUES ('Alice'), ('Bob'), ('Charlie')")
            conn.commit()
            conn.close()

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            rows = [("Error executing query:", str(e))] # Return error as data
        finally:
            conn.close()
        return rows


class ChatBot:
    """
    Coordinates conversation with Anthropic Claude, simulating tool use via prompting.
    """
    TOOL_CALL_PREFIX = "TOOL_CALL:"

    def __init__(self, api_key: str, registry: ToolRegistry):
        self.client = Anthropic(api_key=api_key)
        self.registry = registry
        self.messages: List[Dict[str, Any]] = []
        self.model_name = "claude-3-5-sonnet-20240620" # Use the latest recommended model
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """Builds the system prompt including tool descriptions and instructions."""
        tool_descriptions = []
        for tool_schema in self.registry.get_manifest():
            # Simplified schema representation for the prompt
            tool_descriptions.append(
                f"- Tool Name: {tool_schema['name']}\n"
                f"  Description: {tool_schema['description']}\n"
                f"  Input Schema: {json.dumps(tool_schema['input_schema'])}"
            )
        tool_list_str = "\n".join(tool_descriptions)

        return (
            "You are a helpful assistant. You can use tools to answer questions.\n\n"
            "Available Tools:\n"
            f"{tool_list_str}\n\n"
            f"Instructions for Tool Use:\n"
            f"1. When you need to use a tool to answer a question or perform an action, "
            f"respond *only* with a single line starting with '{self.TOOL_CALL_PREFIX}' followed by a JSON object.\n"
            f"2. The JSON object must have two keys: 'tool_name' (string) and 'arguments' (object).\n"
            f"   Example: {self.TOOL_CALL_PREFIX} {{\"tool_name\": \"get_weather\", \"arguments\": {{\"location\": \"London\"}}}}\n"
            f"3. Do not add any other text, explanations, or formatting before or after the {self.TOOL_CALL_PREFIX} line.\n"
            f"4. After you make a tool call, I will provide the result in the next message starting with 'TOOL_RESULT:'.\n"
            f"5. Use the information from the 'TOOL_RESULT:' to formulate your final response to the user.\n"
            f"6. If you don't need a tool, just respond normally."
        )

    def ask(self, user_input: str) -> str:
        """
        Send a user prompt to Claude, handle simulated tool calls, and return the final response.
        """
        # Add the user's input to the message history
        self.messages.append({"role": "user", "content": user_input})

        while True:
            print(f"\n-> Sending to Claude (History Length: {len(self.messages)}): {self.messages[-1]}") # Debug print
            response = self.client.messages.create(
                model=self.model_name,
                messages=self.messages,
                system=self.system_prompt, # Pass system prompt here
                # NO 'tools' or 'tool_choice' parameters
                max_tokens=1000,
                temperature=0.1 # Lower temperature might help follow the strict format
            )
            print(f"<- Received from Claude: Stop Reason: {response.stop_reason}") # Debug print

            # Extract the primary text content from the response
            # Claude's response.content is a list, usually with one TextBlock
            assistant_response_text = ""
            if response.content and response.content[0].type == "text":
                assistant_response_text = response.content[0].text.strip()
                print(f"   Raw Assistant Text: '{assistant_response_text}'") # Debug print
            else:
                 print(f"   Assistant response content not text or empty: {response.content}")
                 # Decide how to handle this - maybe return an error or the raw content?
                 # For now, let's add the raw content as the message and try to proceed
                 self.messages.append({"role": "assistant", "content": response.content})
                 return f"Error: Unexpected response format from Claude: {response.content}"


            # Append the assistant's *raw* response message to history *before* checking for tool call
            # This ensures the LLM sees its own thought process if it emitted a tool call
            self.messages.append({"role": "assistant", "content": response.content})

            # Check if the response is a tool call based on our defined format
            if assistant_response_text.startswith(self.TOOL_CALL_PREFIX):
                tool_call_json_str = assistant_response_text[len(self.TOOL_CALL_PREFIX):].strip()
                print(f"   Detected TOOL_CALL. Parsing: '{tool_call_json_str}'") # Debug print
                try:
                    tool_call_data = json.loads(tool_call_json_str)
                    tool_name = tool_call_data.get("tool_name")
                    tool_input = tool_call_data.get("arguments", {})

                    if not tool_name or not isinstance(tool_input, dict):
                        raise ValueError("Invalid TOOL_CALL format in JSON.")

                    print(f"   Executing tool: {tool_name} with input: {tool_input}") # Debug print
                    try:
                        tool_result = self.registry.execute(tool_name, tool_input)
                        print(f"   Tool result: {tool_result}") # Debug print
                        result_content_str = json.dumps(tool_result)
                    except Exception as e:
                        print(f"   Error executing tool {tool_name}: {e}")
                        result_content_str = json.dumps({"error": f"Failed to execute tool {tool_name}: {str(e)}"})

                    # Feed tool result back into the conversation as a user message
                    tool_result_message = {
                        "role": "user",
                        "content": f"TOOL_RESULT: {result_content_str}" # Simple text feedback
                    }
                    self.messages.append(tool_result_message)
                    # Continue the loop to get Claude's response based on the tool result
                    continue

                except json.JSONDecodeError as e:
                    print(f"   Error parsing TOOL_CALL JSON: {e}")
                    # Add an error message back and let Claude try again or respond
                    error_feedback = {
                        "role": "user",
                        "content": f"TOOL_RESULT: {{\"error\": \"Invalid JSON format in TOOL_CALL: {e}\"}}"
                    }
                    self.messages.append(error_feedback)
                    continue # Let Claude respond to the error
                except ValueError as e:
                    print(f"   Error in TOOL_CALL data structure: {e}")
                    error_feedback = {
                        "role": "user",
                        "content": f"TOOL_RESULT: {{\"error\": \"Invalid data structure in TOOL_CALL: {e}\"}}"
                    }
                    self.messages.append(error_feedback)
                    continue # Let Claude respond to the error

            else:
                # Not a tool call, this is the final response for this turn
                print(f"   Final response: {assistant_response_text}") # Debug print
                return assistant_response_text

        # Should not be reached due to return/continue inside loop
        return "Error: Unexpected loop exit."


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        return

    registry = ToolRegistry()

    # Register all tools
    registry.register(WeatherTool())
    registry.register(QueryDbTool())

    bot = ChatBot(api_key, registry)

    # Example interactions
    print("\n--- Asking about weather ---")
    print(f"Bot response: {bot.ask('Whats the weather in NY?')}")

    print("\n--- Asking to query database ---")
    # Ensure the dummy DB exists or is created by the tool
    db_file = "example.db"
    if os.path.exists(db_file):
        print(f"Using existing database: {db_file}")
    else:
        print(f"Database {db_file} will be created by the tool.")

    print(f"Bot response: {bot.ask('SELECT name FROM users WHERE id = 2;')}") # More specific query

    print("\n--- Asking about unknown weather location ---")
    print(f"Bot response: {bot.ask('Whats the weather in Atlantis?')}")

    print("\n--- Asking with invalid SQL ---")
    print(f"Bot response: {bot.ask('SELECT non_existent_column FROM users;')}")

    print("\n--- Asking something that doesn't require a tool ---")
    print(f"Bot response: {bot.ask('Explain the concept of a language model.')}")


if __name__ == "__main__":
    main()
