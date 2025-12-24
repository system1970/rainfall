# 🌧️ Rainfall

> **Call functions that don't exist. Let AI figure it out.**

Rainfall is a Python CLI that runs your scripts and uses AI to execute stub functions. Write the function signature and docstring, leave the body as `...`, and Rainfall fills in the gaps.

## Installation

```bash
pip install rainfall
```

Or install from source:

```bash
git clone https://github.com/yourusername/rainfall.git
cd rainfall
pip install -e .
```

## Quick Start

**1. Set your Gemini API key:**

```bash
export GEMINI_API_KEY=your_api_key_here
```

Get a free API key at [Google AI Studio](https://aistudio.google.com/app/apikey).

**2. Write a Python script with stub functions:**

```python
# my_script.py

def calculate_tip(bill: float, quality: str) -> float:
    """
    Calculate tip based on bill amount and service quality.
    Quality can be: 'poor', 'okay', 'good', 'excellent'
    Returns the tip amount in dollars.
    """
    ...


def is_palindrome(text: str) -> bool:
    """Check if the given text is a palindrome (ignoring case and spaces)."""
    ...


# Use them like normal functions
tip = calculate_tip(85.50, "excellent")
print(f"Tip: ${tip}")

print(f"'racecar' is palindrome: {is_palindrome('racecar')}")
print(f"'hello' is palindrome: {is_palindrome('hello')}")
```

**3. Run with Rainfall:**

```bash
rainfall my_script.py
```

**Output:**

```
Tip: $17.1
'racecar' is palindrome: True
'hello' is palindrome: False
```

## How It Works

1. **Parse**: Rainfall scans your Python file for stub functions (functions with `...`, `pass`, or `raise NotImplementedError` as their body)
2. **Intercept**: When running your script, Rainfall replaces these stubs with AI-powered wrappers
3. **Execute**: When a stub is called, Rainfall sends the function name, signature, docstring, and arguments to the LLM
4. **Return**: The LLM infers what the function should return and sends back the result

## CLI Reference

```bash
rainfall <script.py> [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--api-key KEY` | Gemini API key (or set `GEMINI_API_KEY` env var) |
| `--model MODEL` | Model to use (default: `gemini-2.0-flash`) |
| `--verbose, -v` | Show LLM prompts and responses |
| `--dry-run` | List detected stubs without executing |
| `--temperature FLOAT` | LLM temperature 0-1 (default: 0.2) |

**Examples:**

```bash
# Run with verbose output
rainfall my_script.py --verbose

# See which functions would be AI-powered
rainfall my_script.py --dry-run

# Use a different model
rainfall my_script.py --model=gemini-1.5-pro
```

## Best Practices

### Write Descriptive Docstrings

The docstring is your prompt. Be specific about what the function should do:

```python
# ❌ Vague - AI has to guess
def process(data):
    """Process the data."""
    ...

# ✅ Specific - AI knows exactly what to do
def extract_person_info(text: str) -> dict:
    """
    Extract person information from unstructured text.
    
    Returns a dict with keys:
    - name: full name (str)
    - age: age if mentioned (int or None)  
    - email: email if found (str or None)
    """
    ...
```

### Use Type Hints

Return types help the AI format responses correctly:

```python
def get_count() -> int: ...      # Returns: 42
def get_names() -> list: ...     # Returns: ["Alice", "Bob"]
def is_valid() -> bool: ...      # Returns: true/false
def get_data() -> dict: ...      # Returns: {"key": "value"}
```

### Provide Examples

Include examples in your docstring for complex behavior:

```python
def analyze_sentiment(text: str) -> str:
    """
    Analyze the emotional sentiment of text.
    
    Returns one of: 'positive', 'negative', 'neutral'
    
    Examples:
        "I love this!" → 'positive'
        "This is terrible" → 'negative'
        "It's okay" → 'neutral'
    """
    ...
```

## Limitations

Rainfall uses LLMs to **reason** about what functions should return. It cannot:

- ❌ Make actual HTTP requests
- ❌ Read or write files
- ❌ Access databases
- ❌ Execute system commands
- ❌ Access real-time data

It **can** do:

- ✅ Math and calculations
- ✅ Text processing and analysis
- ✅ Data transformation
- ✅ Logic and classification
- ✅ Generate text content

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Your Gemini API key (recommended) |
| `RAINFALL_API_KEY` | Alternative name for API key |

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions welcome! Please open an issue or PR on GitHub.
