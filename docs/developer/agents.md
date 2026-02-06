# Custom Agents

Vibe allows you to define custom agent profiles to tailor the assistant's behavior, available models, and tool permissions.

## Agent Configuration

Agent profiles are defined in TOML files.

### Example: `researcher.toml`

```toml
# Researcher agent configuration
active_model = "devstral-2"
system_prompt_id = "researcher"
agent_type = "agent"

# Enable only search and read tools
enabled_tools = ["grep", "read_file", "mcp_google_search"]
disabled_tools = ["bash", "write_file", "search_replace"]

[tools.read_file]
permission = "always"

[tools.grep]
permission = "always"
```

## Configuration Fields

- `active_model`: The model alias to use for this agent.
- `system_prompt_id`: The ID of the system prompt to use (matches the filename in `prompts/` without `.md`).
- `agent_type`:
    - `agent`: A standard agent that interacts with the user.
    - `subagent`: An agent designed for delegation via the `task` tool.
- `enabled_tools` / `disabled_tools`: Lists of tool names or patterns (glob/regex) to enable or disable.
- `[tools.<name>]`: Tool-specific overrides, such as `permission` (`always`, `ask`, `never`).

## Agent Discovery

Vibe looks for agent profile TOML files in:
1.  **User-global**: `~/.vibe/agents/`.
2.  **Custom paths**: Any directories listed in `agent_paths` in `config.toml`.

## Using a Custom Agent

Invoke Vibe with the `--agent` flag followed by the name of your agent:

```bash
vibe --agent researcher
```
