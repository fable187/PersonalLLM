import os
import json
import sqlite3
from typing import Any, List, Tuple, Dict
from anthropic import Anthropic


class Tool:
    """
    Abstract base class for all tools.
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
    Coordinates conversation with Anthropic Claude including tool invocations.
    """
    def __init__(self, api_key: str, registry: ToolRegistry):
        self.client = Anthropic(api_key=api_key)
        self.registry = registry
        # Initialize messages with a system prompt
        self.system_prompt = "You are a helpful assistant with tool access."
        self.messages: List[Dict[str, Any]] = []
        self.model_name = "claude-3-5-sonnet-20240620" # Use the latest recommended model

    def ask(self, user_input: str) -> str:
        """
        Send a user prompt to Claude, handle any tool invocations, and return the final response.
        """
        # Add the user's input to the message history
        self.messages.append({"role": "user", "content": user_input})

        while True:
            print(f"\n-> Sending to Claude: {self.messages[-1]}") # Debug print
            response = self.client.messages.create(
                model=self.model_name,
                messages=self.messages,
                system=self.system_prompt, # Pass system prompt here
                tools=self.registry.get_manifest(),
                tool_choice={"type": "auto"}, # Correct format for tool_choice
                max_tokens=1000
            )
            print(f"<- Received from Claude: Stop Reason: {response.stop_reason}") # Debug print

            # Append Claude's response (assistant message)
            # The response content itself is a list of blocks, which is suitable for the 'assistant' role content
            self.messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason == "tool_use":
                tool_use_block = next((block for block in response.content if block.type == "tool_use"), None)
                if not tool_use_block:
                    # Should not happen if stop_reason is tool_use, but good to handle
                    print("Error: Stop reason is tool_use but no tool_use block found.")
                    return "An error occurred: Could not find tool use information."

                tool_name = tool_use_block.name
                tool_input = tool_use_block.input
                tool_use_id = tool_use_block.id

                print(f"   Executing tool: {tool_name} with input: {tool_input}") # Debug print
                try:
                    tool_result = self.registry.execute(tool_name, tool_input)
                    print(f"   Tool result: {tool_result}") # Debug print
                    result_content = json.dumps(tool_result)
                    is_error = False
                except Exception as e:
                    print(f"   Error executing tool {tool_name}: {e}")
                    result_content = json.dumps({"error": f"Failed to execute tool {tool_name}: {str(e)}"})
                    is_error = True

                # Feed tool result back into the conversation
                tool_result_message = {
                    "role": "user", # Tool results are sent back as a user message
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": result_content,
                            "is_error": is_error # Indicate if the tool execution failed
                        }
                    ]
                }
                self.messages.append(tool_result_message)
                # Continue the loop to get Claude's response based on the tool result
                continue

            elif response.stop_reason in ["end_turn", "max_tokens", "stop_sequence"]:
                # Find the final text response from Claude
                final_text_block = next((block for block in response.content if block.type == "text"), None)
                if final_text_block:
                    final_response = final_text_block.text
                    print(f"   Final response: {final_response}") # Debug print
                    return final_response
                else:
                    # Handle cases where the response might end without a text block (e.g., only tool use)
                    print("Warning: Conversation ended without a final text response from Claude.")
                    return "Claude finished processing." # Or some other indicator
            else:
                # Handle unexpected stop reasons
                print(f"Error: Unexpected stop reason: {response.stop_reason}")
                return f"An unexpected error occurred: {response.stop_reason}"


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

    print(f"Bot response: {bot.ask('SELECT name FROM users LIMIT 2;')}")

    print("\n--- Asking about unknown weather location ---")
    print(f"Bot response: {bot.ask('Whats the weather in Atlantis?')}")

    print("\n--- Asking with invalid SQL ---")
    print(f"Bot response: {bot.ask('SELECT non_existent_column FROM users;')}")


if __name__ == "__main__":
    main()
