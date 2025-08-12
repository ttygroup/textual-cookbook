"""This script demonstrates how you cannot use the same widget in multiple places.
The second Static `widget2` will not be displayed twice because it is already
displayed in the first container.

Example by Edward Jazzhands, 2025"""

from textual.app import App
from textual.widgets import Static, Footer
from textual.containers import Container

class TextualApp(App[None]):

    DEFAULT_CSS = """
    #my_container {
        width: 1fr; height: 1fr;
        border: solid red;
        align: center middle; content-align: center middle;
    }
    Static { border: solid blue; width: auto;}
    """
    
    def compose(self):

        widget = Static("Hello, Textual!")
        widget2 = Static("Hello, Textual! 2")

        with Container(id="my_container"):
            yield widget2
        with Container(id="my_container2"):
            yield widget
            yield widget2

        yield Footer()


TextualApp().run()