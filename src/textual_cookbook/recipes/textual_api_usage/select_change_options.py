"""This script demonstrates how to change the options of a Select widget in real-time.

Recipe by Edward Jazzhands"""

import sys
from textual.app import App
from textual.widgets import Select, Button
from textual.containers import Container

class TextualApp(App[None]):

    DEFAULT_CSS = """
    #my_container { width: 1fr; height: 1fr; align: center middle; }
    """

    my_list = [
        ("Option 1", "1"),
        ("Option 2", "2"),
        ("Option 3", "3"),
        ("Option 4", "4"),
        ("Option 5", "5"),
    ]
    my_list2 = [
        ("Option 6", "6"),
        ("Option 7", "7"),
        ("Option 8", "8"),
        ("Option 9", "9"),
        ("Option 10", "10"),
    ]
    
    def compose(self):

        with Container(id="my_container"):
            self.my_select = Select(self.my_list)
            yield self.my_select
            yield Button("Change list")

    def on_button_pressed(self, event: Button.Pressed):
        self.my_select.set_options(self.my_list2)


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)