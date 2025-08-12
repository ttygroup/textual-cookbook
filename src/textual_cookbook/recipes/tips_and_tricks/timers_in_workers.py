"""This script demonstrates setting timers inside of workers.
A timer schedules a job to run on the event loop, and is independent
of the worker that created it. This demonstrates how in both cases
the timer callback runs after the worker has completed, as well as
how the thread worker must use call_from_thread to schedule timers.

Recipe by Edward Jazzhands
"""
from __future__ import annotations
import sys
import asyncio
import time
from typing import cast
from functools import partial

from textual import work, on
from textual.worker import Worker, get_current_worker  # type: ignore  ("Partially Unknown")
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import RichLog, Button


class TextualApp(App[None]):

    CSS = """
    Screen { align: center middle; }
    #log_container {
        width: 70%;
        min-width: 60;
        height: 90%;
        RichLog { border: heavy $primary; }
    }
    .buttonrow { 
        height: auto;
        Button { margin: 0 2; }
    }
    """

    def compose(self) -> ComposeResult:

        with Vertical(id="log_container"):
            with RichLog(id="log1", markup=True) as rlog:
                rlog.border_title = "Non-Threaded Worker Log"
                rlog.can_focus = False
            with Horizontal(classes="buttonrow"):
                yield Button("Start normal worker ", id="start_normal_worker")
                yield Button("Start thread worker", id="start_thread_worker")
                

    def update_log(self, message: str) -> None:

        log_widget = self.query_one(RichLog)
        log_widget.write(message)

    async def on_button_pressed(self, event: Button.Pressed) -> None:

        if event.button.id == "start_normal_worker":
            self.normal_worker()
        elif event.button.id == "start_thread_worker":
            self.threaded_worker()

    def worker_timer(self, set_by_worker: Worker[None], log_num: int) -> None:

        self.update_log(
            "[yellow]Timer callback[/yellow]: \n"
            f"[red]Set by[/red]: {set_by_worker.name} \n"
            f"[red]State[/red]: {set_by_worker.state} \n"
            f"[red]Is finished?[/red]: {set_by_worker.is_finished} \n"
        )

    @work
    async def normal_worker(self) -> None:

        current_worker = cast(Worker[None], get_current_worker())
        self.set_timer(2, partial(self.worker_timer, current_worker, 1))
        await asyncio.sleep(1)

    @work(thread=True)
    def threaded_worker(self) -> None:

        current_worker = cast(Worker[None], get_current_worker())

        # Threaded workers must use call_from_thread to schedule timers.
        # Calling set_timer by itself would raise an error.
        self.app.call_from_thread(
            self.set_timer,
            2, partial(self.worker_timer, current_worker, 2)
        )
        time.sleep(1)

    @on(Worker.StateChanged)
    def _worker_state_changed(self, event: Worker.StateChanged) -> None:

        worker = event.worker   # type: ignore  ("Unknown worker type")
        self.update_log(f"{worker.name} is {worker.state}")


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)