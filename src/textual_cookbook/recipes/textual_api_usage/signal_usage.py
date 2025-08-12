"""This file demonstrates the usage of Textual's secret 'Signal' class.
This isn't a public API, but it is used internally by Textual.
It allows widgets to communicate with each other without sending events
or passing in direct references to anything.

Recipe by Edward Jazzhands"""

import sys
from textual import on
from textual.app import App, ComposeResult
from textual.signal import Signal
from textual.widget import Widget
from textual.widgets import Static, Button, Footer


class MyManager(Widget):

    def __init__(self):
        super().__init__()
        self.display = False

        self.my_special_num = 42
        self.my_signal: Signal[int] = Signal(self, "my_signal")

    def send_signal(self):
        self.my_signal.publish(self.my_special_num)


class TextualApp(App[None]):

    CSS = """
    Screen { align: center middle; }
    #my_static { border: solid blue; width: auto;}
    """

    BINDINGS = [
        ("b", "send_signal", "Send Signal"),
    ]

    def __init__(self):
        super().__init__()
        self.manager = MyManager()

    def compose(self) -> ComposeResult:
        self.manager = MyManager()
        yield self.manager

        yield Static("Press button or press b", id="my_static")
        yield Button("Send Signal", id="send_signal_button")
        yield Footer()

    def on_mount(self) -> None:
        self.manager.my_signal.subscribe(self, self.on_my_signal)

    @on(Button.Pressed, "#send_signal_button")
    def action_send_signal(self):
        self.manager.send_signal()

    def on_my_signal(self, value: int):
        self.notify(f"Received signal with value: {value}")


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)