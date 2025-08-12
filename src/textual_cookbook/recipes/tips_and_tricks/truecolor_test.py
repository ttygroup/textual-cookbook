"""This script demonstrates how Textual can detect the color system
in use and display a message accordingly.

Recipe by Edward Jazzhands"""

import sys
from textual.app import App
from textual.widgets import Static, Footer
from textual.containers import Container

class TextualApp(App[None]):

    DEFAULT_CSS = """
    Screen { width: 1fr; height: 1fr;}
    #my_static { border: solid blue; width: auto;}
    """
    
    def compose(self):

        with Container(id="my_container"):
            yield Static("Hello, Textual!", id="my_static")

        yield Footer()

    def on_ready(self):

        color_system = self.app.console.color_system

        if color_system == "256":
            self.notify("256 colors")
        elif color_system == "truecolor":
            self.notify("True color")
        elif color_system == "standard":
            self.notify("Standard color")
        else:
            self.notify("Unknown color system")

        # possibly set os.environ afterwards??
        # import os
        # os.environ["COLORTERM"] = "truecolor"


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)