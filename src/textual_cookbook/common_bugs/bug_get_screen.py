"""This file demonstrates ?
Example by Edward Jazzhands, 2025"""

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Button
from textual.screen import Screen
from textual.message import Message

class MainScreen(Screen[None]):

    class EventFoo(Message):
        pass

    def compose(self) -> ComposeResult:
        yield Button("Press Me", id="main_button")

    def on_button_pressed(self) -> None:
        self.post_message(self.EventFoo())

class TuiApp(App[None]):

    SCREENS = {"main": MainScreen}

    def on_mount(self) -> None:
        self.push_screen("main")

    @on(MainScreen.EventFoo)
    def workfoo(self) -> None:

        main_screen = self.get_screen("main", MainScreen)
        main_screen.query_one("#main_button", Button).label = "Success"
        self.notify(f"EventFoo received from {main_screen}")


if __name__ == "__main__":
    app = TuiApp()
    app.run()