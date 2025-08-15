"""This file demonstrates how to create animating pop-up
context menus. The menu will pop up whereever you click
on the static banner in the center.
The context menu itself is actually on a Modal Screen. This
allows us to close it by clicking anywhere.

Recipe by Edward Jazzhands"""

# Python imports
from __future__ import annotations
from typing import TYPE_CHECKING
import sys

if TYPE_CHECKING:
    from textual.app import ComposeResult

# Textual and rich imports
from textual import work
from textual.app import App, ComposeResult
from textual.geometry import Offset
from textual.screen import ModalScreen
from textual.containers import Container
from textual import events
from textual.widgets import Static, Button


class ContextMenu(ModalScreen[None]):
    
    BINDINGS = [
        ("up", "app.focus_previous"),
        ("down", "app.focus_next"),
    ]

    CSS = """
    ContextMenu {
        background: $background 0%;
        align: left top;    /* This will set the starting coordinates to (0, 0) */
    }                       /* Which we need for the absolute offset to work */
    #menu_container {
        background: $surface;
        width: 10;
        border-left: wide $panel;
        border-right: wide $panel;        
        &.bottom { border-top: hkey $panel; }
        &.top { border-bottom: hkey $panel; }
        & > Button {
            min-width: 8;
            &:hover { background: $panel-lighten-2; }
            &:focus {
                background: $panel-lighten-2; 
                text-style: none;
            }
        }
    }
    """

    def __init__(self, menu_offset: Offset) -> None:
        super().__init__()
        self.menu_offset = menu_offset

    def compose(self) -> ComposeResult:

        with Container(id="menu_container"):
            yield Button("Menu 1", id="menu1", compact=True)
            yield Button("Menu 2", id="menu2", compact=True)
            yield Button("Menu 3", id="menu3", compact=True)
            yield Button("Menu 4", id="menu4", compact=True)

    def on_mount(self) -> None:

        menu = self.query_one("#menu_container")
        # automatically set the height to the number of buttons:
        height = len(menu.children)
        menu.styles.height = height
        
        # Subtracting the menu's height will make it appear above
        # the mouse instead of below it
        y_offset = self.menu_offset.y - height
        menu.offset = Offset(self.menu_offset.x, y_offset)

    def on_mouse_up(self) -> None:

        # This allows us to close it by clicking anywhere
        self.dismiss(None)

    async def on_button_pressed(self, event: Button.Pressed) -> None:

        if event.button.id == "menu1":
            self.notify("Menu 1")
        elif event.button.id == "menu2":
            self.notify("Menu 2")
        elif event.button.id == "menu3":
            self.notify("Menu 3")
        elif event.button.id == "menu4":
            self.notify("Menu 4")
            
        self.dismiss()

class MyStatic(Static):
    
    @work
    async def on_click(self, event: events.Click) -> None:
        menu_offset = event.screen_offset
        await self.app.push_screen_wait(
            ContextMenu(menu_offset=menu_offset)
        )

class TextualApp(App[None]):

    CSS = """
    #my_container { 
        align: center middle; 
        border: solid red;
    }
    MyStatic { 
        border: hkey blue;
        width: auto;
        &:hover { background: $boost; }
    }
    """

    def compose(self):

        with Container(id="my_container"):
            yield MyStatic(
                "Click on me anywhere. "
                "Notice how the menu pops up where you click. \n"
                "You can also navigate the menu with up/down keys or tab.",
                id="main_button"
            )
             

if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)