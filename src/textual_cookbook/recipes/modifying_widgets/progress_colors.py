"""This example demonstrates making a progress bar with different colors
for different states: indeterminate, complete, incomplete, and error.

Recipe by NSPC911  
https://github.com/NSPC911"""

import sys
from textual.app import App, ComposeResult
from textual.widgets import ProgressBar

class TextualApp(App[None]):
    CSS = """
    .bar {
      color: $warning
    }
    .bar--indeterminate {
      color: $accent
    }
    .bar--complete {
      color: $success;
    }
    .error .bar--complete,
    .error .bar--bar {
      color: $error;
    }
    """
    def compose(self) -> ComposeResult:
        yield ProgressBar(total=None, id="indeterminate")
        yield ProgressBar(total=100, id="complete", classes="complete")
        yield ProgressBar(total=100, id="incomplete", classes="incomplete")
        yield ProgressBar(total=100, id="error", classes="error complete")
        yield ProgressBar(total=100, id="incompleteerror", classes="error incomplete")
        
    def on_mount(self) -> None:
        for widget in self.query("ProgressBar.incomplete"):
            widget.update(progress=50)
        for widget in self.query("ProgressBar.complete"):
            widget.update(progress=100)
            


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)