from typing import Iterable
from rich.style import Style
from worklogi.entry import Entry
from rich.console import Console
from rich.table import Table
from itertools import groupby
from .database import WorkLogDatabase


def browse_day(entries: Iterable[Entry]):
    table = Table(title="worklogi")
    for column in Entry.get_header():
        table.add_column(column)
    for entry in entries:
        table.title = entry.datetime().date().isoformat()
        is_checkout = entry.title == "checkout"
        is_rebase = entry.branch == "HEAD"
        row_style = Style(dim=is_rebase, bold=is_checkout)
        table.add_row(*entry.get_data(), style=row_style)

    console = Console()
    console.print(table)

def browse_entries(_):
    entries = WorkLogDatabase.get_entries()
    list_of_entries = list(entries)
    for _, group in groupby(reversed(list_of_entries), key=lambda entry: entry.datetime().date().day):
        browse_day(group)
        input()
