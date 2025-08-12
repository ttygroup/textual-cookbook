"""This script demonstrates how the content of the MarkdownViewer widget
can be updated using the `document.update()` method.

Recipe by Edward Jazzhands"""

import sys
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import MarkdownViewer, Button

MARKDOWN1 = """\
# Markdown Viewer

Markdown syntax and extensions are supported.

- Typography *emphasis*, **strong**, `inline code` etc.
- Headers
- Lists (bullet and ordered)
- Syntax highlighted code blocks
- Tables!

# Header 2
"""

MARKDOWN2 = """\
# Header 1

| Name            | Type   | Default | Description                        |
| --------------- | ------ | ------- | ---------------------------------- |
| `show_header`   | `bool` | `True`  | Show the table header              |
| `fixed_rows`    | `int`  | `0`     | Number of fixed rows               |
| `fixed_columns` | `int`  | `0`     | Number of fixed columns            |
| `zebra_stripes` | `bool` | `False` | Display alternating colors on rows |
| `header_height` | `int`  | `1`     | Height of header row               |
| `show_cursor`   | `bool` | `True`  | Show a cell cursor                 |

# Header 2
"""

class TextualApp(App[None]):

    def compose(self) -> ComposeResult:

        self.markdown_viewer = MarkdownViewer(MARKDOWN1, id="markdown_viewer")
        yield self.markdown_viewer
        yield Button("Markdown 1", id="markdown1")
        yield Button("Markdown 2", id="markdown2")

    @on(Button.Pressed, selector="#markdown1")
    def markdown1_pressed(self) -> None:
        self.markdown_viewer.document.update(MARKDOWN1)

    @on(Button.Pressed, selector="#markdown2")
    def markdown2_pressed(self) -> None:
        self.markdown_viewer.document.update(MARKDOWN2)        


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)