"""This file demonstrates how to animate a single widget's offset
using Textual's animation capabilities. The widget will move horizontally
when the button is pressed, and the animation will last for 1 second.

Recipe by Edward Jazzhands"""

import sys
from textual.app import App, ComposeResult
from textual.widgets import Static, Button
from textual.geometry import Offset

class TextualApp(App[None]):
    
    def compose(self) -> ComposeResult:
        yield Button("Animate Offset", id="animate_button")        
        self.box = Static("Hello, World!")
        yield self.box

    def on_button_pressed(self) -> None:
        self.box.animate("offset", value=Offset(20, 0), duration=1.0)


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)