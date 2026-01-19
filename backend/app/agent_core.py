import json
import inspect
import traceback
from typing import List, Dict, Any, Callable, Optional, Union, get_type_hints
from openai import OpenAI
from pydantic import BaseModel

class ToolRegistry:
    """
    A helper to register python functions as OpenAI tools.
    """
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._schemas: List[Dict[str, Any]] = []

    def register(self, func: Callable):
        """
        Decorator to register a tool.
        Autogenerates schema from docstring and type hints (simplified).
        """
        self._tools[func.__name__] = func
        
        # Get type hints
        type_hints = get_type_hints(func)
        
        # Basic schema generation suitable for tech interview speed
        sig = inspect.signature(func)
        parameters = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        for name, param in sig.parameters.items():
            # Skip self/cls if present (though functional tools usually don't have them)
            if name in ['self', 'cls']: 
                continue

            param_type = "string" # Default fallback
            
            # Map Python types to JSON types
            hint = type_hints.get(name)
            if hint == int: param_type = "integer"
            elif hint == bool: param_type = "boolean"
            elif hint == float: param_type = "number"
            elif hint == list or hint == List: param_type = "array"
            elif hint == dict or hint == Dict: param_type = "object"
            
            parameters["properties"][name] = {
                "type": param_type,
                "description": f"Parameter {name}" 
            }
            if param.default == inspect.Parameter.empty:
                parameters["required"].append(name)

        schema = {
            "type": "function",
            "function": {
                "name": func.__name__,
                "description": func.__doc__ or "No description provided.",
                "parameters": parameters
            }
        }
        self._schemas.append(schema)
        print(f"[REGISTRY] Registered tool: {func.__name__}")
        return func

    def get_tool_schemas(self):
        return self._schemas

    def get_tool_func(self, name: str):
        return self._tools.get(name)


class AgentRuntime:
    """
    The brain that manages the LLM conversation loop.
    """
    def __init__(self, client: OpenAI, model: str = "openai/gpt-4o-mini", system_prompt: str = ""):
        self.client = client
        self.model = model
        self.system_prompt = system_prompt
        self.tools: ToolRegistry = ToolRegistry()
        self.memory: List[Dict[str, Any]] = []

    def set_tools(self, registry: ToolRegistry):
        self.tools = registry

    def reset_memory(self):
        """Clears all conversation history, keeping only the system prompt if needed."""
        self.memory = []
        if self.system_prompt:
            self.memory.append({"role": "system", "content": self.system_prompt})

    def add_message(self, role: str, content: str, tool_call_id: Optional[str] = None):
        msg = {"role": role, "content": content}
        if tool_call_id:
            msg["tool_call_id"] = tool_call_id
        self.memory.append(msg)

    def _execute_tool_call(self, tool_call) -> str:
        """Executes a single tool call and returns the result as JSON string."""
        func_name = tool_call.function.name
        arguments_json = tool_call.function.arguments
        
        print(f"\n[RUNTIME] 🛠️ Tool Call: {func_name}")
        print(f"[RUNTIME] 📥 Args: {arguments_json}")
        
        func = self.tools.get_tool_func(func_name)
        if not func:
            return json.dumps({"error": f"Tool {func_name} not found"})
        
        try:
            kwargs = json.loads(arguments_json)
            # Basic type conversion could happen here if needed, 
            # but usually it's better to let Python handle it or strict hints.
            result = func(**kwargs)
            
            result_str = json.dumps(result, default=str)
            print(f"[RUNTIME] 📤 Result: {result_str}")
            return result_str
        except Exception as e:
            traceback.print_exc()
            return json.dumps({"error": str(e)})

    def run(self, user_message: str, max_steps: int = 10) -> str:
        """
        Main ReAct Loop
        """
        # 1. Initialize Memory for this run
        if not self.memory:
            self.memory.append({"role": "system", "content": self.system_prompt})
        
        self.add_message("user", user_message)
        print(f"\n[RUNTIME] 👤 User: {user_message}")

        step = 0
        while step < max_steps:
            step += 1

            # 2. Call OpenAI
            print(f"\n[RUNTIME] ⏳ Step {step}: Thinking...")
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.memory,
                    tools=self.tools.get_tool_schemas() if self.tools.get_tool_schemas() else None,
                    tool_choice="auto" if self.tools.get_tool_schemas() else None
                )
            except Exception as e:
                return f"Error calling OpenAI: {str(e)}"

            msg = response.choices[0].message
            self.memory.append(msg.model_dump(exclude_none=True))

            # Debug Print
            if msg.content:
                print(f"[RUNTIME] 🤖 AI Says: {msg.content}")

            # 3. Handle Tool Calls
            if msg.tool_calls:
                for tool_call in msg.tool_calls:
                    result = self._execute_tool_call(tool_call)
                    
                    self.memory.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    })
                continue
            
            # 4. Final Response
            if msg.content:
                return msg.content
            
        return "Agent stopped: Max steps reached."