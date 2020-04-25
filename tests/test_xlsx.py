import jedi_toolz as jt
from jedi_toolz.xlsx import make_test_file
import openpyxl
import toolz.curried as tz

def get_number_formats(file, sheet_name, rows_to_review=100):
    wb = openpyxl.load_workbook(str(file), read_only=True)
    ws = wb[sheet_name]
    rows = ws.rows
    header = next(rows)
    names = [cell.value for cell in header]
    letters = [cell.column_letter for cell in header]
    return tz.pipe(
        rows,
        tz.take(rows_to_review),
        tz.map(lambda row: dict(zip(names, row))),
        tz.map(tz.valmap(tz.flip(getattr, "number_format"))),
        tz.merge_with(list),
        tz.valmap(tz.frequencies),
    )

def test_format_sheet():
    file = make_test_file()
    assert file.exists() == True
    before = get_number_formats(file, "Test 1")
    jt.xlsx.format_sheet(file, "Test 1")
    after = get_number_formats(file, "Test 1")
    for col in before:
        assert before[col] != after[col]
        if col in ["Order Date", "Close Date"]:
            assert "YYYY-MM-DD" in after[col]
        elif col in ["Balance", "Loan"]:
            assert "#,##0.00" in after[col]