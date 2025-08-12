"""This example demonstrates how to set up and read a dictionary on the app class
in order to share data between different components.

Recipe by Edward Jazzhands"""

import sys
from textual import on
from textual.app import App
from textual.widgets import Button
from textual.containers import Container

class MyContainer(Container):

    DEFAULT_CSS = """ MyContainer {border: panel $primary;} """

    def __init__(self, container_num:int):
        super().__init__()
        self.container_num = container_num
        self.border_title = f"MyContainer {container_num}"

    def compose(self):
        yield Button("Set app dict", id="button1")
        yield Button("Read app dict", id="button2")

    @on(Button.Pressed, "#button1")
    def button1(self):
        x = self.container_num
        my_dict = {
            f"key{x}": f"value{x}",
            f"key{x+1}": f"value{x+1}"
        }
        self.app.app_dict = my_dict          # type: ignore
        self.notify(f"App dict set by container {self.container_num}")

    @on(Button.Pressed, "#button2")
    def button2(self):
        self.notify(str(self.app.app_dict))  # type: ignore
        self.log(self.app.app_dict)          # type: ignore 


class TextualApp(App[None]):

    app_dict = {}

    def compose(self):
        yield MyContainer(1)
        yield MyContainer(3)


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)