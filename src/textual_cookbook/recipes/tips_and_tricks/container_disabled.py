"""This script demonstrates how you can utilize the `disabled` state of a container
to make all of its widgets and contets greyed out and unresponsive.
A container greys out all of its children when it is disabled. This can be useful
for making sections of your UI that can be temporarily disabled. You can select
a container with your mouse and press 'd' to disable it.

Recipe by Edward Jazzhands"""

import sys
from textual.app import App
from textual.widgets import Static, Footer, Button, Checkbox, Input
from textual.containers import Container


class SpecialContainer(Container):

    BINDINGS = [("d", "select", "Disable this container")]

    def compose(self):
        self.can_focus = True
        yield Static("Hello, Textual! great day eh")
        yield Button("A Button")
        yield Checkbox("A Checkbox")
        yield Input(placeholder="An Input")

    def action_select(self):
        self.notify(f"Disabled {self.id}")
        self.disabled = True


class TextualApp(App[None]):

    DEFAULT_CSS = """
    #main_container { 
        align: center middle;
        layout: grid;
        grid-size: 3 2;
    }
    .inner-container {
        border: solid $primary;
        &:focus { border: solid $accent; }
    }
    """
    
    def compose(self):

        with Container(id="main_container"):
            for i in range(6):
                yield SpecialContainer(id=f"container_{i}", classes="inner-container")
        yield Footer()


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)