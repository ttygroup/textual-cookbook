"""This file demonstrates how to create a Textual application
with a transparent background which can be toggled on and off.

Recipe by Edward Jazzhands"""

import sys
from textual import on
from textual.app import App
from textual.screen import Screen
from textual.widgets import Static, Footer, Button
from textual.containers import Container


class DummyScreen(Screen[None]):
    
    def on_mount(self) -> None:
        self.dismiss()


class TextualApp(App[None]):

    CSS = """
    Screen { align: center middle; }
    #my_static { border: solid blue; width: auto;}
    #main_container { width: 50%; height: 50%; border: solid red;
        align: center middle; }
    """

    def compose(self):

        with Container(id="main_container"):
            yield Static("Hello, Textual", id="my_static")
            yield Button("Toggle Transparency", id="toggle_transparency")

        yield Footer()

    @on(Button.Pressed, "#toggle_transparency")
    def toggle_transparency(self) -> None:

        self.ansi_color = not self.ansi_color
        self.push_screen(DummyScreen())


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)