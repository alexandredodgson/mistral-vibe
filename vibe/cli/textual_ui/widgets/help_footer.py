from __future__ import annotations

from typing import Any

from vibe.cli.textual_ui.widgets.no_markup_static import NoMarkupStatic


class HelpFooter(NoMarkupStatic):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.update("Ctrl+O: Tools • Ctrl+T: Todo • Shift+Tab: Auto-Approve")
