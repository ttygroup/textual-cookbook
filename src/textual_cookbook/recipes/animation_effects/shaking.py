"""This file demonstrates how to createa a "shaking" effect on a button.

Recipe by NSPC911"""


import sys
from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Button

from asyncio import sleep

class TextualApp(App[None]):
    CSS = """
    Button {
        margin-left: 10
    }
    """
    def compose(self) -> ComposeResult:
        yield Button("Shake me!")
    @work
    async def on_button_pressed(self, event: Button.Pressed):
        self.query_one(Button).styles.margin = (0,0,0,11)
        await sleep(0.1)
        self.query_one(Button).styles.margin = (0,0,0,10)
        await sleep(0.1)
        self.query_one(Button).styles.margin = (0,0,0,11)
        await sleep(0.1)
        self.query_one(Button).styles.margin = (0,0,0,10)



if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)