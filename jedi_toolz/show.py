__all__ = ['transpose', 'wrap_row', 'wrap_table', 'show']

# Internal Cell
from jedi_toolz.data import handle_data, Table
from textwrap import fill
import toolz.curried as tz
import itertools as it
from tabulate import tabulate
from typing import Union

__all__ = "show transpose wrap_table".split()

@handle_data
def text_table(data, print_out=True, **tabulate_args):
    """A partial version of the tabulate.tabulate function."""
    defaults = {
        "tablefmt": "fancy_grid",
        "floatfmt": ",.2f",
        "headers": "keys"
    }
    tabulate_args = {**defaults, **tabulate_args}
    tab = tz.partial(tabulate, **tabulate_args)
    if print_out:
        print(tab(data))
    else:
        return tab(data)

@handle_data
def head(data: Table, limit=100) -> Table:
    """Returns the first {limit} records of a Table."""
    return list(tz.take(limit, data))

@handle_data
def transpose(data: Table) -> Table:
    """Transposes a table (list of dicts) such that columns are
    rows and rows are columns.
    """
    count = it.count(1)
    row_num = lambda: next(count)
    header = lambda d: list(d.keys())
    values = lambda d: list(zip(*d.values()))
    combine = lambda d: [dict(zip(header(d), row)) for row in values(d)]
    return tz.pipe(
        data,
        tz.map(lambda row: list(zip(*row.items()))),
        tz.map(lambda row: dict(zip(["column", f"row {row_num()}"], row))),
        tz.merge,
        combine,
    )

def wrap_row(row, col_width):
    """Returns a string version of a dict with long values split
    into lines."""
    result = {}
    for k, v in row.items():
        new_k = fill(str(k), col_width)
        new_v = fill(str(v), col_width)
        result[new_k] = new_v
    return result

@handle_data
def wrap_table(data, col_width):
    """Takes a list of dicts and wraps the keys and values by the
    specified col_width."""
    return [wrap_row(row, col_width) for row in data]

def text_width(text):
    return max(len(line) for line in text.splitlines())

@handle_data
def get_text(data, limit, vert, col_width):
    """Returns the text to be printed by text_table."""
    return tz.pipe(
        head(data, limit),
        lambda table: transpose(table) if vert else table,
        tz.partial(wrap_table, col_width=col_width),
        tz.partial(text_table, print_out=False),
    )

@tz.curry
@handle_data
def show(data, limit=30, vert=False, col_width=15, table_width=80,
    print_out: bool=True) -> str:
    """Prints an ascii table using the tabulate.tabulate function.
    col_width and table_width parameters can be provided to customize
    the width and appearance of the table.

    vert = True will transpose the data (columns are rows and rows
    are columns).

    limit can be used to determine the number of rows printed.
    """
    orig = get_text(data, limit, vert, col_width)
    if text_width(orig) <= table_width:
        if print_out:
            print(orig)
            # return ""
            return None
        else:
            return orig
    else:
        good = get_text(data, limit=1, vert=True, col_width=col_width)
        msg = (
            "Showing 1 row vertically exceeds table_width. "
            "Please adjust table_width or col_width."
        )
        assert text_width(good) <= table_width, msg

    for n in range(2, len(data)):
        new = get_text(data, n, True, col_width)
        if text_width(new) <= table_width:
            good = new
        elif print_out:
            print(good)
            # return ""
            return None
        elif not print_out:
            return good
