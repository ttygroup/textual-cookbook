"""This file demonstrates how to create a DataTable with a dynamic first column
that expands to fill the available space, while keeping other columns at
fixed widths. The table will also auto-adjust the first column's width
when the terminal is resized.

Recipe by Edward Jazzhands"""

import sys
from typing import Any
from textual.widgets import DataTable
from textual.widgets.data_table import ColumnKey
from textual.app import App, ComposeResult
from textual.containers import Container

ROWS = [
    ("Joseph Schooling", "Singapore", 50.39, 4),
    ("Michael Phelps", "United States", 51.14, 2),
    ("Chad le Clos", "South Africa", 51.14, 5),
    ("László Cseh", "Hungary", 51.14, 6),
    ("Li Zhuhao", "China", 51.26, 3),
    ("Mehdy Metella", "France", 51.58, 8),
    ("Tom Shields", "United States", 51.73, 7),
    ("Aleksandr Sadovnikov", "Russia", 51.84, 1),
    ("Darren Burns", "Scotland", 51.84, 10),
]

class MyDataTable(DataTable[Any]):

    col1_minimum = 15   # dynamic column
    col2_width = 20
    col3_width = 15
    col4_width = 10
    other_cols_total = col2_width + col3_width + col4_width

    def on_mount(self) -> None:

        self.add_column("Name", width=self.col1_minimum, key="col1")
        self.add_column("Country", width=self.col2_width, key="col2")
        self.add_column("Time", width=self.col3_width, key="col3")
        self.add_column("Lane", width=self.col4_width, key="col4")
        self.add_rows(ROWS) 

    def on_resize(self) -> None:
        
        # Account for padding on both sides of each column:
        total_cell_padding = self.cell_padding * (len(self.columns)*2)

        # Pretty obvious how this works I think:
        first_col_width = self.size.width - self.other_cols_total - total_cell_padding

        # Prevent column from being smaller than the chosen minimum:
        if first_col_width < self.col1_minimum:
            first_col_width = self.col1_minimum

        self.columns[ColumnKey("col1")].width = first_col_width
        self.refresh()
        

class TextualApp(App[None]):

    def compose(self) -> ComposeResult:
        with Container():
            yield MyDataTable()


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)