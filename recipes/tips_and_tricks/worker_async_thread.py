"""This script demonstrates that it is possible for a thread worker to also
be an async function in Textual, and that Textual handles this by creating
a new event loop for the thread worker. This allows you to run async code
in a separate thread while still being able to interact with the main Textual
event loop and widgets.

Recipe by Edward Jazzhands

(THIS EXAMPLE IS ROUGH AND WORK IN PROGRESS)"""

from textual import work
from textual.app import App, ComposeResult
from textual.widgets import RichLog
import asyncio
from asyncio.events import AbstractEventLoop
import threading

class AsyncInThreadApp(App[None]):

    def compose(self) -> ComposeResult:
        yield RichLog()

    @work(thread=True, exit_on_error=False)
    async def my_threaded_worker(
        self, 
        main_loop: AbstractEventLoop,
        main_thread_id: int
    ) -> None:

        thread_id = threading.get_ident()
        thread_loop = asyncio.get_event_loop()  
        self.call_from_thread(
            self.update_log,
            f"Main thread ID: {main_thread_id} \n"
            f"Worker thread ID: {thread_id} \n"
            f"Same thread?: {thread_id == main_thread_id} \n"
            f"Same loop as main?: {thread_loop is main_loop}\n"
        )

    async def update_log(self, message: str) -> None:
        """Update the log widget with a message."""
        log_widget = self.query_one(RichLog)
        log_widget.write(message)

    async def on_mount(self) -> None:

        thread_id = threading.get_ident()
        loop = asyncio.get_event_loop()        
        try:
            await self.my_threaded_worker(loop, thread_id).wait()
        except Exception as e:
            self.notify(f"Failed: {e}")           


if __name__ == "__main__":
    AsyncInThreadApp().run()
