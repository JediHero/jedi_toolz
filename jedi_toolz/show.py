__all__ = ['transpose', 'wrap_row', 'wrap_table', 'show']

# Internal Cell
try:
    import pandas
    has_pandas = lambda: True
except ModuleNotFoundError:
    has_pandas = lambda: False

from tabulate import tabulate
from textwrap import fill
import toolz.curried as tz
import itertools as it
from decorator import decorator

@decorator
def handle_pandas(func, *args, **kwargs):
    orig = [arg for arg in args]
    data = orig[0]
    if has_pandas() and isinstance(data, pandas.DataFrame):
        data = data.to_dict("records")
    updated = [data if num == 0 else arg for num, arg in enumerate(orig)]
    return func(*updated, **kwargs)

@handle_pandas
def text_table(data, print_out=True, **tabulate_args):
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

@handle_pandas
def head(data, limit=100):
    return list(tz.take(limit, data))

@handle_pandas
def transpose(data):
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
    result = {}
    for k, v in row.items():
        new_k = fill(str(k), col_width)
        new_v = fill(str(v), col_width)
        result[new_k] = new_v
    return result

@handle_pandas
def wrap_table(data, col_width):
    """Takes a list of dicts and wraps the keys and values by the
    specified col_width."""
    return [wrap_row(row, col_width) for row in data]

def text_width(text):
    return max(len(line) for line in text.splitlines())

@handle_pandas
def get_text(data, limit, vert, col_width):
    return tz.pipe(
        head(data, limit),
        lambda table: transpose(table) if vert else table,
        tz.partial(wrap_table, col_width=col_width),
        tz.partial(text_table, print_out=False),
    )

@tz.curry
@handle_pandas
def show(data, limit=30, vert=False, col_width=15, table_width=80):
    orig = get_text(data, limit, vert, col_width)
    if text_width(orig) <= table_width:
        print(orig)
        return None
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
        else:
            print(good)
            return None