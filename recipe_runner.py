"""Textual Cookbook Recipe Runner
================================

# ~ Type Checking (Pyright and MyPy) - Strict Mode
# ~ Linting - Ruff
# ~ Formatting - Black - max 110 characters / line
"""

# python standard lib
from __future__ import annotations
from typing import TypedDict, Any
import os
import re
from pathlib import Path
from enum import Enum

# Textual imports
from textual import on, work, events
from textual.app import App, ComposeResult
from textual.widgets import Static, DataTable, Button, Markdown
from textual.widgets.data_table import ColumnKey, Column
from textual.screen import Screen, ModalScreen
from textual.message import Message
from textual.containers import Horizontal, Vertical
from textual.binding import Binding
from rich.text import Text

# Textual library imports
from textual_pyfiglet import FigletWidget


class RecipeData(TypedDict):
    name: str
    category: str
    author: str
    description: str


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
                yield Button("Run", id="run_button", compact=True)
                yield Button("Back", id="back_button", compact=True)

    @on(Button.Pressed, "#run_button")
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

    @on(DataTable.RowSelected)
    @work
    async def recipe_selected(self, event: DataTable.RowSelected) -> None:

        row_data: list[str] = self.get_row(event.row_key)
        recipe_name = str(row_data[0])
        directory = str(row_data[1])
        description = self.recipe_data_dict[recipe_name]["description"]
        result = await self.app.push_screen(DescriptionScreen(description), wait_for_dismiss=True)
        if result:
            self.run_recipe(recipe_name, directory)

    def run_recipe(self, recipe_name: str, directory: str) -> None:

        with self.app.suspend():
            os.system(f"uv run recipes/{directory}/{recipe_name}.py")



class TableScreen(Screen[None]):

    BINDINGS = [
        Binding("1", "sort_column(0)", "Sort Column 1"),
        Binding("2", "sort_column(1)", "Sort Column 2"),
        Binding("3", "sort_column(2)", "Sort Column 3"),
        Binding("d", "description_screen", "Show Description"),
    ]

    def __init__(self, recipe_data_dict: dict[str, RecipeData]) -> None:
        super().__init__()
        self.recipe_data_dict = recipe_data_dict

    def compose(self) -> ComposeResult:

        with Vertical(id="header_container"):
            yield FigletWidget(
                "TeXTuaL cOOkBOOk",
                font="double_blocky",
                colors=["red", "red", "magenta"],
                horizontal=True,
                animate=True,
                # gradient_quality=30,
                fps=30,
            )
            yield Static(
                "Select a recipe to run (Keyboard and Mouse supported)",
                id="header",
            )
        with Vertical(id="table_container"):
            self.table = CustomDataTable(self.recipe_data_dict)
            yield self.table
        with Vertical(id="bottom_container"):
            yield Static(
                "[orange]Up/Down[/] Navigate │ "
                "[orange]Enter[/] Run │ "
                "[orange]1-3[/] Sort │ "
                "[orange]r[/] Run directly | "
                "[orange]Ctrl+q[/] Quit",
                id="controls_bar",
            )
            with Horizontal(classes="button_container"):
                quit_button = Button("Quit", id="quit_button", compact=True)
                quit_button.can_focus = False
                yield quit_button

    def action_sort_column(self, column_index: int) -> None:

        try:
            column = self.table.ordered_columns[column_index]
        except IndexError:
            return
        else:
            self.table.sort_column(column, column.key)

    # def action_description_screen(self) -> None:

    #     current_index = self.table.cursor_row
    #     row_data = self.table.get_row_at(current_index)
    #     recipe_name = str(row_data[0])
    #     description = self.recipe_data_dict[recipe_name]["description"]
    #     self.app.push_screen(DescriptionScreen(description))

    @on(Button.Pressed, "#quit_button")
    def quit_button_pressed(self) -> None:
        self.set_timer(0.2, self.app.exit)


class CookBookApp(App[None]):

    CSS_PATH = "recipe_runner_styles.tcss"

    class WorkerFinished(Message):
        def __init__(self, recipe_data_dict: dict[str, RecipeData]) -> None:
            super().__init__()
            self.recipe_data_dict = recipe_data_dict

    def on_mount(self) -> None:
        self.run_worker(self.scan_for_recipes)

    async def scan_for_recipes(self) -> None:

        recipe_data_dict: dict[str, RecipeData] = {}
        recipes_dir = Path(__file__).parent / "recipes"
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
            }
            recipe_data_dict[recipe_file.stem] = recipe_data

        self.post_message(CookBookApp.WorkerFinished(recipe_data_dict))

    @on(WorkerFinished)
    async def worker_finished(self, message: WorkerFinished) -> None:

        await self.push_screen(TableScreen(message.recipe_data_dict))
    

if __name__ == "__main__":
    CookBookApp().run()    