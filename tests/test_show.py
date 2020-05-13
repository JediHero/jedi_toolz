from jedi_toolz.show import show, wrap_row, wrap_table, transpose

normal_dict = lambda: {5: "five"}
record1 = lambda: dict(name="Joe", age=10,
    text="Some long text here and there")
record2 = lambda: dict(name="Joe", age=10,
    text="This should be wrapped so it is easier to see")
table = lambda: [record1(), record2()]

def test_wrap_row():
    assert wrap_row(record1(), 10) == {'name': 'Joe', 'age': '10',
        'text': 'Some long\ntext here\nand there'}

def test_wrap_table():
    assert wrap_table(table(), 10) == [
        {'name': 'Joe', 'age': '10',
            'text': 'Some long\ntext here\nand there'},
        {'name': 'Joe', 'age': '10',
            'text': 'This\nshould be\nwrapped so\nit is\neasier to\nsee'}
    ]

def test_transpose():
    expected1 = [
        {'column': 'name', 'row 1': 'Joe', 'row 2': 'Joe'},
        {'column': 'age', 'row 1': 10, 'row 2': 10},
        {'column': 'text',
            'row 1': 'Some long text here and there',
            'row 2': 'This should be wrapped so it is easier to see'}
    ]
    assert transpose(table()) == expected1

    expected2 = [
        {'column': 'column', 'row 1': 'name', 'row 2': 'age', 'row 3': 'text'},
        {'column': 'value', 'row 1': 'Joe', 'row 2': 10,
            'row 3': 'Some long text here and there'}
    ]
    assert transpose(record1()) == expected2

def test_show():
    expected1 = (
        "╒══════════╤════════════════╕\n"
        "│ column   │ value          │\n"
        "╞══════════╪════════════════╡\n"
        "│ name     │ Joe            │\n"
        "├──────────┼────────────────┤\n"
        "│ age      │ 10             │\n"
        "├──────────┼────────────────┤\n"
        "│ text     │ Some long text │\n"
        "│          │ here and there │\n"
        "╘══════════╧════════════════╛"
    )
    print(expected1)
    result1 = show(record1(), print_out=False)
    print(result1)
    assert result1 == expected1

    expected2 = (
        "╒════════╤═══════╤════════════════╕\n"
        "│ name   │   age │ text           │\n"
        "╞════════╪═══════╪════════════════╡\n"
        "│ Joe    │    10 │ Some long text │\n"
        "│        │       │ here and there │\n"
        "├────────┼───────┼────────────────┤\n"
        "│ Joe    │    10 │ This should be │\n"
        "│        │       │ wrapped so it  │\n"
        "│        │       │ is easier to   │\n"
        "│        │       │ see            │\n"
        "╘════════╧═══════╧════════════════╛"
    )
    print(expected2)
    result2 = show(table(), print_out=False)
    print(result2)
    assert result2 == expected2