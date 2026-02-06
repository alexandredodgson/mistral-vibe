# Configuration System

Mistral Vibe uses a flexible configuration system based on TOML files and environment variables.

## Configuration Files

Vibe looks for its main configuration in:
1.  **Project-local**: `./.vibe/config.toml`.
2.  **User-global**: `~/.vibe/config.toml`.

### Basic `config.toml` Structure

```toml
active_model = "devstral-2"
vim_keybindings = false

[project_context]
max_chars = 40000

[[mcp_servers]]
name = "fetch_server"
transport = "stdio"
command = "uvx"
args = ["mcp-server-fetch"]
```

## Environment Variable Overrides

Any setting in `config.toml` can be overridden by an environment variable prefixed with `VIBE_`. For nested keys, use double underscores.

Example:
- `VIBE_ACTIVE_MODEL="devstral-small"`
- `VIBE_PROJECT_CONTEXT__MAX_CHARS="50000"`

## API Keys

API keys are loaded from:
1.  Environment variables (e.g., `MISTRAL_API_KEY`).
2.  The `~/.vibe/.env` file.

## Discovery Paths

You can configure additional paths for Vibe to look for tools, agents, and skills:
- `tool_paths`: For custom tool definitions.
- `agent_paths`: For custom agent profiles.
- `skill_paths`: For custom skill directories.
