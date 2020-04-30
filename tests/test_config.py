from jedi_toolz.config import *

def test_as_dict():
    assert as_dict(example_ini()) == {
        "test1": {"value1": "5", "value2": "6"},
        "test2": {"valuea": "ABC", "valueb": "123"},
    }

test_as_dict()

def test_as_records():
    assert as_records(example_ini()) == [
        {"section": "test1", "option": "value1", "value": "5"},
        {"section": "test1", "option": "value2", "value": "6"},
        {"section": "test2", "option": "valuea", "value": "ABC"},
        {"section": "test2", "option": "valueb", "value": "123"},
    ]

def test_select():
    assert select("test1", config_path=example_ini()) == {"value1": "5", "value2": "6"}
    assert select("test1", "value2", config_path=example_ini()) == "6"