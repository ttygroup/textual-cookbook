"""This file demonstrates an improved optionlist, where you can search for the available\
options and select them accordingly. The options are from \
`Starlight (Keep Me Afloat) - Martin Garrix` <3

Recipe by NSPC911
https://github.com/NSPC911"""

import sys

from textual import events
from textual.app import App, ComposeResult
from textual.containers import VerticalGroup
from textual.screen import ModalScreen
from textual.widgets import Button, Input, OptionList
from textual.widgets.option_list import Option

starlight = [
    "I see you through the clouds",
    "I feel you anyways",
    "You never walk out",
    "Even on my darkest days",
    "Like a guardian, you're watching over me",
    "Through the depths of my own despair",
    "I look up to the sky and I find my peace",
    "I know you'll be there, so",
    "Starlight, won't you lead the way down this river?",
    "Keep me afloat, keep me afloat",
    "If I ever drift away, won't you be there?",
    "Keep me afloat, keep me afloat",
]


class NarrowOptionsWithInput(ModalScreen):
    def __init__(self, options: list = [], placeholder: str = "Don't drop your jaw!", **kwargs) -> None:
        super().__init__(**kwargs)
        self.placeholder = placeholder
        self.options = options

    def compose(self) -> ComposeResult:
        with VerticalGroup(id="root"):
            yield Input(placeholder=self.placeholder)
            yield OptionList(*self.options)

    def on_mount(self) -> None:
        self.query_one(OptionList).can_focus = False
        self.query_one(Input).focus()

    def on_input_changed(self, event: Input.Changed) -> None:
        value = event.value
        optionlist: OptionList = self.query_one(OptionList)
        optionlist.clear_options()
        for option in self.options:
            if isinstance(option, Option):
                if value.lower() in option.prompt.lower():
                    optionlist.add_option(option)
            elif isinstance(option, str):
                if value.lower() in option.lower():
                    optionlist.add_option(option)
            else:
                raise TypeError(f"Unexpected {type(option)} found.")
        if optionlist.option_count == 0:
            optionlist.add_option(Option("--no matches--", disabled=True))
        optionlist.highlighted = 0

    def on_input_submitted(self, event: Input.Submitted) -> None:
        optionlist = self.query_one(OptionList)
        if optionlist.highlighted is None:
            optionlist.highlighted = 0
        optionlist.action_select()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected):
        self.dismiss(event.option.prompt)

    def on_key(self, event: events.Key) -> None:
        """Handle key presses."""
        match event.key:
            case "escape":
                self.dismiss(None)
            case "down":
                zoxide_options = self.query_one(OptionList)
                if zoxide_options.options:
                    zoxide_options.action_cursor_down()
            case "up":
                zoxide_options = self.query_one(OptionList)
                if zoxide_options.options:
                    zoxide_options.action_cursor_up()
            case "tab":
                self.focus_next()
            case "shift+tab":
                self.focus_previous()


class TextualApp(App):
    def compose(self) -> ComposeResult:
        yield Button("Show the improved optionlist")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.push_screen(NarrowOptionsWithInput(starlight, "Starlight (Keep Me Afloat)"), lambda x: self.notify(str(x)))

if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)
