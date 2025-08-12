"""This example shows how to use the rich library to display a spinner in Textual.
The spinner object changes its rendering internally, but Textual needs to be manually updated
to reflect that change. This is done by using `set_interval` to call the `update_spinner` method.

Recipe by Edward Jazzhands"""

from __future__ import annotations
import sys
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
	from rich.console import RenderableType
from rich.spinner import Spinner


from textual.app import App
from textual.widgets import Static

class SpinnerWidget(Static):

    def __init__(self, spinner: str, text: RenderableType, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._spinner = Spinner(spinner, text)  

    def on_mount(self) -> None:
        self.set_interval(0.02, self.update_spinner)

    def update_spinner(self) -> None:
        self.update(self._spinner)

class TextualApp(App[None]):

    CSS = """
        SpinnerWidget {width: 1fr; height: 1fr; content-align: center middle;}
    """

    def compose(self):

        yield SpinnerWidget("line", "Loading...")
        # A few common options:
        # arc, arrow, bouncingBall, boxBounce, dots, dots2 to dots12, line
        # python -m rich.spinner to see all options


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)