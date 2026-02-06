# Programmatic Usage

While Mistral Vibe is primarily a CLI tool for interactive use, it also supports non-interactive "programmatic" mode, which is useful for scripting and automation.

## CLI Flags for Automation

Use the `--prompt` flag to run Vibe non-interactively.

```bash
vibe --prompt "Analyze the code in @src/main.py"
```

### Automation Options

- `--prompt "<text>"`: The initial prompt for the agent.
- `--max-turns <N>`: Limit the maximum number of assistant turns.
- `--max-price <dollars>`: Interrupt the session if the cost exceeds this limit.
- `--enabled-tools <pattern>`: Only enable tools matching this pattern. In programmatic mode, this disables all other tools.
- `--output <format>`:
    - `text` (default): Human-readable text output.
    - `json`: Returns all messages as JSON at the end.
    - `streaming`: Outputs newline-delimited JSON per message.

## Example: Extraction as JSON

```bash
vibe --prompt "List all dependencies in @pyproject.toml" --output json > dependencies.json
```

## Input Piping

Vibe can also read from stdin:

```bash
cat error.log | vibe --prompt "Fix the errors shown in this log"
```
