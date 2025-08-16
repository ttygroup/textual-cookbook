"""This example demonstrates how the `push_screen_wait` method
(A wrapper around `push_screen` with the `wait_for_dismiss` argument
set to True) can be used to push a screen in the middle of a worker
that will cause the worker to temporarily pause what it is doing. This
is demonstrated in both a normal async worker and a threaded worker.

Recipe by NSPC911  
https://github.com/NSPC911"""

import sys
from typing import Any
import asyncio

from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Grid, Container
from textual.screen import ModalScreen
from textual.widgets import Button, Label, ProgressBar

class Dismissable(ModalScreen[None]):
    """Super simple screen that can be dismissed."""

    DEFAULT_CSS = """
    Dismissable {
        align: center middle
    }
    #dialog {
        grid-size: 1;
        grid-gutter: 1 2;
        grid-rows: 1fr 3;
        padding: 1 3;
        width: 50vw;
        max-height: 13;
        border: round $primary-lighten-3;
        column-span: 3
    }
    #message {
        height: 1fr;
        width: 1fr;
        content-align: center middle
    }
    Container {
        align: center middle
    }
    Button {
        width: 50%
    }
    """

    def __init__(self, message: str, **kwargs: Any):
        super().__init__(**kwargs)
        self.message = message

    def compose(self) -> ComposeResult:
        with Grid(id="dialog"):
            yield Label(self.message, id="message")
            with Container():
                yield Button("Ok", variant="primary", id="ok")

    def on_mount(self) -> None:
        self.query_one("#ok").focus()

    @on(Button.Pressed, "#ok")
    def on_button_pressed(self) -> None:
        """Handle button presses."""
        self.dismiss()


class TextualApp(App[None]):
    
    def compose(self) -> ComposeResult:
        yield Container()
        yield Button("test in normal worker", id="test")
        yield Button("test in threaded worker", id="test_threaded")
        
    @on(Button.Pressed, "#test")
    @work
    async def if_button_pressed(self, event: Button.Pressed) -> None:
        
        progress = ProgressBar(total=10)
        self.mount(progress)
        while progress.percentage != 1:
            progress.advance()
            await asyncio.sleep(0.5)
            if progress.percentage == 0.5:
                await self.push_screen_wait(Dismissable("hi"))
                
    @on(Button.Pressed, "#test_threaded")
    @work(thread=True)
    def if_button_pressed_thread(self) -> None:
        
        progress = ProgressBar(total=10)
        self.call_from_thread(self.mount, progress)
        while progress.percentage != 1:
            self.call_from_thread(progress.advance)
            self.call_from_thread(asyncio.sleep, 0.5)
            if progress.percentage == 0.5:
                self.call_from_thread(self.push_screen_wait, Dismissable("hi"))


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)