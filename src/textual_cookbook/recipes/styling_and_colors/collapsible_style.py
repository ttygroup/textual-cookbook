"""This file shows how to change the color and style of the
title/header of a Collapsible widget in Textual.

Recipe by Edward Jazzhands"""

import sys
from textual.app import App
from textual.widgets import Collapsible, Button


class TextualApp(App[None]):

    CSS = """
    Screen { align: center middle; }
    Collapsible { 
        width: 50%; height: auto; 
        CollapsibleTitle {
            background: transparent;
            color: blue;    /* text color */
        }
    }
    """

    def compose(self):

        for _ in range(3):
            with Collapsible():
                for _ in range(3):
                    yield Button("Hello, Textual!")


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)