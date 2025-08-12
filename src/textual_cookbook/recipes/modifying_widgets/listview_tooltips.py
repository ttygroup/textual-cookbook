"""This example demonstrates how to create a ListView with tooltips for each item.

Recipe by Edward Jazzhands"""

import sys
from textual.app import App, ComposeResult
from textual.widgets import Footer, Label, ListItem, ListView


class TextualApp(App[None]):
    
    CSS = """
    Screen {align: center middle;}
    ListView { width: 30; height: auto; }
    Label { padding: 1 2; }
    """

    def compose(self) -> ComposeResult:

        with ListView():
            item1 = ListItem(Label("One"))
            item1.tooltip = "This is the first item"
            item2 = ListItem(Label("Two"))
            item2.tooltip = "This is the second item"
            item3 = ListItem(Label("Three"))
            item3.tooltip = "This is the third item"

            yield item1
            yield item2
            yield item3

        yield Footer()


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)