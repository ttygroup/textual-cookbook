"""This file demonstrates how to create a TabbedContent widget with
tabs that cannot be clicked or interacted with by the user.
They can only be changed programmatically, which is demonstrated
by pressing the "Enter" key to switch to the next tab.

Recipe by Edward Jazzhands"""

import sys
from textual.app import App, ComposeResult
from textual.widgets import Placeholder, Footer, TabbedContent, TabPane
from textual.containers import Container

class TextualApp(App[None]):    

    CSS = """
    Tabs {
        &:disabled {
            .underline--bar {
                background: $foreground 30%;
            }
            & .-active {
                color: $block-cursor-foreground;
                background: $block-cursor-background;
            }
        }
    }    
    """

    BINDINGS = [
        ("enter", "next_tab", "Next Tab"),
    ]

    current_tab = 1

    def compose(self) -> ComposeResult:
        with Container(id="main_container"):
            with TabbedContent() as TB:
                TB.disabled = True
                with TabPane("Tab 1", id="tab1"):
                    yield Placeholder("Placeholder for Tab 1")
                with TabPane("Tab 2", id="tab2"):
                    yield Placeholder("Placeholder for Tab 2")
                with TabPane("Tab 3", id="tab3"):
                    yield Placeholder("Placeholder for Tab 3")
        yield Footer()

    def action_next_tab(self) -> None:
        next_tab = (self.current_tab + 1) if self.current_tab < 3 else 1
        self.current_tab = next_tab
        self.query_one(TabbedContent).active = f"tab{next_tab}"


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)