# %%
from dataclasses import dataclass, field
from typing import Iterator, Any, Sequence, Mapping, NamedTuple, Union
import collections as cl
import toolz.curried as tz
from pathlib import Path

PathOrStr = Union[str, Path]

# %%
@dataclass
class Table(cl.abc.Iterator):
    rows: Iterator[Any]
    headers: Sequence[str]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]):
        pass

    @classmethod
    def from_records(cls, data: Sequence[Mapping[str, Any]]):
        pass

    @classmethod
    def from_namedtuple(cls, data: NamedTuple):
        pass

    @classmethod
    def from_csv(cls, path: PathOrStr):
        pass

    def __init__(self):
        return self

    def __next__(self):
        return next(self.rows)

    def as_records(self):
        values = self.__next()
        return {
        }

    def as_tuples(self):
        values = self.__next()
        headers = [header for header in self.headers]
        nam_tup = cl.namedtuple("Record", headers)
        return nam_tup(*values)
# %%
