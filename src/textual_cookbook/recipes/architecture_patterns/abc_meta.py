"""This script demonstrates how to create a Textual widget that is also
an abstract base class (ABC) using a metaclass that combines
the functionality of both `Widget` and `ABC`. This allows you to define
abstract methods that must be implemented by any subclass of the widget.
Note that I would not recommend doing this in general. It causes too
many issues with the Textual framework, such as preventing workers
from functioning correctly, and it can lead to unexpected behavior.
But its useful to keep this example up just as a demonstration of
how one would do it.

Recipe by Edward Jazzhands"""

import sys
from abc import ABC, abstractmethod
from textual.widget import Widget
from textual.app import App, ComposeResult


class ABCWidgetMeta(type(Widget), type(ABC)):
    pass


class AbstractDataWidget(Widget, ABC, metaclass=ABCWidgetMeta):
    
    @abstractmethod
    def load_data(self) -> None:
        pass
    
    def on_mount(self) -> None:
        self.load_data()


class UserListWidget(AbstractDataWidget):
    "Widget inheriting from AbstractDataWidget"
    
    # comment this method out to see the ABC error
    def load_data(self) -> None:
        self.notify("Data loaded from source")


class TextualApp(App[None]):

    def compose(self) -> ComposeResult:
        yield UserListWidget()


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)