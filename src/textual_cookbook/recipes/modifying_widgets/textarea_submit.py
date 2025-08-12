"""This shows how to add a Submitted action to a TextArea widget which
replicates the Submitted messge in the Input widget, and which can
be triggered by pressing a key or combo (ctrl+s in this case).

Recipe by Edward Jazzhands"""

from __future__ import annotations
import sys
from textual import on
from textual.app import App
from textual.message import Message
from textual.binding import Binding
from textual.widgets import TextArea, Footer

class MyTextArea(TextArea):

    class Submitted(Message):
        def __init__(self, textarea: MyTextArea, text: str):
            super().__init__()
            self.textarea = textarea  
            self.text = text
    
    BINDINGS = [
        Binding("ctrl+s", "submit", "Submit", show=True),
    ]
    
    def action_submit(self):
        self.post_message(self.Submitted(self, self.text))



class TextualApp(App[None]):

    CSS = """
    Screen { align: center middle; }
    MyTextArea { border: solid blue; width: 50%; height: 50%; }
    """

    def compose(self):
        yield MyTextArea()
        yield Footer()
    
    @on(MyTextArea.Submitted)
    def my_textarea_submitted(self, event: MyTextArea.Submitted):
        self.notify(f"TextArea submitted with text: {event.text}")
        # handle submit here


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)