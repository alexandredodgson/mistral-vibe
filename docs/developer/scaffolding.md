# Project Scaffolding

Mistral Vibe provides built-in support for scaffolding new projects and components using templates.

## The `/scaffold` Command

You can trigger the scaffolding process directly from the interactive CLI using the `/scaffold` command. This will guide you through selecting a template and providing the necessary parameters.

## `ScaffoldProject` Tool

Under the hood, Vibe uses the `ScaffoldProject` tool, which is a wrapper around [cookiecutter](https://github.com/cookiecutter/cookiecutter).

- **Template Support**: Supports any valid cookiecutter template (local path or Git URL).
- **Integration**: The agent can use this tool to initialize new modules or sub-projects within your codebase according to established patterns.

## Dependencies

The scaffolding feature requires `cookiecutter` to be installed (included in Vibe's default dependencies).
