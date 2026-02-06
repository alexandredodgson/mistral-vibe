from __future__ import annotations

from collections.abc import AsyncGenerator
from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel, Field

from vibe.core.orchestrator.architect import Architect
from vibe.core.tools.base import (
    BaseTool,
    BaseToolConfig,
    BaseToolState,
    InvokeContext,
    ToolPermission,
)
from vibe.core.tools.ui import ToolCallDisplay, ToolResultDisplay, ToolUIData
from vibe.core.types import ToolCallEvent, ToolResultEvent, ToolStreamEvent


class AnalyzeArchitectureArgs(BaseModel):
    depth: int = Field(
        default=2, description="Grouping depth for modules (1=top-level, 2=subpackages)."
    )
    update_docs: bool = Field(
        default=False, description="Whether to update ARCHITECTURE.md with the generated graph."
    )


class AnalyzeArchitectureResult(BaseModel):
    mermaid_graph: str
    updated_file: str | None = None


class AnalyzeArchitectureToolConfig(BaseToolConfig):
    permission: ToolPermission = ToolPermission.ALWAYS


class AnalyzeArchitecture(
    BaseTool[
        AnalyzeArchitectureArgs,
        AnalyzeArchitectureResult,
        AnalyzeArchitectureToolConfig,
        BaseToolState,
    ],
    ToolUIData[AnalyzeArchitectureArgs, AnalyzeArchitectureResult],
):
    description: ClassVar[str] = (
        "Analyzes project dependencies using static analysis and generates a Mermaid diagram."
    )

    async def run(
        self, args: AnalyzeArchitectureArgs, ctx: InvokeContext | None = None
    ) -> AsyncGenerator[ToolStreamEvent | AnalyzeArchitectureResult, None]:
        # In Vibe, the current working directory is typically the project root.
        architect = Architect(workdir=Path.cwd())

        deps = architect.analyze_dependencies(depth=args.depth)
        graph = architect.generate_mermaid_graph(deps)

        updated_file = None
        if args.update_docs:
            content = f"# Architecture\n\n```mermaid\n{graph}\n```\n"
            architect.arch_file.write_text(content, encoding="utf-8")
            updated_file = str(architect.arch_file)

        yield AnalyzeArchitectureResult(mermaid_graph=graph, updated_file=updated_file)

    @classmethod
    def get_call_display(cls, event: ToolCallEvent) -> ToolCallDisplay:
        return ToolCallDisplay(summary="Analyzing project architecture")

    @classmethod
    def get_result_display(cls, event: ToolResultEvent) -> ToolResultDisplay:
        if isinstance(event.result, AnalyzeArchitectureResult):
            msg = "Architecture analyzed"
            if event.result.updated_file:
                msg += f" and updated {event.result.updated_file}"
            return ToolResultDisplay(success=True, message=msg)
        return ToolResultDisplay(success=True, message="Analysis complete")

    @classmethod
    def get_status_text(cls) -> str:
        return "Analyzing architecture"
