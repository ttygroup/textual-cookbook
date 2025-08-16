"""This file demonstrates how the `exclusive` parameter of the `work`
decorator can only be used to cancel/debounce workers that are normal
async workers (non-threaded). The normal worker will be restarted
each time the button is pressed and effectively cancel the currently
running worker. But threaded workers will not be cancelled
and will run to completion, even if the button is pressed multiple
times (This is a limitation of threading in Python and not because of Textual).

Recipe by NSPC911  
https://github.com/NSPC911"""


from asyncio import sleep

import sys
from textual import work, on
from textual.app import App, ComposeResult
from textual.widgets import Button, RichLog
from textual.containers import HorizontalGroup

class TextualApp(App[None]):
    def compose(self) -> ComposeResult:
        self.richlog = RichLog()
        yield self.richlog
        with HorizontalGroup():
            yield Button("Run worker", id="worker")
            yield Button("Run worker THREAD", id="thread")

    def on_button_pressed(self, event:Button.Pressed):
        self.richlog.write(event.button.id)

    @on(Button.Pressed, "#worker")
    @work(exclusive=True, thread=False)
    async def worker_runner(self, event:Button.Pressed):
        await sleep(1) # simulate process intensive thing
        self.richlog.write("Worker completed!")

    @on(Button.Pressed, "#thread")
    @work(exclusive=True, thread=True)
    def thread_runner(self, event:Button.Pressed):
        self.call_from_thread(sleep, 1)
        self.richlog.write("Thread completed!")


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)