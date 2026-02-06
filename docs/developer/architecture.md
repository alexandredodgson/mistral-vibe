# Architecture Overview

Mistral Vibe is built on a modular, agentic orchestrator architecture designed for extensibility and reliability.

## Agent Loop and Orchestration

The core execution engine is the `AgentLoop`, which manages the interaction between the user, the LLM, and the available tools. To enhance the agent's capabilities, Vibe integrates an `Orchestrator` and `OrchestratorMiddleware`.

- **`Orchestrator`**: The central component that coordinates specialized modules to handle complex tasks, planning, and state management.
- **`OrchestratorMiddleware`**: Integrated into the `AgentLoop`, this middleware allows the orchestrator to intercept and augment messages, providing the agent with necessary context and guidance from the specialized modules.

## Orchestrator Modules

The `Orchestrator` (located in `vibe/core/orchestrator/`) is composed of several specialized modules:

1.  **Planning**: Responsible for breaking down complex user requests into a sequence of actionable steps. It maintains the high-level goal and tracks progress using files like `brainfile.md`.
2.  **Persistence**: Handles session state, message history, and tool outputs. It ensures that the agent's state is preserved across turns and sessions using `STATE.md` and `DECISION_LOG.md`.
3.  **Architect**: Analyzes the codebase and project structure. It ensures that architectural decisions are documented (e.g., in `SPEC.md` and `ARCHITECTURE.md`) and provides relevant context to the agent.
4.  **Scaffolding**: Handles project initialization and boilerplate generation. It leverages tools like `cookiecutter` via the `ScaffoldProject` tool and the `/scaffold` CLI command.

## Message Flow

1.  **User Input**: Captured via the CLI (interactive or `--prompt`).
2.  **Middleware**: Processors (including `OrchestratorMiddleware`) that modify the input, such as expanding `@file` references, adding system context, or injecting planning/state information.
3.  **Agent Loop**:
    - The LLM receives the augmented prompt and history.
    - The LLM decides to respond with text or a tool call.
    - **Tool Execution**: If a tool is called, Vibe checks permissions, optionally asks for user approval, and then executes the tool.
    - **Observation**: The tool result is fed back into the history and processed by the orchestrator modules.
4.  **Response**: The final answer is displayed to the user.

## Extension Points

Vibe is designed to be extended through:
- **Custom Tools**: New Python-based capabilities.
- **Skills**: Bundled tools and specialized prompts.
- **MCP**: Connecting to external services via the Model Context Protocol.
- **Custom Agents**: Tailored personas and configurations.
