"""This script demonstrates how to change the timeout for tooltips.
This is achieved by monkey-patching the _handle_tooltip_timer method
of the Screen class in Textual. Pyright / Mypy do not like this file.
I'm not even gonna bother trying to type hint it (I can assure you it works).

Recipe by Edward Jazzhands"""

from __future__ import annotations
import sys

from textual.app import App
from textual.widgets import Static, Footer
from textual.widget import Widget
from textual.css.query import NoMatches
from textual.containers import Container
from textual.widgets._tooltip import Tooltip
from textual.screen import Screen
from rich.console import RenderableType


def _handle_tooltip_timer(self, widget: Widget) -> None:

    try:
        tooltip = self.get_child_by_type(Tooltip)
    except NoMatches:
        pass
    else:
        tooltip_content: RenderableType | None = None
        for node in widget.ancestors_with_self:
            if not isinstance(node, Widget):
                break
            if node.tooltip is not None:
                tooltip_content = node.tooltip
                break

        if tooltip_content is None:
            tooltip.display = False
        else:
            tooltip.display = True
            tooltip.absolute_offset = self.app.mouse_position
            tooltip.update(tooltip_content)

            self.set_timer(2.0, lambda: setattr(tooltip, "display", False))


# MONKEY PATCH:
Screen._handle_tooltip_timer = _handle_tooltip_timer


class TextualApp(App[None]):

    DEFAULT_CSS = """
    #my_container { align: center middle; }
    #my_static { border: solid blue; width: auto;}
    """

    def compose(self):

        self.log("Composing the app")

        with Container(id="my_container"):
            mystatic = Static("Hello, Textual!", id="my_static")
            yield mystatic
            mystatic.tooltip = "This is a tooltip"

        yield Footer()


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)