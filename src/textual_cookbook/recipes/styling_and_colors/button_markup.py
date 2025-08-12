"""This example demonstrates how to create a button with markup text.

Recipe by Edward Jazzhands"""

import sys
from textual.app import App
from textual.widgets import Footer, Button
from textual.containers import Container
from textual.content import Content

class TextualApp(App[None]):

    CSS = """
    #my_container { 
        width: 1fr; height: 1fr;
        border: solid red;
        align: center middle; content-align: center middle;
    }
    /* This just removes the focus highlight from the button text: */
    .buttons { &:focus {text-style: bold;} }
    """
    
    def compose(self):

        with Container(id="my_container"):
            button = Button(
                Content.from_markup("[yellow]This[/yellow] is my [red]button"),
                classes="buttons"
            )
            yield button
            yield Button("This is a normal button")
        yield Footer()


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)