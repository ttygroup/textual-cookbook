"""This example demonstrates the "Data Widget" architecture pattern.
This involves creating a dedicated widget to hold any kind
of data or non-Textual class instances you want to share
across your app.

The DataWidget is invisible (display = False) and does not
render anything. But by making it an invisible widget mounted
to the App class, it can be queried from anywhere in
your app.


Recipe by Edward Jazzhands"""

from typing import Any
from textual.app import App
from textual.widget import Widget
from textual.widgets import Button, Static

# imagine this in some non-textual library
class MyNonTextualClass:
    def __init__(self):
        self.data = "Hello from MyNonTextualClass"

# Create a file called datawidget.py so it can be imported
# anywhere in your textual app
class DataWidget(Widget):

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.display = False 
        self.my_non_textual_class = MyNonTextualClass()

# import the data widget into your main app file:
# from mypackage.datawidget import DataWidget

# This simulates some other part of your app
# in a different module that wants to access the data
class MyOtherWidget(Widget):
    
    def compose(self):
        yield Button("Click to read DataWidget data")
        yield Static(id="output")
    
    def on_button_pressed(self):
        data_widget = self.app.query_one("#data_widget", DataWidget)
        data = data_widget.my_non_textual_class.data
        self.query_one("#output", Static).update(data)
        
        # TIP: You could also query by only the id to avoid
        # circular import problems if necessary for some reason

class TextualApp(App[None]):

    def compose(self):
        yield DataWidget(id="data_widget")
        yield MyOtherWidget()
    

if __name__ == "__main__":
    app = TextualApp()
    app.run()