# %%
from typing import List, Dict, Any, Iterable, Union
import toolz.curried as tz
from decorator import decorator
from datetime import datetime, date
import re

__all__ = "to_table handle_data decamel multichar pretty_names".split()

RecordValue = Union[str, bool, int, float, date,
    datetime, None]
Record = Dict[str, RecordValue]
Table = Iterable[Record]

# %%
def has_all_attrs(obj: Any, attrs: str) -> bool:
    """Checks an object for all of the provided attrs."""
    assert isinstance(attrs, str)
    return all([hasattr(obj, attr)
        for attr in attrs.split()])

# %%
def has_any_attrs(obj: Any, attrs: str) -> bool:
    """Checks an object for any of the provided attrs."""
    assert isinstance(attrs, str)
    return any([hasattr(obj, attr)
        for attr in attrs.split()])

# %%
def is_pandas(data: Any) -> bool:
    """Returns True if data is a pandas.DataFrame."""
    assert data is not None
    attrs = (
        "values columns transpose head to_dict "
        "from_records"
    )
    return has_all_attrs(data, attrs)

# %%
def is_record_value(value: Any) -> bool:
    """Returns True if value is a valid record value."""
    test = isinstance(value, (str, bool, int, float, date,
        datetime))
    return test or value is None

# %%
def record_value(value: Any, use_repr: bool=False
    ) -> RecordValue:
    """Returns a valid record value or str if not a valid
    record value."""
    return (
        value if is_record_value(value) else
        str(value)
    )

# %%
def is_record(data: Any) -> bool:
    assert data is not None
    if not isinstance(data, dict):
        return False
    if not all([isinstance(k, str) for k in data]):
        return False
    if not all([ is_record_value(v)
        for k, v in data.items()]):
        return False
    else:
        return True

# %%
def is_table(data: Any) -> bool:
    assert data is not None
    if is_pandas(data): return False
    attrs = "__iter__ __next__"
    if not has_any_attrs(data, attrs):
        return False
    first_row, _ = tz.peek(data)
    return is_record(first_row)

# %%
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
            {"column": str(k), "value": record_value(v)}
            for k, v in data.items()
        ]

    elif is_pandas(data):
        records = data.to_dict("records")
        return [
            {str(k): v}
            for row in records
            for k, v in row.items()
        ]

    else:
        raise ValueError(
            "data does not appear to be an Iterable of dicts, a "
            "dict, or a DataFrame."
        )

# %%
@decorator
def handle_data(func, *args, **kwargs):
    arg1, *other_args = args
    data = to_table(arg1)
    updated_args = data, *other_args
    return func(*updated_args, **kwargs)

# %%
def decamel(string: str, sep: str="_"):
    """Adds a sep character to a camelCase string.
    decamel('FirstNameMD', '_') -> 'First_Name_MD'
    """
    assert isinstance(string, str), f"string must be a string, " \
        "received {repr(string)}"
    string = str(string) or ""
    prev_char = ""
    result = ""
    for char in string:
        if prev_char.islower() and char.isupper():
            result += f"{sep}{char}"
        else:
            result += char
        prev_char = char
    return result

# %%
def multichar(string: str, char: str=" ", trim: bool=True):
    """Replaces consecutive characters with a single character.
    Optionally, can replace the character at the beginning or end
    with a space.
    multichar('_First__Name___MD_', '_') -> 'First_Name_MD'.
    """
    assert isinstance(string, str), f"string must be a string, " \
        "received {repr(string)}"
    result = re.sub(f"{char}+", f"{char}", string)
    if trim:
        return re.sub(f"^{char}+|{char}+$", "", result)
    else:
        return result

# %%
@tz.curry
@handle_data
def pretty_names(data: Any, *funcs) -> Table:
    """Returns the Table with pretty names.
    By default, the following functions are applied in order:
    1. decamel with sep = "_"
    2. multichar with char = "_" and trim = True
    3. str.replace with old = "_" and new = " "

    User can provide own list of funcs instead of the defaults.
    However, each func must accept only 1 arg which is the column
    name or string. Use functools.partial to fix functions as
    needed.

    >>> tbl = [
        {'FirstName': 'Joe',  'Age_In_Years': 40},
        {'FirstName': 'Mary', 'Age_In_Years': 35},
    ]
    >>> pretty_names(tbl)
    [
        {'First Name': 'Joe',  'Age In Years': 40},
        {'First Name': 'Mary', 'Age In Years': 35},
    ]
    >>> pretty_names(tbl, decamel, str.lower)
    [
        {'first_name': 'Joe',  'age_in_years': 40},
        {'first_name': 'Mary', 'age_in_years': 35},
    ]
    """
    if len(funcs) == 0:
        pretty = lambda string: tz.pipe(
            string,
            tz.partial(decamel, sep="_"),
            tz.partial(multichar, char="_", trim=True),
            lambda s: s.replace("_", " "),
        )
    else:
        pretty = lambda string: tz.pipe( string, *funcs)

    return [
        {pretty(k): v for k, v in row.items()}
        for row in data
    ]
