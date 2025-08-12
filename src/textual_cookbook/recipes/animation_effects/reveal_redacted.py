"""This script demonstrates how you could set redacted text and then reveal
the text when hovered.
The RedactedText widget has a reveal_range reactive attribute which is updated
when some redacted text is hovered. This will prompt a "smart refresh" to update
which ranges have the 'redacted' styling.
The important part is the metadata (meta) applied to portions of the text.
The mouse event handler checks the event.style.meta and updates the reveal_range
reactive attribute accordingly.

Recipe by Tom J Gooding"""

# These two imports added by Edward Jazzhands:
from __future__ import annotations    # added for 3.9 compatibility
import sys                            # added to conform to the recipe format

from rich.text import Text
from textual import events
from textual.app import App, ComposeResult, RenderResult
from textual.reactive import reactive
from textual.widget import Widget


class RedactedText(Widget):
    COMPONENT_CLASSES = {"redacted"}

    DEFAULT_CSS = """
    RedactedText {
        width: auto;
        height: auto;

        .redacted {
            color: $foreground;
            background: $foreground;
        }
    }
    """

    reveal_range: reactive[tuple[int, int] | None] = reactive(None)

    def render(self) -> RenderResult:
        redacted_style = self.get_component_rich_style("redacted")

        redacted_text = Text("Hello world foo bar")
        redact_ranges = [(6, 11), (16, 19)]

        for redact_range in redact_ranges:
            start, end = redact_range
            # Add meta info - see the mouse handler below
            redacted_text.apply_meta({"redacted": redact_range}, start, end)

            if self.reveal_range != redact_range:
                # Add a redacted style to portions of the text
                redacted_text.stylize(redacted_style, start, end)

        return redacted_text

    def on_mouse_move(self, event: events.MouseMove) -> None:
        meta = event.style.meta
        if "redacted" in meta:
            self.reveal_range = meta["redacted"]
        else:
            self.reveal_range = None

    def on_leave(self) -> None:
        self.reveal_range = None


class TextualApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        yield RedactedText()


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)