"""This file is a fairly complex example that shows off how Textual Screens
are handled by the App class and the DOM. It has 3 screens, which
all inherit from MyScreenType just to reduce code duplication (They are
all identical except for the text they display).
The main screen has a RichLog widget that displays debug information
when the user presses the "Print Debug" button (or the 'p' key).
The screens are transparent Modal screens and they also have a button to
print the debug information to the RichLog. You can see the info
being printed to the RichLog on the main screen below (although the Modal
Screen is the active screen on top).
You will see that for the `self.children` attribute on the App class,
there will only ever be one child, which is the currently active screen.
The docstring for `self.children` says this:

  > A view onto the app's immediate children.
  > This attribute exists on all widgets. In the case of the App, it will only ever
  > contain a single child, which will be the currently active screen.

You can see that when using the `self.query_children()` method, the currently
active screen will NOT be included in the results, even though it is technically
the only child of the App class (as shown by `self.children`).
Textual (I believe) automatically makes queries on the main App class
start the query on the currently active screen, as opposed to including it
in the query results.

Recipe by Edward Jazzhands"""


import sys
from textual import on
from textual.app import App, ComposeResult
from textual.screen import ModalScreen
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.widgets import Static, Button, Footer, RichLog


class MyScreenType(ModalScreen[None]):

    def compose(self) -> ComposeResult:
        with Container(classes="screen_container"):
            yield Button("Print Debug", id="print_debug_button")
            yield Button("Close", id="close_button")
        yield Footer()

    @on(Button.Pressed, "#close_button")
    def close_button(self) -> None:
        self.dismiss()

    @on(Button.Pressed, "#print_debug_button")
    async def print_debug(self) -> None:
        await self.app.run_action("print_debug")
        

class ScreenOne(MyScreenType):

    def on_mount(self) -> None:
        self.query_one(Container).mount(
            Static("This is Screen One", classes="statics"), before=0
        )

class ScreenTwo(MyScreenType):

    def on_mount(self) -> None:
        self.query_one(Container).mount(
            Static("This is Screen Two", classes="statics"), before=0
        )


class ScreenThree(MyScreenType):

    def on_mount(self) -> None:
        self.query_one(Container).mount(
            Static("This is Screen Three", classes="statics"), before=0
        )

class TextualApp(App[None]):

    CSS = """
    ModalScreen { 
        align: center middle; 
        background: $background 30%;  /* extra transparent for demo */
    }
    .statics { padding: 1; }
    .left_container { align: center middle; width: 30; }
    .screen_container { border: solid $primary; width: auto; height: auto;}
    """

    BINDINGS = [
        Binding("up", "select('up')", description="Selection up", priority=True),
        Binding("down", "select('down')", description="Selection down", priority=True),
        Binding("p", "print_debug", description="Print debug information"),
    ]    

    # Screens here count as installed screens
    SCREENS = {
        "screen_one": ScreenOne,
        "screen_two": ScreenTwo,
        "screen_three": ScreenThree,
    }

    def compose(self) -> ComposeResult:

        with Horizontal():
            with Container(classes="left_container"):
                yield Button("Go to Screen One", id="screen_one_button", classes="main_button")
                yield Button("Go to Screen Two", id="screen_two_button", classes="main_button")
                yield Button("Go to Screen Three", id="screen_three_button", classes="main_button")
                yield Button("Print Debug", id="print_debug_button", classes="main_button")
            with Container(classes="right_container"):
                richlog = RichLog()
                richlog.can_focus = False
                yield richlog
        yield Footer()

    @on(Button.Pressed, ".main_button")
    def main_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "print_debug_button":
            self.action_print_debug()
            return
        if button_id is not None:
            screen_name = button_id.replace("_button", "")
            self.query_one(RichLog).write(f"Opening screen: {screen_name}")
            self.push_screen(screen_name)

    def action_select(self, direction: str) -> None:
        """Handle up and down selection."""
        if direction == "up":
            self.action_focus_previous()
        else: 
            assert direction == "down"
            self.action_focus_next()

    def action_print_debug(self) -> None:
        """Print debug information to the RichLog."""
        log = self.query_one(RichLog)
        log.write("Debug Information:")
        log.write(f"Current Screen: {self.screen}")
        log.write(f"Screen Stack: {self.screen_stack}")
        log.write(f"Direct children of App: {self.children}")
        my_query = self.query_children().results()
        for item in my_query:
            log.write(f"Query Result: {item} (Type: {type(item)})")


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)