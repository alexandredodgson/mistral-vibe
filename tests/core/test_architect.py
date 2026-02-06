from pathlib import Path
import pytest
from vibe.core.orchestrator.architect import Architect

def test_analyze_dependencies(tmp_path):
    # Setup a dummy project structure
    root = tmp_path / "root"
    root.mkdir()

    project = root / "my_project"
    project.mkdir()
    (project / "__init__.py").touch()

    core = project / "core"
    core.mkdir()
    (core / "__init__.py").touch()
    (core / "utils.py").write_text("import my_project.db")

    db = project / "db"
    db.mkdir()
    (db / "__init__.py").touch()
    (db / "models.py").write_text("from my_project.core.utils import helper")

    architect = Architect(workdir=root)
    deps = architect.analyze_dependencies(depth=2)

    # Expected:
    # my_project.core -> my_project.db
    # my_project.db -> my_project.core

    assert "my_project.core" in deps
    assert "my_project.db" in deps["my_project.core"]

    assert "my_project.db" in deps
    assert "my_project.core" in deps["my_project.db"]

def test_generate_mermaid_graph():
    deps = {
        "A": ["B", "C"],
        "B": ["C"]
    }
    architect = Architect()
    graph = architect.generate_mermaid_graph(deps)
    assert "graph TD" in graph
    assert "A --> B" in graph
    assert "A --> C" in graph
    assert "B --> C" in graph

def test_get_module_name():
    architect = Architect(workdir=Path("/tmp/foo"))
    assert architect._get_module_name(Path("/tmp/foo/bar/baz.py")) == "bar.baz"
    assert architect._get_module_name(Path("/tmp/foo/bar/__init__.py")) == "bar"
