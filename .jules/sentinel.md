## 2026-02-07 - Path Traversal in File Tools
**Vulnerability:** `ReadFile`, `SearchReplace`, and `Grep` tools allowed accessing files outside the project directory using relative paths (e.g., `../../`) or symlinks, because they lacked a check to ensure the resolved path was within the project root.
**Learning:** `Path.resolve()` resolves symlinks and relative segments but does NOT raise an error if the path is outside the current working directory. `Path.relative_to(base)` is required to enforce sandboxing.
**Prevention:** Always use `path.resolve().relative_to(root)` when handling file paths from user/LLM input.
