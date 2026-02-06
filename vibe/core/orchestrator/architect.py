from __future__ import annotations

import ast
from pathlib import Path
from typing import Dict, List

class Architect:
    def __init__(self, workdir: Path = Path(".")) -> None:
        self.workdir = workdir
        self.spec_file = workdir / "SPEC.md"
        self.arch_file = workdir / "ARCHITECTURE.md"

    def validate_spec(self) -> bool:
        """Checks if SPEC.md exists and is not empty."""
        return self.spec_file.exists() and len(self.spec_file.read_text().strip()) > 0

    def ensure_architecture_doc(self) -> None:
        if not self.arch_file.exists():
            content = """# Architecture

```mermaid
graph TD
    User -->|Input| CLI
    CLI --> Core
```
"""
            self.arch_file.write_text(content, encoding="utf-8")

    def generate_diagram_prompt(self, file_structure: str) -> str:
        """Returns a prompt to generate a Mermaid diagram based on file structure."""
        return f"""
Based on the following file structure, generate a Mermaid class diagram or flow chart that represents the architecture.
Output ONLY the mermaid block.

Structure:
{file_structure}
"""

    def analyze_dependencies(self, depth: int = 2) -> Dict[str, List[str]]:
        """
        Analyzes dependencies between modules in the project.
        depth: How deep to group modules (e.g. 1 for top-level, 2 for subpackages).
        """
        dependencies: Dict[str, List[str]] = {}
        py_files = list(self.workdir.rglob("*.py"))

        # First pass: map all internal modules
        internal_modules = set()
        for py_file in py_files:
            try:
                module_name = self._get_module_name(py_file)
                internal_modules.add(module_name)
            except Exception:
                continue

        for py_file in py_files:
            try:
                module_name = self._get_module_name(py_file)
                # Group module name by depth
                parts = module_name.split(".")
                source_node = ".".join(parts[:depth])

                if source_node not in dependencies:
                    dependencies[source_node] = []

                imports = self._extract_imports(py_file)
                for imp in imports:
                    # Check if it's an internal module (matches any internal module prefix)
                    is_internal = any(imp == m or imp.startswith(m + ".") for m in internal_modules)
                    if is_internal:
                        imp_parts = imp.split(".")
                        target_node = ".".join(imp_parts[:depth])
                        if target_node != source_node and target_node not in dependencies[source_node]:
                            dependencies[source_node].append(target_node)
            except Exception:
                continue

        return dependencies

    def generate_mermaid_graph(self, dependencies: Dict[str, List[str]]) -> str:
        lines = ["graph TD"]
        for source, targets in dependencies.items():
            for target in targets:
                lines.append(f"    {source} --> {target}")

        if len(lines) == 1:
            lines.append("    Empty --> Project")

        return "\n".join(lines)

    def _get_module_name(self, file_path: Path) -> str:
        try:
            relative = file_path.relative_to(self.workdir)
        except ValueError:
            # Fallback if file is not under workdir (should not happen with rglob)
            return file_path.stem

        parts = list(relative.parts)
        if parts[-1] == "__init__.py":
            parts.pop()
        else:
            parts[-1] = parts[-1].removesuffix(".py")
        return ".".join(parts)

    def _extract_imports(self, file_path: Path) -> List[str]:
        imports = []
        try:
            content = file_path.read_text(encoding="utf-8")
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        # Handle relative imports (dots)
                        if node.level > 0:
                            # We'd need current module to resolve, but let's keep it simple for now
                            # and just use the module name if present.
                            pass
                        imports.append(node.module)
        except Exception:
            pass
        return imports
