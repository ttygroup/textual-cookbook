"""This file demonstrates how to use the rich traceback feature
in a Textual application to log errors to a file and display them
in HTML format. The application includes a button that, when pressed,
will intentionally cause an error, triggering the logging mechanism.

Recipe by Edward Jazzhands"""

import sys
from datetime import datetime
from textual.app import App
from textual.widgets import Static, Button
from textual.containers import Container  
from rich.console import Console
from rich.traceback import Traceback


class TextualApp(App[None]):

    CSS = """
    Screen { align: center middle; }
    #my_static { border: solid blue; width: auto;}
    """

    def compose(self):

        with Container(id="my_container"):
            yield Static("Hello, Textual!", id="my_static")
            yield Button("Press me to cause a bug", classes="some-tcss-class")

    def on_button_pressed(self):
        self.query_one("#non_existent_widget")  # This will raise an error

    def _handle_exception(self, error: Exception) -> None:

        self.record_log_files(error)
        super()._handle_exception(error)


    def record_log_files(self, e: Exception):

        with open("error.txt", "w") as log_txt_file:
            console = Console(file=log_txt_file, record=True, width=100)
            console.print(f"TextualDon Error Report: {datetime.now()}\n")
            traceback = Traceback.from_exception(
                type(e),
                e,
                e.__traceback__,
                show_locals=True
            )
            console.print(traceback)            
            console.save_html("error.html")


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)