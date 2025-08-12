"""This file demonstrates ?

Recipe by Edward Jazzhands"""


import sys
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.widgets import Button, RichLog


class TextualApp(App[None]):
    CSS = """
    #buttons {
        dock: top;
        height: auto;
    }
    """

    count = reactive(0, always_update=True)

    def validate_count(self, count: int) -> int:
        """Validate value."""
        self.log(f"ValidatING {count=}")

        if count < 0:
            self.log("Count cannot be negative")
            count = 0
        elif count > 10:
            self.log("Count cannot be greater than 10")
            count = 10

        self.log(f"Validated {count=}")
        return count

    def watch_count(self, count: int) -> None:
        """Watch for changes to count."""
        self.log(f"Count changed to {count=}")

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Button("+1", id="plus", variant="success"),
            Button("-1", id="minus", variant="error"),
            id="buttons",
        )
        yield RichLog(highlight=True)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "plus":
            self.count += 1
        else:
            self.count -= 1
        self.query_one(RichLog).write(f"count = {self.count}")


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)