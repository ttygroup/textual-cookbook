"""This script demonstrates how widgets do not have a `CSS` class attribute.
It is fairly common to assume that they do, but they do not.
The code below will not work as expected.
Widgets must use the `DEFAULT_CSS` class attribute instead.

Example by Edward Jazzhands, 2025"""

from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Header, Static

class MyContainer(Widget):

    CSS = """     # Widget.CSS does not exist, use DEFAULT_CSS instead
    #porque {
        border: round red;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static("Hello World", id="porque")


class BorderTestApp(App):
    CSS = """
    MyContainer {
        border: round blue;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield MyContainer()


if __name__ == "__main__":
    app = BorderTestApp()
    app.run()