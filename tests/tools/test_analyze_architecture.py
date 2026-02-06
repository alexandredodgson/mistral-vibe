import pytest
import os
from pathlib import Path
from vibe.core.tools.builtins.analyze_architecture import AnalyzeArchitecture, AnalyzeArchitectureArgs, AnalyzeArchitectureToolConfig
from vibe.core.tools.base import InvokeContext

@pytest.mark.asyncio
async def test_analyze_architecture_tool(tmp_path):
    # Setup
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "__init__.py").touch()
    (pkg / "a.py").write_text("import pkg.b")
    (pkg / "b.py").touch()

    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        tool = AnalyzeArchitecture.from_config(AnalyzeArchitectureToolConfig())
        args = AnalyzeArchitectureArgs(depth=2, update_docs=False)
        ctx = InvokeContext(tool_call_id="test")

        events = []
        async for event in tool.run(args, ctx):
            events.append(event)

        assert len(events) == 1
        result = events[0]
        assert "pkg.a --> pkg.b" in result.mermaid_graph
    finally:
        os.chdir(old_cwd)

@pytest.mark.asyncio
async def test_analyze_architecture_tool_update_docs(tmp_path):
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "__init__.py").touch()
    (pkg / "a.py").write_text("import pkg.b")
    (pkg / "b.py").touch()

    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        tool = AnalyzeArchitecture.from_config(AnalyzeArchitectureToolConfig())
        args = AnalyzeArchitectureArgs(depth=2, update_docs=True)
        ctx = InvokeContext(tool_call_id="test")

        async for _ in tool.run(args, ctx):
            pass

        arch_file = tmp_path / "ARCHITECTURE.md"
        assert arch_file.exists()
        content = arch_file.read_text()
        assert "pkg.a --> pkg.b" in content
    finally:
        os.chdir(old_cwd)
