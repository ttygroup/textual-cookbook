"""Textual Cookbook Recipe Runner
================================

# ~ Type Checking (Pyright and MyPy) - Strict Mode
# ~ Linting - Ruff
# ~ Formatting - Black - max 110 characters / line
"""

# python standard lib
from __future__ import annotations
from typing import TypedDict, Any
import subprocess
import sys
import re
from pathlib import Path
from importlib import resources
# from importlib.abc import Traversable
# import importlib
from enum import Enum

# Textual imports
from textual import on, work, events
from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Static, DataTable, Button, Markdown, TextArea
from textual.widgets.data_table import ColumnKey, Column
from textual.screen import Screen, ModalScreen
from textual.message import Message
from textual.containers import Horizontal, Vertical
from textual.binding import Binding
from textual.geometry import clamp
from rich.text import Text

# Textual library imports
from textual_pyfiglet import FigletWidget

class RecipeData(TypedDict):
    name: str
    category: str
    author: str
    description: str
    text_blob: str


class SortableText(Text):

    def __lt__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.plain < other
        if isinstance(other, Text):
            return self.plain < other.plain
        return NotImplemented


class DescriptionScreen(ModalScreen[bool]):

    BINDINGS = [
        Binding("escape", "close_screen", description="Close the help window."),
        Binding("left", "app.focus_previous", description="Focus Previous"),
        Binding("right", "app.focus_next", description="Focus Next"),
    ]

    def __init__(self, description: str) -> None:
        super().__init__()
        self.description = description

    def compose(self) -> ComposeResult:

        with Vertical(classes="description_container"):
            yield Markdown(self.description)
            with Horizontal(classes="button_container modal"):
                yield Button("Run", id="run_button_modal", compact=True)
                yield Button("Back", id="back_button", compact=True)

    @on(Button.Pressed, "#run_button_modal")
    def run_button_pressed(self) -> None:
        self.dismiss(True)

    @on(Button.Pressed, "#back_button")
    def back_button_pressed(self) -> None:
        self.dismiss(False)

    def on_click(self, event: events.Click) -> None:
        
        if isinstance(event.control, DescriptionScreen):
            self.dismiss(False)

    def action_close_screen(self) -> None:
        self.dismiss()


class ErrorScreen(ModalScreen[bool]):

    BINDINGS = [
        Binding("escape", "close_screen", description="Close the help window."),
    ]

    def __init__(self, error: subprocess.CalledProcessError) -> None:
        super().__init__()
        self.error = error

    def compose(self) -> ComposeResult:

        with Vertical(classes="description_container"):
            yield Static(
                "[$accent]Recipe failed to run[/$accent] \n\n"
                "Close the cookbook to view the error output.\n",
                markup=True
            )
            with Horizontal(classes="button_container modal"):
                yield Button("Close", id="close_button", compact=True)

    @on(Button.Pressed, "#close_button")
    def close_button_pressed(self) -> None:
        self.dismiss(False)

    def on_click(self, event: events.Click) -> None:
        
        if isinstance(event.control, ErrorScreen):
            self.dismiss(False)

    def action_close_screen(self) -> None:
        self.dismiss()


class ResizeBar(Static):

    DEFAULT_CSS = """
    ResizeBar {
        width: 1;
        height: 1fr;
        border-left: outer $panel;
        &:hover { border-left: outer $primary-darken-2; }
        &.pressed {   border-left: outer $primary-lighten-1; }
    }
    """

    def __init__(self, parent: Widget, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.connected_container = parent
        self.min_width = 25    # adjust as needed
        self.max_width = 80
        self.tooltip = "<-- Drag to resize -->"

    def on_mouse_move(self, event: events.MouseMove) -> None:

        # App.mouse_captured refers to the widget that is currently capturing mouse events.
        if self.app.mouse_captured == self:

            total_delta = event.screen_offset - self.position_on_down
            new_size = self.size_on_down - total_delta
        
            self.connected_container.styles.width = clamp(new_size.width, self.min_width, self.max_width)

    def on_mouse_down(self, event: events.MouseDown) -> None:

        self.max_width = self.app.screen.size.width - 10
        self.position_on_down = event.screen_offset
        self.size_on_down = self.connected_container.size

        self.add_class("pressed")    # this requires a "pressed" class to exist
        self.capture_mouse()

    def on_mouse_up(self) -> None:

        self.remove_class("pressed")
        self.release_mouse()


class CodeContainer(Horizontal):

    def compose(self) -> ComposeResult:
        yield ResizeBar(self)
        with Vertical():
            with Horizontal():
                yield Static(id="current_recipe")
                yield Static(id="current_category")
                with Button("Run", id="run_button", compact=True) as butt:
                    butt.can_focus = False
            yield TextArea(
                "Select a recipe \n"
                "Hint: You can resize this area by dragging \n"
                "<-- this Resize bar with your mouse.",
                # language="markdown",
                read_only=True,
                show_line_numbers=True,
                soft_wrap=False,
                tab_behavior="indent"
            )

    def update(self, recipe_data: RecipeData):
        self.query_one("#current_recipe", Static).update(f"🗎 {recipe_data['name']}.py  │")
        self.query_one("#current_category", Static).update(f"🗁  {recipe_data['category']}")
        text_area = self.query_one(TextArea)
        text_area.language = "python"
        text_area.text = recipe_data['text_blob']


class CustomDataTable(DataTable[Any]):

    class TableInitialized(Message):
        pass

    class SortingStatus(Enum):
        UNSORTED = 0  #     [-] unsorted
        ASCENDING = 1  #    [↑] ascending (reverse = True)
        DESCENDING = 2  #   [↓] descending (reverse = False)


    def __init__(
        self,
        recipe_data_dict: dict[str, RecipeData], 
    ) -> None:
        super().__init__(zebra_stripes=True, show_cursor=True, cursor_type="row")
        self.recipe_data_dict = recipe_data_dict
        self.initialized = False

        self.sort_status: dict[str, CustomDataTable.SortingStatus] = {
            "name": CustomDataTable.SortingStatus.UNSORTED,
            "category": CustomDataTable.SortingStatus.UNSORTED,
            "author": CustomDataTable.SortingStatus.UNSORTED,
        }

        for key in self.sort_status:
            self.add_column(f"{key} [dark_orange]-[/]", key=key)

    def on_mount(self) -> None:

        for recipe_data in self.recipe_data_dict.values():

            self.add_row(
                SortableText(recipe_data["name"], overflow="ellipsis"),
                SortableText(recipe_data["category"], overflow="ellipsis"),
                SortableText(recipe_data["author"], overflow="ellipsis"),
            )        

    @on(DataTable.HeaderSelected)
    def header_selected(self, event: DataTable.HeaderSelected) -> None:

        column = self.columns[event.column_key]
        self.sort_column(column, column.key)


    def sort_column(self, column: Column, column_key: ColumnKey) -> None:

        if column_key.value is None:
            raise ValueError("Tried to sort a column with no key.")
        if column_key.value not in self.sort_status:
            raise ValueError(
                f"Unknown column key: {column_key.value}. "
                "This should never happen, please report this issue."
            )
        value = column_key.value

        # if its currently unsorted, that means the user is switching columns
        # to sort. Reset all columns to unsorted.
        if self.sort_status[value] == self.SortingStatus.UNSORTED:
            for key in self.sort_status:
                self.sort_status[key] = self.SortingStatus.UNSORTED
                col_index = self.get_column_index(key)
                col = self.ordered_columns[col_index]
                col.label = Text.from_markup(f"{key} [dark_orange]-[/]")

            # Now set chosen column to ascending:
            self.sort_status[value] = self.SortingStatus.ASCENDING
            self.sort(column_key, reverse=True)
            column.label = Text.from_markup(f"{value} [dark_orange]↑[/]")

        # For the other two conditions, we just toggle ascending/descending
        elif self.sort_status[value] == self.SortingStatus.ASCENDING:
            self.sort_status[value] = self.SortingStatus.DESCENDING
            self.sort(value, reverse=False)
            column.label = Text.from_markup(f"{value} [dark_orange]↓[/]")
        elif self.sort_status[value] == self.SortingStatus.DESCENDING:
            self.sort_status[value] = self.SortingStatus.ASCENDING
            self.sort(column_key, reverse=True)
            column.label = Text.from_markup(f"{value} [dark_orange]↑[/]")
        else:
            raise ValueError(
                f"Sort status for {value} is '{self.sort_status[value]}', did not meet any expected values."
            )


class TableScreen(Screen[None]):

    BINDINGS = [
        Binding("1", "sort_column(0)", "Sort Column 1"),
        Binding("2", "sort_column(1)", "Sort Column 2"),
        Binding("3", "sort_column(2)", "Sort Column 3"),
        Binding("d", "show_description", "Show Description"),
    ]

    def __init__(self, recipe_data_dict: dict[str, RecipeData]) -> None:
        super().__init__()
        self.recipe_data_dict = recipe_data_dict
        self.selected_recipe = None

    def compose(self) -> ComposeResult:

        with Vertical(id="main_container"):
            with Vertical(id="header_container"):
                yield FigletWidget(
                    "TeXTuaL cOOkBOOk",
                    font="double_blocky",
                    colors=["red", "red", "magenta"],
                    horizontal=True,
                    animate=True,
                    fps=30,
                )
                yield Static(
                    "Select once to view code, select again to run",
                    id="header_text",
                )
            with Vertical(id="table_container"):
                self.table = CustomDataTable(self.recipe_data_dict)
                yield self.table
            with Vertical(id="bottom_container"):
                yield Static(
                    "[$accent]Up/Down[/] Navigate │ "
                    "[$accent]Enter[/]/[$accent]Click[/] Select │ "
                    "[$accent]1-3[/] Sort │ "
                    "[$accent]d[/] Description",
                    id="controls_bar",
                )
                with Horizontal(classes="button_container"):
                    yield Button("Quit", id="quit_button", compact=True)
        yield CodeContainer()

    def action_sort_column(self, column_index: int) -> None:

        try:
            column = self.table.ordered_columns[column_index]
        except IndexError:
            return
        else:
            self.table.sort_column(column, column.key)

    @on(Button.Pressed, "#run_button")
    def run_button_pressed(self) -> None:

        if self.selected_recipe is None:
            self.notify("No recipe selected", timeout=3)
        else:
            category = self.recipe_data_dict[self.selected_recipe]["category"]
            self.run_recipe(self.selected_recipe, category)        

    @on(DataTable.RowSelected)
    @work
    async def recipe_selected(self, event: DataTable.RowSelected) -> None:

        row_data: list[str] = self.table.get_row(event.row_key)
        recipe_name = str(row_data[0])
        recipe_data = self.recipe_data_dict[recipe_name]
        category = self.recipe_data_dict[recipe_name]["category"]
        code_container = self.query_one(CodeContainer)

        if recipe_name == self.selected_recipe:
            self.run_recipe(recipe_name, category)
        else:
            self.selected_recipe = recipe_name
            code_container.update(recipe_data)

    @work
    async def action_show_description(self) -> None:

        cursor_index = self.table.cursor_row
        row_data: list[str] = self.table.get_row_at(cursor_index)
        recipe_name = str(row_data[0])
        description = self.recipe_data_dict[recipe_name]["description"]
        result = await self.app.push_screen(DescriptionScreen(description), wait_for_dismiss=True)
        if result:
            category = self.recipe_data_dict[recipe_name]["category"]
            self.run_recipe(recipe_name, category)

    def run_recipe(self, recipe_name: str, category: str) -> None:

        with self.app.suspend():

            cookbook = resources.files("textual_cookbook")
            recipe_traversable = cookbook.joinpath(f"recipes/{category}/{recipe_name}.py")

            # as_file gives a real filesystem Path (extracts to a temp file if inside a zip/wheel)
            with resources.as_file(recipe_traversable) as recipe_path:
                try:
                    subprocess.run([sys.executable, str(recipe_path)], check=True)
                except subprocess.CalledProcessError as e:
                    self.app.push_screen(ErrorScreen(e))
                except Exception as e:
                    raise e


    @on(Button.Pressed, "#quit_button")
    def quit_button_pressed(self) -> None:
        self.set_timer(0.2, self.app.exit)


class CookBookApp(App[None]):

    CSS_PATH = "styles.tcss"

    class WorkerFinished(Message):
        def __init__(self, recipe_data_dict: dict[str, RecipeData]) -> None:
            super().__init__()
            self.recipe_data_dict = recipe_data_dict

    def on_mount(self) -> None:
        self.run_worker(self.scan_for_recipes)

    async def scan_for_recipes(self) -> None:

        recipe_data_dict: dict[str, RecipeData] = {}
        
        # NEW: Start with Traversable then convert to Path for easier handling
        recipes_traversable = resources.files("textual_cookbook").joinpath("recipes")
        recipes_dir = Path(str(recipes_traversable))

        # Simple one-level scan - categories are subdirectories, no files in root
        for recipe_file in recipes_dir.rglob("*.py"):
            with open(recipe_file, "r", encoding="utf-8") as f:
                text_blob = f.read()
                author_match = re.search(r"Recipe by (.+)", text_blob)
                if author_match:
                    author = author_match.group(1).strip()
                    author = author.replace('"', "")
                else:
                    author = "Unknown"

            description_match = re.match(r'"""(.*?)"""', text_blob, re.DOTALL)
            if description_match:
                description = description_match.group(1).strip()
            else:
                description = "No description available."

            recipe_data: RecipeData = {
                "name": recipe_file.stem,
                "category": recipe_file.parent.name,
                "author": author,
                "description": description,
                "text_blob": text_blob
            }
            recipe_data_dict[recipe_file.stem] = recipe_data

        self.post_message(CookBookApp.WorkerFinished(recipe_data_dict))


    @on(WorkerFinished)
    async def worker_finished(self, message: WorkerFinished) -> None:

        await self.push_screen(TableScreen(message.recipe_data_dict))

def run_main() -> None:
    CookBookApp().run()

if __name__ == "__main__":
    run_main()