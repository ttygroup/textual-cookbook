"""This file demonstrates how to add the `control` method in a Textual message
to allow it to be specified in CSS selectors (query, @on, etc.).

Recipe by Edward Jazzhands"""


from __future__ import annotations
import sys
from textual import on
from textual.app import App
from textual.widgets import Static, Footer, Button
from textual.containers import Container
from textual.message import Message


class MyStatic(Static):

    class MessageFoo(Message):

        def __init__(self, sender: MyStatic):
            super().__init__()
            self.sender: MyStatic = sender

        @property
        def control(self) -> MyStatic:
            return self.sender

    def send_foo(self):
        self.post_message(self.MessageFoo(self))


class TextualApp(App[None]):

    DEFAULT_CSS = """
    Screen { align: center middle; }
    #my_static { border: solid blue; width: auto;}
    """

    def compose(self):

        with Container(id="my_container"):
            yield MyStatic("Hello, Textual!", id="my_static")
            yield Button("press me", id="my_button")

        yield Footer()

    def on_button_pressed(self):
        my_static = self.query_one(MyStatic)
        my_static.send_foo()

    @on(MyStatic.MessageFoo, "#my_static")
    def recieve_foo(self, message: MyStatic.MessageFoo):
        self.notify(f"Received MessageFoo from {message.sender}!")


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)