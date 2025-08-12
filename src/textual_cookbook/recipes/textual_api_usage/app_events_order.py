"""This script demonstrates what order that events are fired in Textual.

Recipe by Edward Jazzhands"""

import sys
from textual.app import App
from textual.widgets import Footer
class TextualApp(App):

    def counter(self) -> int:
        self._counter += 1
        return self._counter      

    def __init__(self):         # This is the very first thing to run.
        super().__init__()
        self.foo = "foo"
        self._counter = 0
        self.log("This log statement won't work. The logger isn't set up yet")

    def on_load(self, event):
        self.log(f"on_load: {self.counter()} | foo: {self.foo}")

    def compose(self):
        self.log(f"compose: {self.counter()})")          #2

        yield Footer()

    def on_resize(self, event):
        self.log(f"on_resize: {self.counter()})")     #3 and 5 

    def on_mount(self, event):
        self.log(f"on_mount: {self.counter()})")      #4

    def on_ready(self, event):
        self.log(f"on_ready: {self.counter()})")      #6


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)