from typing import List, Dict, Any, Iterable, Union
import toolz.curried as tz
from enum import Enum, Flag, auto
from decorator import decorator
from datetime import datetime, date
try:
    import pandas
except ModuleNotFoundError:
    pandas = False

__all__ = (
    "has_pandas is_pandas is_record_value record_value "
    "is_record is_table TableType get_table_type "
    "to_table to_pandas"
).split()

RecordValue = Union[str, bool, int, float, date,
    datetime, None]
Record = Dict[str, RecordValue]
Table = Iterable[Record]

def has_all_attrs(obj: Any, attrs: str) -> bool:
    assert isinstance(attrs, str)
    return all([hasattr(obj, attr)
        for attr in attrs.split()])

def has_any_attrs(obj: Any, attrs: str) -> bool:
    assert isinstance(attrs, str)
    return any([hasattr(obj, attr) 
        for attr in attrs.split()])

def has_pandas() -> bool:
    return (True if pandas else False)

def is_pandas(data: Any) -> bool:
    assert data is not None
    attrs = (
        "values columns transpose head to_dict "
        "from_records"
    )
    if not has_pandas():
        return False
    elif has_all_attrs(data, attrs):
        return True
    else:
        return False

def is_record_value(value: Any) -> bool:
    test = isinstance(value, (str, bool, int, float, date,
        datetime))
    return test or value is None

def record_value(value: Any, use_repr: bool=False
    ) -> RecordValue:
    return (
        value if is_record_value(value) else
        str(value)
    )

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

def is_table(data: Any) -> bool:
    assert data is not None
    if is_pandas(data): return False
    attrs = "__iter__ __next__"
    if not has_any_attrs(data, attrs):
        return False
    first_row, _ = tz.peek(data)
    return is_record(first_row)

class TableType(Enum):
    NormalDict = auto()
    Record = auto()
    Table = auto()
    DataFrame = auto()

def get_table_type(data: Any) -> Union[TableType, None]:
    assert data is not None
    if is_pandas(data): return TableType.DataFrame
    if is_record(data): return TableType.Record
    if isinstance(data, dict): return TableType.NormalDict
    if is_table(data): return TableType.Table

def to_table(data: Any) -> Table:
    assert data is not None
    table_type = get_table_type(data)
    if table_type is TableType.Table:
        return data
    elif table_type is TableType.Record:
        return [{"column": k, "value": v}
            for k, v in data.items()]
    elif table_type is TableType.NormalDict:
        return [
            {"column": str(k), "value":
                record_value(v)}
            for k, v in data.items()
        ]
    elif table_type is TableType.DataFrame:
        records = data.to_dict("records")
        return [
            {str(k): v}
            for row in records
            for k, v in row.items()
        ]
    else:
        raise ValueError(
            "Value is None, must be a valide TableType.")

def to_pandas(data: Table):
    assert is_table(data) == True
    if has_pandas():
        return pandas.DataFrame.from_records(data)
    else:
        raise ModuleNotFoundError("pandas is not installed")

def handle_data(func, *args, **kwargs):
    orig = [arg for arg in args]
    data = to_table(orig[0])
    updated = [
        data if num == 0 else arg 
        for num, arg in enumerate(orig)
    ]
    return func(*updated, **kwargs)
