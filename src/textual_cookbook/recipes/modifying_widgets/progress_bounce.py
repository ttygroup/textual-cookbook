"""This example demonstrates a progress bar with a cool bouncing
animation effect.

Recipe by David Fokkema
https://github.com/davidfokkema"""

import sys
import time

from textual.app import App, ComposeResult
from textual.widgets import ProgressBar


class ElapsedTimeProgressBar(ProgressBar):
    _start_time: float = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._start_time = time.monotonic()

    def update(self, *args, **kwargs) -> None:
        super().update(*args, **kwargs)
        if self.total is None:
            self._display_eta = int(time.monotonic() - self._start_time)


class TextualApp(App[None]):
    def compose(self) -> ComposeResult:
        yield ElapsedTimeProgressBar()
        yield ProgressBar()

    def on_mount(self) -> None:
        self.progress_timer = self.set_interval(1 / 10, self.make_progress, pause=True)
        self.set_timer(5.0, self.start_progress)

    def start_progress(self) -> None:
        for bar in self.query(ProgressBar):
            bar.update(total=100)
        self.progress_timer.resume()

    def make_progress(self) -> None:
        for bar in self.query(ProgressBar):
            bar.advance(1)


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)