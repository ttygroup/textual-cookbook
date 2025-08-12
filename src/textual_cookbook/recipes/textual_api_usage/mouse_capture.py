"""
This example demonstrates how to capture mouse events in Textual applications 
in order to get clean mouse capture behavior. 
This shows two different ways to capture mouse events:
    1. Using `capture_mouse` and `release_mouse` methods.
    2. Using a flag to track if the click started on the widget.
The second method can be preferable in some cases, as it avoids the need to
explicitly capture and release the mouse.
You can also see that removing either of the `on_leave` event handlers
will result in the mouse not being released when the mouse leaves the widget,
and the mouse_up event will be triggered even if the mouse is not
still over the widget.

Recipe by Edward Jazzhands"""

import sys
from typing import Any
from textual.app import App
from textual import events
from textual.widgets import Static


class MyCapturer1(Static):

    def on_mouse_down(self, event: events.MouseDown) -> None:

        self.capture_mouse()
        self.add_class("pressed")

    def on_mouse_up(self, event: events.MouseUp) -> None:

        if self.app.mouse_captured == self:
            self.release_mouse()            
            self.remove_class("pressed")
            self.notify("Mouse released")

    def on_leave(self) -> None:

        self.release_mouse()
        self.remove_class("pressed")


class MyCapturer2(Static):

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.click_started_on = False

    def on_mouse_down(self, event: events.MouseDown) -> None:

        self.click_started_on = True
        self.add_class("pressed")

    def on_mouse_up(self) -> None:

        self.remove_class("pressed")
        if self.click_started_on:
            self.click_started_on = False
            self.notify("Mouse released")

    def on_leave(self) -> None:

        self.click_started_on = False
        self.remove_class("pressed")


class TextualApp(App[None]):

    CSS = """
    Screen { align: center middle; }
    #capture1 { border: solid blue; }
    #capture2 { border: solid red; }
    .capture { 
        width: auto;
        &.pressed { background: $success; }
    }
    """

    def compose(self):

        yield MyCapturer1("Capturer 1", id="capture1", classes="capture")
        yield MyCapturer2("Capturer 2", id="capture2", classes="capture")


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)