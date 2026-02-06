# Model Context Protocol (MCP)

Mistral Vibe supports the [Model Context Protocol (MCP)](https://modelcontextprotocol.io), allowing you to connect to external servers that provide additional tools and context.

## Configuring MCP Servers

MCP servers are configured in your `config.toml` file under the `[[mcp_servers]]` section.

### stdio Transport (Local Processes)

Use this for MCP servers that run as local processes and communicate via standard input/output.

```toml
[[mcp_servers]]
name = "filesystem"
transport = "stdio"
command = "npx"
args = ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
env = { "DEBUG" = "1" }
```

### HTTP Transport (Remote Servers)

Use this for MCP servers hosted over HTTP. Both `http` and `streamable-http` transports are supported.

```toml
[[mcp_servers]]
name = "remote-tools"
transport = "http"
url = "https://mcp.example.com/api"
headers = { "Authorization" = "Bearer your-token" }
api_key_env = "MY_TOKEN_ENV_VAR"
```

## Tool Naming

MCP tools are automatically registered in Vibe with a name following the pattern:
`{server_name}_{tool_name}`

For example, if the `filesystem` server provides a `list_directory` tool, it will be available in Vibe as `filesystem_list_directory`.

## Permissions

You can configure permissions for MCP tools just like built-in tools:

```toml
[tools.filesystem_list_directory]
permission = "always"
```
