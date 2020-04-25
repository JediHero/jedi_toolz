from jedi_toolz.config import *

def test_as_dict():
    set_path(example_ini())
    assert as_dict() == {
        "test1": {"value1": "5", "value2": "6"},
        "test2": {"valuea": "ABC", "valueb": "123"},
    }

def test_as_records():
    set_path(example_ini())
    assert as_records() == [
        {"section": "test1", "option": "value1", "value": "5"},
        {"section": "test1", "option": "value2", "value": "6"},
        {"section": "test2", "option": "valuea", "value": "ABC"},
        {"section": "test2", "option": "valueb", "value": "123"},
    ]

def test_select():
    set_path(example_ini())
    assert select("test1") == {"value1": "5", "value2": "6"}
    assert select("test1", "value2") == "6"