"""this file is a work in progress please ignore

Recipe by Edward Jazzhands"""

from __future__ import annotations
import sys
# import importlib.resources
from pathlib import Path

from textual.app import App, ComposeResult

from textual.screen import ModalScreen
from textual.widgets import Markdown
from textual.containers import VerticalScroll
from textual.binding import Binding
from textual.widgets import Static, Footer


class HelpScreen(ModalScreen[None]):

    BINDINGS = [
        Binding("escape,enter", "close_screen", description="Close the help window.", show=True),
    ]

    def __init__(self, anchor: str | None = None) -> None:
        super().__init__()
        self.anchor_line = anchor

    def compose(self) -> ComposeResult:

        help_path = Path(__file__).parent / "help.md"
        if not help_path.exists():
            raise FileNotFoundError(f"Help file not found at {help_path}")
        with help_path.open(encoding="utf-8") as f:
            self.help = f.read()

        with VerticalScroll(classes="screen_container help"):
            yield Markdown(self.help)

    def on_mount(self) -> None:
        self.query_one(VerticalScroll).focus()
        if self.anchor_line:
            found = self.query_one(Markdown).goto_anchor(self.anchor_line)
            if not found:
                self.log.error(f"Anchor '{self.anchor_line}' not found in help document.")

    def on_click(self) -> None:
        self.dismiss()

    def action_close_screen(self) -> None:
        self.dismiss()

    def go_to_anchor(self, anchor: str) -> None:
        """Scroll to a specific anchor in the help screen."""

class TextualApp(App[None]):

    CSS = """
    Screen { align: center middle; }
    #my_static { border: solid blue; width: auto;}
    """


    def compose(self):

        yield Static("Hello, Textual!", id="my_static")
        yield Footer()

    def action_binding(self):
        self.notify("You pressed the 'b' key!")


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)