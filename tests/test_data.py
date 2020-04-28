from jedi_toolz.data import *
from datetime import datetime, date

def test_has_pandas():
    assert has_pandas() == False

def test_is_pandas():
    d = dict(column="five", value=5)
    assert is_pandas(d) == False

def test_is_record_value():
    assert is_record_value(1) == True
    assert is_record_value(1.0) == True
    assert is_record_value(False) == True
    assert is_record_value("data") == True
    assert is_record_value(datetime.now()) == True
    assert is_record_value(date.today()) == True
    assert is_record_value(None) == True
    assert is_record_value(list("data")) == False
    assert is_record_value(dict(column="k",
        value="v")) == False
    assert is_record_value(tuple(["k", "v"])) == False

def test_record_value():
    assert record_value(None) == None
    assert record_value(5) == 5
    d = dict(column="five", value=5)
    assert record_value(d) == "{'column': 'five', 'value': 5}"

def test_is_record():
    d1 = dict(column="five", value=5)
    assert is_record(d1) == True
    d2 = {5: "five"}
    assert is_record(d2) == False
    assert is_record(5) == False

def test_is_table():
    table = [
        dict(name="Joe", age=10),
        dict(name="Mary", age=None),
    ]
    assert is_table(table) == True

    record = dict(name="Joe", age=10)
    assert is_table(record) == False

def test_get_table_type():
    table = [
        dict(name="Joe", age=10),
        dict(name="Mary", age=None),
    ]
    assert get_table_type(table) is TableType.Table

    record = dict(name="Joe", age=10)
    assert get_table_type(record) is TableType.Record

    normal_dict = dict(name="Mary", age=tuple([1, 2]))
    assert get_table_type(normal_dict) is TableType.NormalDict

def test_to_table():
    table = [
        dict(name="Joe", age=10),
        dict(name="Mary", age=None),
    ]
    assert to_table(table) == table

    record = dict(name="Joe", age=10)
    assert to_table(record) == [
        dict(column="name", value="Joe"),
        dict(column="age", value=10)
    ]
    normal_dict = dict(name="Mary", age=tuple([1, 2]))
    assert to_table(normal_dict) == [
        dict(column="name", value="Mary"),
        dict(column="age", value="(1, 2)")
    ]