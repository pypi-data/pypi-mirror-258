<!-- PROJECT LOGO -->
<br />
<p align="center">
  <!-- <a href="https://github.com/agentsea/skillpacks">
    <img src="https://project-logo.png" alt="Logo" width="80">
  </a> -->

  <h1 align="center">Agentscript</h1>

  <p align="center">
    A programming language for AI agents
    <br />
    <a href="https://github.com/agentsea/skillpacks"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/agentsea/skillpacks">View Demo</a>
    ·
    <a href="https://github.com/agentsea/skillpacks/issues">Report Bug</a>
    ·
    <a href="https://github.com/agentsea/skillpacks/issues">Request Feature</a>
  </p>
</p>

Agentscript is an isomorphic programming language for AI agents, it includes both a server-side interpreter and browser-based renderer.

▶ On the server, agenscript directly interprets LMM outputs and executes actions in a streaming manner.

▶ In the browser, agentscript renders LLM outputs in a rich manner and provides live updates.

## Server-side Interpreter

The server side interpreter is implemented in [agentscript.rs](https://github.com/agentsea/agentscript.rs) and provides a Python interface

### Install

```bash
pip install agentscript
```

## Usage

Execute the translator tool from python

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
We need to do translation <Invoke tool="Translator" action="translate" parameters={"text": "Hello", "options": {"from": "en", "to": "es"}} />
""")

# Show the past invocations with the results
print(interpreter.invocations())
```

## Browser-based Renderer

### Install

```
npm i @agentsea/agentscript
```

### Usage

```javascript
import Agentscript from "@agentsea/agentscript";

(
  <Agentscript text="I created this image for you <Image url='https://any.url' />">
)
```

### Components

#### Boolean

```js
(
  <Agentscript text="Does this work for you? <Boolean />">
)
```

#### Image

```js
(
  <Agentscript text="I created this image for you <Image src='https://any.url' />">
)
```

## Dialects

The above components are known as the `common` dialect, but you can create your own dialects as well

## Roadmap

### Programable LLMs

Give agentscript the ability to program an LLM. Here we load a LoRA into a PEFT compatible LLM

```python
interpreter.execute("I need to load the weather LoRA <load lora='weather' />")
```

### Browser components

- [ ] Select One
- [ ] Select Any
- [ ] Image
- [ ] Video
- [ ] Plan
- [ ] References
- [ ] Image with bounding box
- [ ] Action
- [ ] Task

## Develop

To test

```sh
make test
```
