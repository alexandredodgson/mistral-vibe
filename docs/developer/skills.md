# Skills System

Skills are reusable components that package tools, prompts, and slash commands. Vibe follows the [Agent Skills specification](https://agentskills.io/specification).

## Skill Structure

A skill is a directory containing a `SKILL.md` file at its root.

```
my-skill/
├── SKILL.md
├── tools/
│   └── my_tool.py
└── prompts/
    └── my_prompt.md
```

### `SKILL.md` Metadata

The `SKILL.md` file must contain YAML frontmatter with metadata.

```markdown
---
name: my-skill
description: A description of what this skill does
license: MIT
version: 0.1.0
user-invocable: true
allowed-tools:
  - read_file
  - bash
---

# My Skill

This skill provides additional capabilities for...
```

- `name`: Unique identifier for the skill (lowercase, numbers, and hyphens only).
- `user-invocable`: If true, the skill can be invoked directly by the user via a slash command (`/my-skill`).
- `allowed-tools`: List of tools the skill is permitted to use when delegated to.

## Skill Discovery

Vibe searches for skills in:
1.  **Project-local**: `.vibe/skills/` in your project.
2.  **User-global**: `~/.vibe/skills/`.
3.  **Custom paths**: Any paths listed in `skill_paths` in `config.toml`.

## Enabling and Disabling Skills

In your `config.toml`, you can control which skills are loaded:

```toml
enabled_skills = ["code-review", "test-*"]
disabled_skills = ["experimental-*"]
```

## Custom Slash Commands

By setting `user-invocable = true` in `SKILL.md`, you automatically create a slash command with the skill's name. When invoked, Vibe starts a subagent session scoped to this skill.
