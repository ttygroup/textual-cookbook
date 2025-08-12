"""This script demonstrates how to replace a widget's default "loading"
animation with a custom spinner widget in Textual.
The Spinner is using the rich.spinner module. You can replace the loading
animation with any Textual widget. The SpinnerWidget is only one example.

Recipe by Edward Jazzhands"""


from __future__ import annotations
import sys
import asyncio
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
	from rich.console import RenderableType

from textual.app import App, ComposeResult
from rich.spinner import Spinner
from textual.widget import Widget
from textual.widgets import Button, Static

class SpinnerWidget(Static):

	DEFAULT_CSS = """
	SpinnerWidget {
		content-align: center middle;
		width: 1fr; height: 1fr;
	}
	"""

	def __init__(self, spinner: str, text: RenderableType = "", *args: Any, **kwargs: Any):

		super().__init__(*args, **kwargs)
		self._spinner = Spinner(spinner, text)  

	def on_mount(self) -> None:
		self.update_render = self.set_interval(1 / 60, self.update_spinner)

	def update_spinner(self) -> None:
		self.update(self._spinner)


class CustomLoadingWidget(Static):

	def render(self):
		return "This is the normal / finished state."	

	def get_loading_widget(self) -> Widget:
		return SpinnerWidget("bouncingBall", "Loading...")	
		
	async def loading_progress(self):
		
		self.loading = True
		for _ in range(4):
			await asyncio.sleep(0.75)
		self.loading = False


class TextualApp(App[None]):

	CSS = """
	Screen { align: center middle; }
	CustomLoadingWidget {
		border: solid red;
		width: 50%; height: 5;
		content-align: center middle;
	}
	"""
	
	def compose(self) -> ComposeResult:
		yield CustomLoadingWidget()
		yield Button("Start", id="start_button")

	async def on_button_pressed(self):
		my_widget = self.query_one(CustomLoadingWidget)
		await my_widget.loading_progress()		



if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)