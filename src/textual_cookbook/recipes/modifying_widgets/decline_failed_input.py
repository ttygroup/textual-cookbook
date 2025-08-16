from asyncio import sleep

from textual import events, work
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup
from textual.screen import ModalScreen
from textual.validation import Function
from textual.widgets import Input, Button


class ModalInput(ModalScreen):
    def __init__(
        self,
        border_title: str,
        border_subtitle: str = "",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.border_title = border_title
        self.border_subtitle = border_subtitle
        self.validators = [
            Function(lambda x: "h" in x, "The character 'h' isnt in the string!"),
            Function(lambda x: "i" in x, "The character 'i' isnt in the string!"),
        ]

    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield Input(
                id="input",
                compact=True,
                valid_empty=False,
                validators=self.validators,
                validate_on=["changed", "submitted"],
            )

    @work(exclusive=True)
    async def on_input_changed(self, event: Input.Changed) -> None:
        if self.query_one(Input).is_valid:
            self.horizontal_group.classes = "valid"
            self.horizontal_group.border_subtitle = self.border_subtitle
        else:
            self.horizontal_group.classes = "invalid"
            try:
                self.horizontal_group.border_subtitle = str(
                    event.validation_result.failure_descriptions[0]
                )
            except AttributeError:
                # valid_empty = False
                self.horizontal_group.border_subtitle = "The word cannot be empty!"

    def on_mount(self) -> None:
        self.horizontal_group: HorizontalGroup = self.query_one(HorizontalGroup)
        inp: Input = self.query_one(Input)
        self.horizontal_group.border_title = self.border_title
        if self.border_subtitle != "":
            self.horizontal_group.border_subtitle = self.border_subtitle
        inp.focus()
        inp.validate(inp.value)
        self.on_input_changed(inp.Changed(inp, inp.value))

    @work
    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission."""
        if not self.query_one(Input).is_valid:
            # shake
            for i in range(3):
                self.horizontal_group.styles.offset = (1, 0)
                await sleep(0.1)
                self.horizontal_group.styles.offset = (0, 0)
                await sleep(0.1)
            return
        self.dismiss(event.input.value)

    def on_key(self, event: events.Key) -> None:
        """Handle escape key to dismiss the dialog."""
        if event.key == "escape":
            event.stop()
            self.dismiss("")

class Application(App):
    CSS = """
    ModalInput {
      align: center middle;
      HorizontalGroup {
        border: round $border;
        width: 50vw;
        max-height: 3;
        padding: 0 1;
        background: transparent !important;
        &.invalid {
          border: round $error-lighten-3
        }
        &:light {
          border: round $error;
        }
      }
      Input { background: transparent !important }
      Label {
        height: 1;
      }
    }
    """
    def compose(self) -> ComposeResult:
        yield Button("Open an input dialog!")
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.push_screen(ModalInput("What word do you start a greeting with?"), callback=self.notify)

Application().run()
