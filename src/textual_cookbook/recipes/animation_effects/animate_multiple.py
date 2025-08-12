"""This file demonstrates how Textual can animate multiple widgets at once.
I'm honestly not sure exactly of how it handles it internally, but it
seems to work fine when you simply run the animate method multiple times
in a row. It will make them all run simultaneously.

Recipe by Edward Jazzhands"""

import sys
from textual.app import App
from textual.widgets import Static, Button
from textual.containers import Container
from textual.geometry import Offset

class TextualApp(App[None]):

    CSS = """
    #my_container { align: center middle; border: solid red;}
    #my_static1, #my_static2 { border: solid blue; width: auto;}
    """
    duration = 1.0

    def compose(self):

        with Container(id="my_container"):

            self.static1 = Static("Static 1", id="my_static1")
            self.static2 = Static("Static 2", id="my_static2")
            yield self.static1
            yield self.static2
            yield Button("press me")

    def on_button_pressed(self):
        self.static1.animate(
            "offset",
            Offset(20, 0),
            duration=self.duration,
        ) 
        self.static2.animate(
            "offset",
            Offset(20, 0),
            duration=self.duration,
        )    
        # Note how it uses `self.styles.animate` here instead of `self.animate`:
        self.static2.styles.animate(
            "opacity",
            0.0,
            duration=self.duration,
        )                    


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)