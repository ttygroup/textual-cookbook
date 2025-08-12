"""This file demonstrates how to use on_click to get the widget
that was clicked within a Container in Textual.

Recipe by Edward Jazzhands"""

import sys
from textual.containers import Container
from textual.widgets import Static
from textual.app import App
from textual import events

class PopularContainer(Container):

    def on_click(self, event: events.Click) -> None:

        self.notify(f"card: {self.id}")
        # card = event.control      # <-- this would also work.
        # if card:
        #     self.notify(f"card: {card.id}")

class TextualApp(App[None]):

    DEFAULT_CSS = """
    Screen { align: center middle; }
    #my_container { border: solid blue; width: 50%; height: 50%;}
    #popular_container { border: solid red; width: 50%;}
    """

    def compose(self):

        with Container(id="my_container"):
            with PopularContainer(id="popular_container"):
                yield Static("Hello, Textual!", id="my_static")


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)