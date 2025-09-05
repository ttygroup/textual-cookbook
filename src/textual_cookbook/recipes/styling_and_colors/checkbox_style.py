"""This script demonstrates how to modify the style of 
a Checkbox widget. It shows removing the label highlight
when focused as well as changing the color of the check symbol
in the 'on' state.

Recipe by Edward Jazzhands"""

import sys
from textual.app import App
from textual.widgets import Static, Footer, Checkbox, Button
from textual.containers import Container

class TextualApp(App[None]):

    CSS = """
    Screen { align: center middle; }    
    #my_container { width: auto; height: auto; border: solid red;
    align: center middle; content-align: center middle; }
    Checkbox { 
        &.-on > .toggle--button {
            color: $text-success;
            background: green;
        }
        &:focus {
            & > .toggle--label {
                background: transparent;
            }
        }
    } 
    """
    
    def compose(self):

        with Container(id="my_container"):
            yield Static("Hello, Textual!")
            yield Checkbox("My Checkbox")
            yield Button()

        yield Footer()


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)