# Agentscript.rs

A Rust based interpreter for the Agentscript language.

## Syntax

### Invoke

Invoke a tool based on the [ToolsV1](https://github.com/agentsea/agent-tools) protocol.

An example of invoking the `Translator` tool to translate text from English to Spanish

```
We need to do translation <invoke tool="Translator" action="translate" parameters={"text": "Hello", "options": {"from": "en", "to": "es"}} />
```

## Python API

```sh
pip install agentscript
```

### Usage

Execute the tranlator tool from python

```python
from agentscript import Interpreter
from agent_tools import Tool, action

# Create a fake translator tool
class Translator(Tool):
    """A fake translator tool"""

    @action
    def translate(self, text: str, options: Dict[str, Any]) -> str:
        return "Hola"


# Create the interpreter supplying our translator tool
interpreter = Interpreter(tools=[Translator()])

# Parse the script, find the tool, and execute it
interpreter.execute("""
We need to do translation <invoke tool="Translator" action="translate" parameters={"text": "Hello", "options": {"from": "en", "to": "es"}} />
""")

# Show the past invocations with the results
print(interpreter.invocations())
```

## Devloping

When changing the rust code

```sh
make develop-rs
```

Will complile it and make the package available to the Python project.
