from typing import List, Dict, Any, Iterable
import toolz.curried as tz
from enum import Enum, Flag

Record = Dict[str, Any]
Table = Iterable[Record]

class TableType(Enum):
    Record = 1
    NestedDict = 2
    IterableOfRecords = 3
    DataFrame = 4\

def is_table(data) -> bool:
    iter_attrs = "__iter__ __next__"
    iter_test = [hasattr(data, attr) for attr in iter_attrs.split()]
    if not any(iter_test):
        return False
    rec_attrs = "keys values items"
    rec = next(iter(data))
    rec_test = [hasattr(rec, attr) for attr in rec_attrs.split()]
    if all(rec_test):
        return True
    else:
        return False

def has_pandas():
    try:
        import pandas
        return True
    except ModuleNotFoundError:
        return False 
        
def is_pandas(data):
    attrs = "values columns transpose head to_dict from_records"
    if not has_pandas():
        return False
    elif all([hasattr(data, attr) for atr in attrs.split()]):
        return True
    else:
        return False
