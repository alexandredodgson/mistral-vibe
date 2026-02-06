# Custom Tools

Mistral Vibe allows you to extend its capabilities by creating custom tools. Tools are Python classes that inherit from `BaseTool` and define their inputs and outputs using Pydantic models.

## Anatomy of a Tool

A tool consists of:
1.  **Arguments Model**: A Pydantic `BaseModel` defining the input parameters.
2.  **Result Model**: A Pydantic `BaseModel` defining the output.
3.  **Config Model**: (Optional) Configuration settings for the tool.
4.  **State Model**: (Optional) For keeping track of state across multiple calls.
5.  **Run Method**: An asynchronous generator that performs the tool's action.

### Basic Example

```python
from collections.abc import AsyncGenerator
from typing import ClassVar
from pydantic import BaseModel, Field
from vibe.core.tools.base import BaseTool, BaseToolConfig, BaseToolState, InvokeContext
from vibe.core.types import ToolStreamEvent

class MyToolArgs(BaseModel):
    message: str = Field(description="The message to echo")

class MyToolResult(BaseModel):
    echo: str

class MyTool(BaseTool[MyToolArgs, MyToolResult, BaseToolConfig, BaseToolState]):
    description: ClassVar[str] = "A simple tool that echoes a message."

    async def run(
        self, args: MyToolArgs, ctx: InvokeContext | None = None
    ) -> AsyncGenerator[ToolStreamEvent | MyToolResult, None]:
        yield MyToolResult(echo=f"Echo: {args.message}")
```

## InvokeContext

The `InvokeContext` provides access to session-level resources:
- `tool_call_id`: Unique ID for the current tool call.
- `agent_manager`: Access to the agent manager (for delegating tasks).
- `approval_callback`: To request user approval.
- `user_input_callback`: To ask questions to the user.

## Tool Discovery

Vibe looks for custom tools in:
1.  **Project-local**: `.vibe/tools/` in your project directory.
2.  **User-global**: `~/.vibe/tools/`.
3.  **Custom paths**: Configured via `tool_paths` in `config.toml`.
4.  **Skills**: Bundled with active skills.

## Built-in Tools

Vibe comes with several built-in tools that can be used as references:
- `read_file`, `write_file`, `search_replace`: Core file manipulation.
- `bash`: Shell command execution.
- `grep`: Code search.
- `task`: Subagent delegation.
- `ScaffoldProject`: Wraps `cookiecutter` to initialize projects from templates.

## UI Customization

To customize how your tool appears in the Vibe UI, inherit from `ToolUIData` and implement methods to return display summaries and status text.
