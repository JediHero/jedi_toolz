from jedi_toolz.data import (is_pandas, is_record_value, is_record,
    record_value, is_table, to_table, pretty_names)
from jedi_toolz.str_funcs import *
from datetime import datetime, date
import pandas

normal_dict = lambda: {5: "five"}
record1 = lambda: dict(FirstName="Joe", Age_in_Years=40)
record2 = lambda: dict(FirstName="Mary", Age_in_Years=35)
table = lambda: [record1(), record2()]
df = lambda: pandas.DataFrame.from_records(table())

def gen_table():
    for rec in table():
        yield rec

def test_is_pandas():
    assert is_pandas(table()) == False
    assert is_pandas(record1()) == False
    assert is_pandas(normal_dict()) == False
    assert is_pandas(df()) == True


def test_is_record_value():
    assert is_record_value(1) == True
    assert is_record_value(1.0) == True
    assert is_record_value(False) == True
    assert is_record_value("data") == True
    assert is_record_value(datetime.now()) == True
    assert is_record_value(date.today()) == True
    assert is_record_value(None) == True
    assert is_record_value(list("data")) == False
    assert is_record_value(
        dict(column="k", value="v")) == False
    assert is_record_value(tuple(["k", "v"])) == False

def test_record_value():
    assert record_value(None) == None
    assert record_value(5) == 5
    assert record_value(normal_dict()) == "{5: 'five'}"

def test_is_record():
    assert is_record(record1()) == True
    assert is_record(normal_dict()) == False
    assert is_record(5) == False

def test_is_table():
    assert is_table(table()) == True
    assert is_table(record1()) == False
    assert is_table(gen_table()) == True

def test_to_table():
    assert to_table(table()) == table()

    expected1 = [
        {"column": "FirstName", "value": "Joe"},
        {"column": "Age_in_Years", "value": 40}
    ]
    assert to_table(record1()) == expected1

    expected2 = [{"column": "5", "value": "five"}]
    assert to_table(normal_dict()) == expected2

def test_pretty_names():
    expected1 = [
        {"First Name": "Joe", "Age in Years": 40},
        {"First Name": "Mary", "Age in Years": 35},
    ]
    result1 = pretty_names(table())
    assert result1 == expected1
    expected2 = [
        {"first_name": "Joe", "age_in_years": 40},
        {"first_name": "Mary", "age_in_years": 35},
    ]
    result2 = pretty_names(table(), decamel,str.lower)
    assert result2 == expected2

    df = pandas.DataFrame.from_records(table())
    expected3 = [
        {"First Name": "Joe", "Age in Years": 40},
        {"First Name": "Mary", "Age in Years": 35},
    ]
    result3 = to_table(pretty_names(df))
    assert result3 == expected3