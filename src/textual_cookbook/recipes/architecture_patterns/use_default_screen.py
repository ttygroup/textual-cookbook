"""An example showing how to use a default main screen.

Simple Textual apps place a lot of logic in the `App` class, but you can also
use a `Screen` as the main screen. This example shows how to do that, and how to
push modal screens from the main screen, and show a modal confirmation screen
when quitting the app. You'll never leave the main screen until you quit the
application, but you can still use the `App` class to manage a (few)
application-wide bindings.

Recipe by David Fokkema
"""

import sys

from textual import on
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.screen import ModalScreen, Screen
from textual.widgets import Button, Footer, Label


class HelpModal(ModalScreen[None]):
    BINDINGS = [("escape", "dismiss", "Dismiss")]

    def compose(self) -> ComposeResult:
        yield Footer()
        yield Label("Just your regular help screen, dismiss with escape")


class MainScreen(Screen[None]):
    BINDINGS = [
        ("a", "add_item", "Add Item"),
        ("r", "remove_item", "Remove Item"),
        ("h", "show_help", "Help"),
    ]

    items: list[str] = []

    def compose(self) -> ComposeResult:
        yield Footer()
        yield Label()

    def on_mount(self) -> None:
        self.update_label()

    def action_add_item(self) -> None:
        self.items.append("💡")
        self.update_label()

    def action_remove_item(self) -> None:
        if self.items:
            self.items.pop()
            self.update_label()

    def update_label(self) -> None:
        widget = self.query_one(Label)
        if self.items:
            widget.update("".join(self.items))
        else:
            widget.update("Empty")

    def action_show_help(self) -> None:
        self.app.push_screen(HelpModal())


class ConfirmQuitScreen(ModalScreen[bool]):
    BINDINGS = [("escape", "dismiss", "Dismiss")]

    def compose(self) -> ComposeResult:
        yield Footer()
        with VerticalGroup():
            yield Label("Are you sure you want to quit?")
            yield HorizontalGroup(
                Button("Yes", id="yes_button", variant="success"),
                Button("No", id="no_button", variant="error"),
            )

    @on(Button.Pressed)
    def confirm(self, event: Button.Pressed) -> None:
        if event.button.id == "yes_button":
            self.dismiss(True)
        else:
            self.dismiss(False)


class MainApp(App[None]):
    BINDINGS = [("q", "confirm_quit", "Quit")]

    CSS = """
        MainScreen Label {
            width: 100%;
            text-align: center;
            padding-top: 5;
        }

        HelpModal {
            align: center middle;
            & Label {
                border: $primary hkey;
                background: $panel;
                padding: 1 2;
                margin-top: 3;
            }
        }

        ConfirmQuitScreen {
            align: center middle;
            & VerticalGroup {
                width: auto;

                & Label {
                    width: 100%;
                    text-align: center;
                }

                & HorizontalGroup {
                    width: auto;

                    & Button {
                        margin: 1 2;
                    }
                }
            }
        }
    """

    def get_default_screen(self) -> Screen[None]:
        return MainScreen()

    def action_confirm_quit(self) -> None:
        def callback(is_confirmed: bool | None) -> None:
            if is_confirmed:
                self.exit()

        self.push_screen(ConfirmQuitScreen(), callback=callback)


if __name__ == "__main__":
    app = MainApp()
    app.run()
    sys.exit(app.return_code)
