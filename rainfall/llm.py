"""LLM provider for executing stub functions."""

import json
import google.generativeai as genai
from typing import Any

from rainfall.config import RainfallConfig
from rainfall.parser import StubFunction


SYSTEM_PROMPT = """You are a function executor. You receive a function signature, its arguments, and a description of what it should do.

Your job is to execute the function mentally and return ONLY the result value.

CRITICAL RULES:
1. Respond with ONLY the return value - no explanation, no markdown, no code.
2. For numbers, return just the number: 42
3. For strings, return just the string without quotes: Hello World
4. For booleans, return lowercase: true or false
5. For lists/dicts, return valid JSON: ["a", "b"] or {"key": "value"}
6. For None/null, return: null
7. Be deterministic - same inputs should give same outputs.
8. If you cannot determine the result, make a reasonable guess based on the function name and description.

EXAMPLES:
- calculate_tip(bill=50.0, quality="excellent") → 10.0
- is_palindrome("racecar") → true
- extract_emails("Contact: a@b.com, c@d.org") → ["a@b.com", "c@d.org"]
- summarize("Long text...") → A brief summary of the text.
- generate_greeting("Alice", formal=True) → Dear Alice,"""


class LLMProvider:
    """Gemini-based LLM provider for function execution."""
    
    def __init__(self, config: RainfallConfig):
        self.config = config
        genai.configure(api_key=config.api_key)
        self.model = genai.GenerativeModel(
            model_name=config.model,
            system_instruction=SYSTEM_PROMPT,
            generation_config={
                "temperature": config.temperature,
                "max_output_tokens": config.max_tokens,
            }
        )
    
    def execute_stub(self, stub: StubFunction, args: tuple, kwargs: dict) -> Any:
        """Execute a stub function via LLM."""
        prompt = self._build_prompt(stub, args, kwargs)
        
        if self.config.verbose:
            print(f"\n[Rainfall] Calling: {stub.name}")
            print(f"[Rainfall] Prompt:\n{prompt}")
        
        response = self.model.generate_content(prompt)
        raw_result = response.text.strip()
        
        if self.config.verbose:
            print(f"[Rainfall] Response: {raw_result}")
        
        return self._parse_response(raw_result, stub.return_type)
    
    def _build_prompt(self, stub: StubFunction, args: tuple, kwargs: dict) -> str:
        """Build the prompt for the LLM."""
        parts = [stub.to_prompt_context()]
        
        # Add actual argument values
        if args or kwargs:
            parts.append("\nCalled with:")
            
            # Map positional args to parameter names
            for i, (arg_name, arg_val) in enumerate(zip(stub.args, args)):
                parts.append(f"  {arg_name} = {repr(arg_val)}")
            
            # Add remaining kwargs
            for key, val in kwargs.items():
                parts.append(f"  {key} = {repr(val)}")
        
        parts.append("\nReturn the result:")
        
        return "\n".join(parts)
    
    def _parse_response(self, raw: str, return_type: str | None) -> Any:
        """Parse the LLM response into a Python value."""
        # Try JSON parsing first (handles lists, dicts, booleans, null)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass
        
        # Handle based on return type hint
        if return_type:
            rt_lower = return_type.lower()
            
            if rt_lower == "int":
                try:
                    return int(float(raw))
                except ValueError:
                    pass
            
            elif rt_lower == "float":
                try:
                    return float(raw)
                except ValueError:
                    pass
            
            elif rt_lower == "bool":
                return raw.lower() in ("true", "yes", "1")
            
            elif rt_lower == "str":
                return raw
        
        # Default: return as string
        return raw
