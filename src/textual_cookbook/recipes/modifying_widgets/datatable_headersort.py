"""This example demonstrates how to create a sortable DataTable
with headers that change their appearance based on the sorting state.
The arrows in the header label will flip direction when the user clicks
on a header to indicate the current sort order.

Recipe by Edward Jazzhands"""

# python standard lib
from __future__ import annotations
import sys
from typing import Any
from enum import Enum

# Textual imports
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import DataTable
from textual.widgets.data_table import Column, ColumnKey
from textual.containers import Container
from rich.text import Text


ROWS = [
    (4, "Joseph Schooling", "Singapore", 50.39),
    (2, "Michael Phelps", "United States", 51.14),
    (5, "Chad le Clos", "South Africa", 51.14),
    (6, "László Cseh", "Hungary", 51.14),
    (3, "Li Zhuhao", "China", 51.26),
    (8, "Mehdy Metella", "France", 51.58),
    (7, "Tom Shields", "United States", 51.73),
    (1, "Aleksandr Sadovnikov", "Russia", 51.84),
    (10, "Darren Burns", "Scotland", 51.84),
]

class SortingStatus(Enum):
    UNSORTED = 0  #     [-] unsorted
    ASCENDING = 1  #    [↑] ascending (reverse = True)
    DESCENDING = 2  #   [↓] descending (reverse = False)


class TextualApp(App[None]):

    DEFAULT_CSS = """
    #datatable_container { align: center middle; }
    DataTable { width: 60; height: auto; }
    """

    sorting_statuses_dict: dict[str, SortingStatus] = {
        "lane": SortingStatus.UNSORTED,
        "swimmer": SortingStatus.UNSORTED, 
        "country": SortingStatus.UNSORTED, 
        "time": SortingStatus.UNSORTED,
    }

    def compose(self) -> ComposeResult:
        self.datatable = DataTable[Any]()
        with Container(id="datatable_container"):
            yield self.datatable

    def on_mount(self) -> None:
        
        self.datatable.add_column("lane [yellow]-[/]", key="lane")
        self.datatable.add_column("swimmer [yellow]-[/]", key="swimmer")
        self.datatable.add_column("country [yellow]-[/]", key="country")
        self.datatable.add_column("time [yellow]-[/]", key="time")
        self.datatable.add_rows(ROWS)

        # Retrieving the actual column from `DataTable.columns` is the trick
        # to making this work. This is different from `DataTable.get_column`, which
        # returns the values of the column, not the actual column object.
        # You need the column object to modify its label.  

        column = self.datatable.columns[ColumnKey("time")]
        self.sort_column(column, column.key)

    @on(DataTable.HeaderSelected)
    def header_selected(self, event: DataTable.HeaderSelected) -> None:
              
        column = self.datatable.columns[event.column_key]
        self.sort_column(column, column.key)
    
    def sort_column(self, column: Column, column_key: ColumnKey) -> None:

        if column_key.value not in self.sorting_statuses_dict:
            raise ValueError(
                f"Unknown column key: {column_key.value}. "
                "This should never happen, please report this issue."
            )

        key = column_key.value
        sort_status = self.sorting_statuses_dict
        table = self.datatable

        if sort_status[key] == SortingStatus.UNSORTED :
            # if column is unsorted, that means the user is switching which
            # column to sort. Start by resetting all columns to unsorted.
            for col_key in sort_status:
                sort_status[col_key] = SortingStatus.UNSORTED
                col_index = table.get_column_index(col_key)
                col = table.ordered_columns[col_index]
                col.label = Text.from_markup(f"{col_key} [yellow]-[/]")

            # Now set chosen column to ascending:
            sort_status[key] = SortingStatus.ASCENDING
            table.sort(column_key, reverse=True)
            column.label = Text.from_markup(f"{key} [yellow]↑[/]")

        # For the other two conditions, we just toggle ascending/descending
        elif sort_status[key] == SortingStatus.ASCENDING:
            sort_status[key] = SortingStatus.DESCENDING 
            table.sort(key, reverse=False)
            column.label = Text.from_markup(f"{key} [yellow]↓[/]")
        elif sort_status[key] == SortingStatus.DESCENDING: 
            sort_status[key] = SortingStatus.ASCENDING  
            table.sort(column_key, reverse=True)
            column.label = Text.from_markup(f"{key} [yellow]↑[/]")
        else:
            raise ValueError(
                f"Sort status for {key} is '{sort_status[key]}' "
                "did not meet any expected values."
            )
        

if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)