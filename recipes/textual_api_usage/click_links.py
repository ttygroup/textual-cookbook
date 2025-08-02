"""This script demonstrates how to use click links.

Recipe by Edward Jazzhands"""

from textual.app import App, ComposeResult
from textual.widgets import Label

class ContentClick(App[None]):

    BINDINGS = [
        ("f2", "show_note", "Show Notification"),
    ]

    def compose(self) -> ComposeResult:
        yield Label("Play the [on green @click=app.bell]bells[/] today!")
        yield Label("Show a [@click=app.show_note]notification[/]!")

    def action_show_note(self) -> None:
        self.notify("Action activated!")


if __name__ == "__main__":
    app = ContentClick()
    app.run()