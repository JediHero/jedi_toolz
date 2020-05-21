import jedi_toolz as jt
from jedi_toolz.xlsx import Formats, get_cell_attrs
import openpyxl
import toolz.curried as tz
from pathlib import Path
from random import choice, randint, random
from datetime import date
from dateutil.relativedelta import relativedelta as delta

names = (
    "Joe Nancy Harry Gus David Max Matt Nicole Tracy Stacy "
    "Kristi Kelly Mike James"
)
texts = (
    "Univeristy Franklin End_Game Tower New_York_Mets Last_Dance Movies Donald_Trump "
    "Nation_Captial COVID-19 Honesty Some_Really_Long_Text The_Lord_of_the_Rings"
)
flag = lambda: True if randint(1, 10) < 10 else False
text = lambda: choice([val.replace("_", " ") for val in texts.split()]) if flag() else None
name = lambda: choice(names.split())
dt = lambda: date.today() + delta(days=randint(-30, 30)) if flag() else None
amt = lambda: randint(150_000, 350_000) * random()

gen_data = lambda n=100: [
    {
        "Order Date": dt(),
        "Close Date": dt(),
        "Name": name(),
        "Dept": text(),
        "Balance": amt(),
        "Loan": amt(),
    }
    for row in range(n)
]


def test_to_xlsx():
    file = Path.cwd() / "tests/test.xlsx"
    if file.exists(): file.unlink()
    assert not file.exists()

    jt.to_xlsx(gen_data(100), file, "to_xlsx 1", over_write=True)
    jt.to_xlsx(
        gen_data(100),
        file,
        "to_xlsx 2",
        jt.ColumnFormat("Loan", "#,##0"),
        jt.ColumnFormat("Order Date", "mm/dd/yyyy"),
        over_write=False
    )
    wb = openpyxl.load_workbook(file, read_only=True)
    assert ["to_xlsx 1", "to_xlsx 2"] == wb.sheetnames

    rows = 100
    freq = lambda fmt: {fmt: rows}
    attr_rows = "number_format", rows
    result2 = get_cell_attrs(file, "to_xlsx 2", *attr_rows)
    expected2 = {
        "Order Date": freq("mm/dd/yyyy"),
        "Close Date": freq("yyyy-mm-dd"),
        "Name": freq(""),
        "Dept": freq(""),
        "Balance": freq("#,##0.00"),
        "Loan": freq("#,##0"),
    }
    assert result2 == expected2

    if file.exists(): file.unlink()
    assert not file.exists()

def make_test_file(tests: int=3) -> Path:
    """Makes a test .xlsx file used for testing."""
    file = Path.cwd() / "tests/test.xlsx"
    data = gen_data(100)
    for test in range(1, tests + 1):
        over_write = True if test == 1 else False
        jt.to_xlsx(data, file, f"Test {test}", over_write=over_write)
    return file


def test_patterns():
    file = make_test_file(3)
    formats = {
        k: v.number_format
        for k, v in Formats.from_sheet(file, "Test 1").to_dict().items()
    }
    expected = {
        "Order Date": "yyyy-mm-dd",
        "Close Date": "yyyy-mm-dd",
        "Name": "",
        "Dept": "",
        "Balance": "#,##0.00",
        "Loan": "#,##0.00",
    }
    assert formats == expected

    user_defined = jt.ColumnFormat("Loan", "#,##0")
    u_formats = {
        k: v.number_format
        for k, v in Formats.from_user(file, "Test 2", user_defined)
            .to_dict().items()
    }
    u_expected = {
        k: ("#,##0" if k == "Loan" else v)
        for k, v in expected.items()
    }
    assert u_formats == u_expected

    wildcard = jt.ColumnFormat("*Date", "mm/dd/yyyy")
    w_formats = {
        k: v.number_format
        for k, v in Formats.from_user(file, "Test 3", wildcard)
            .to_dict().items()
    }
    w_expected = {
        k: ("mm/dd/yyyy" if "Date" in k else v)
        for k, v in expected.items()
    }
    assert w_formats == w_expected


def test_format_sheet():
    file = make_test_file(2)
    assert file.exists() == True

    rows = 100
    freq = lambda fmt: {fmt: rows}
    attr_rows = "number_format", rows

    file_sheet = file, "Test 1"
    jt.format_sheet(*file_sheet)
    result1 = get_cell_attrs(*file_sheet, *attr_rows)
    expected1 = {
        "Order Date": freq("yyyy-mm-dd"),
        "Close Date": freq("yyyy-mm-dd"),
        "Name": freq(""),
        "Dept": freq(""),
        "Balance": freq("#,##0.00"),
        "Loan": freq("#,##0.00"),
    }
    assert result1 == expected1

    file_sheet = file, "Test 2"
    jt.format_sheet(
        *file_sheet,
        jt.ColumnFormat("Loan", "#,##0"),
        jt.ColumnFormat("Order Date", "mm/dd/yyyy"),
    )
    result2 = get_cell_attrs(*file_sheet, *attr_rows)
    expected2 = {
        "Order Date": freq("mm/dd/yyyy"),
        "Close Date": freq("yyyy-mm-dd"),
        "Name": freq(""),
        "Dept": freq(""),
        "Balance": freq("#,##0.00"),
        "Loan": freq("#,##0"),
    }
    assert result2 == expected2

    file.unlink()
    assert not file.exists()