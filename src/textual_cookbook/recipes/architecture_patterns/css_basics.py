"""This file is a very simple example of how to use Textual CSS to
set the sizes and borders of widgets.

Recipe by Edward Jazzhands"""

import sys
from textual import on
from textual.app import App
from textual.widgets import Button, RichLog, Footer
from textual.containers import Container


class TextualApp(App[None]):

    CSS = """
    Screen { align: center middle; }
    RichLog { 
        border: solid blue; 
        width: 70%;
        height: 1fr;
    }
    #button_container {
        border: solid green;
        height: 15;
    }
    """

    BINDINGS = [
        ("g", "send_log_msg", "Send a Log Message"),
    ]

    def compose(self):

        yield RichLog()
        with Container(id="button_container"):
            yield Button("Click to send log msg", id="my_button")
        yield Footer()

    @on(Button.Pressed, "#my_button")
    def action_send_log_msg(self):
        self.query_one(RichLog).write("This is a log message")


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)