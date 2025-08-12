"""This example demonstrates basic usage of colored text in a Static widget

Recipe by Edward Jazzhands"""

import sys
from textual.app import App
from textual.widgets import Static

class TextualApp(App[None]):

    CSS = """
    Screen { align: center middle; }
    #my_static {
        background: $surface;
        content-align: center middle;
        width: auto; height: 3;
        padding: 1;
    }
    """
    
    def compose(self):
        yield Static("[yellow]This[/yellow] is my [red]Static[/red]", id="my_static")
        # Note that Static has a `markup` argument which is True by default.


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)