"""This script demonstrates how a widget can be initialized with a loading state
and then updated after a delay (simulating the time taken to boot up the app).

Recipe by Edward Jazzhands"""

import sys
from textual.app import App
from textual.widgets import Static, Footer
from textual.containers import Container

class TextualApp(App[None]):

    DEFAULT_CSS = """
    #my_container { align: center middle; }
    #my_static { width: 40; height: 15; border: solid $primary; }
    """
    
    def compose(self):

        self.my_static = Static("Hello, Textual! great day eh", id="my_static")
        self.my_static.loading = True
        with Container(id="my_container"):
            yield self.my_static
        yield Footer()

    def on_ready(self):
        self.set_timer(2, self.finished_loading)

    def finished_loading(self):
        self.my_static.loading = False


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)