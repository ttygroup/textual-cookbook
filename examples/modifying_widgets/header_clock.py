"""This demonstrates how to change the timezone of the header clock in Textual.
This is performing a monkey patch.

Example by Edward Jazzhands, 2025"""

from zoneinfo import ZoneInfo
from datetime import datetime

from textual.app import App, RenderResult
from textual.widgets import  Footer, Header
from textual.widgets._header import HeaderClock
from rich.text import Text

def render(self) -> RenderResult:
    """Render the header clock.

    Returns:
        The rendered clock.
    """
    return Text(datetime.now(ZoneInfo("UTC")).time().strftime(self.time_format))

HeaderClock.render = render

class TextualApp(App[None]):
    
    def compose(self):

        yield Header(show_clock=True)
        yield Footer()

if __name__ == "__main__":
    TextualApp().run()