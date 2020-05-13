from typing import List, Dict, Any, Iterator, Union, Callable, Sequence
from decorator import decorator
from datetime import datetime, date
import re
from jedi_toolz.str_funcs import *

__all__ = (
    "to_table handle_data pretty_names"
).split()

RecordValue = Union[str, bool, int, float, date,
    datetime, None]
Record = Dict[str, RecordValue]
Table = Iterator[Record]


def has_all_attrs(obj: Any, attrs: str) -> bool:
    """Checks an object for all of the provided attrs."""
    assert isinstance(attrs, str)
    return all([hasattr(obj, attr)
        for attr in attrs.split()])

def has_any_attrs(obj: Any, attrs: str) -> bool:
    """Checks an object for any of the provided attrs."""
    assert isinstance(attrs, str)
    return any([hasattr(obj, attr)
        for attr in attrs.split()])

def is_pandas(data: Any) -> bool:
    """Returns True if data is a pandas.DataFrame."""
    assert data is not None
    attrs = (
        "values columns transpose head to_dict "
        "from_records"
    )
    return has_all_attrs(data, attrs)

def is_ipython() -> bool:
    """Returns True if the module is running inside an ipython kernal."""
    return hasattr(__builtins__,'__IPYTHON__')

def is_record(data: Any) -> bool:
    assert data is not None
    if not isinstance(data, dict):
        return False
    if not all([isinstance(k, str) for k in data]):
        return False
    else:
        return True

def is_table(data: Any) -> bool:
    assert data is not None

    if is_pandas(data): return False
    if isinstance(data, dict): return False

    attrs = "__iter__ __next__"
    if not has_any_attrs(data, attrs): return False

    first_row = next(iter(data))
    return is_record(first_row)

def to_table(data: Any) -> Table:
    assert data is not None

    if is_table(data):
        return data

    elif is_record(data):
        return [
            {"column": k, "value": v}
            for k, v in data.items()
        ]

    elif isinstance(data, dict):
        return [
            {"column": str(k), "value":v}
            for k, v in data.items()
        ]

    elif is_pandas(data):
        records = data.to_dict("records")
        return [
            {str(k): v for k, v in row.items()}
            for row in records
        ]

    else:
        raise ValueError(
            "data does not appear to be an Iterator of dicts, a "
            "dict, or a DataFrame."
        )

@decorator
def handle_data(func, *args, **kwargs):
    arg1, *other_args = args
    data = to_table(arg1)
    updated_args = data, *other_args
    return func(*updated_args, **kwargs)

def pretty_names(data: Any, *funcs) -> Any:
    """Returns the Table with pretty names.
    uses the pretty_str function to modify names.
    """
    defaults = (
        decamel,
        invalid_first_char,
        replace_non_word,
        conseq_char,
        trim,
        lambda s: s.replace("_", " "),
    )
    if len(funcs) == 0:
        funcs = defaults

    if is_pandas(data):
        return data.rename(columns={
            col: fmt_str(col, *funcs)
            for col in data.columns
        })
    else:
        return [
            {fmt_str(k, *funcs): v for k, v in row.items()}
            for row in to_table(data)
        ]