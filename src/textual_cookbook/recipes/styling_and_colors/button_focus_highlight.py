"""This demonstrates how to remove the focus highlight from buttons in Textual.
Note that the buttons are still focusable, but they will not show the
default focus highlight.

Recipe by Edward Jazzhands"""

import sys
from textual.app import App
from textual.widgets import Button
from textual.containers import Container

class TextualApp(App[None]):

    CSS = """
    #my_container { width: 1fr; height: 1fr; align: center middle; }
    .my_button {&:focus {text-style: none;}}
    """
    
    def compose(self):

        with Container(id="my_container"):
            yield Button("Button1", classes="my_button")
            yield Button("Button2", classes="my_button")
            yield Button("Button3", classes="my_button")


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)