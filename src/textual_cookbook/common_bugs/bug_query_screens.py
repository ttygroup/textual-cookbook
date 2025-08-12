"""This script demonstrates how you cannot query for screens directly using `query_one` or \
`query_all`. Instead, you should use the `get_screen` method to retrieve the screen instance. \
Attempting to query for the screen as shown below will cause the app to crash. \
Also note that the `get_default_screen` method is not needed if you are using \
`push_screen` to intialize with an installed screen (in SCREENS). This can cause issues \
because the default MainScreen instance will not be the same as the \
sinstalled screen in the app's screen stack.\

Example by Edward Jazzhands, 2025"""

from textual.app import App, ComposeResult
from textual.widgets import Static, Button
from textual.screen import Screen

class MainScreen(Screen[None]):

    def compose(self) -> ComposeResult:
        yield Static("Main Screen Content", id="main_static")
        yield Button("Press Me", id="main_button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.on_path_entered()

class TuiApp(App[None]):

    SCREENS = {"main": MainScreen}

    # def get_default_screen(self):    # This will cause problems. It is not needed.
    #     return MainScreen()          # if you use this instead of the push_screen method, you will see
    #                                  # that main_screen is not the same as self.screen.
    def on_mount(self) -> None:

        self.push_screen("main")
        self.log(self.screen_stack)

    def on_path_entered(self) -> None:

        # main_screen = self.query_one(MainScreen)     # this will not work. 

        main_screen = self.get_screen("main")    # <-- Do this instead
        self.notify(f"{main_screen is self.screen}")   # This shows that main_screen is the same as self.screen 

        main_screen.query_one("#main_static", Static).update("Path Entered!")


if __name__ == "__main__":
    app = TuiApp()
    app.run()