from jedi_toolz.str_funcs import *

tests = ["FirstName/Company", "  1stLien", "% Loans  ", "_Over/Under",
    "First Name", "FirstNameMD"]

def test_decamel():
    assert decamel("FirstNameMD") == "First_Name_MD"
    assert decamel("FirstNameMD", "|") == "First|Name|MD"

def test_invalid_first_char():
    assert invalid_first_char("1stLien") == "x1stLien"
    assert invalid_first_char("1stLien", "_") == "_1stLien"

def test_replace_non_word():
    assert replace_non_word("Over/Under") == "Over_Under"
    assert replace_non_word("Over/Under", "_and_") == "Over_and_Under"

def test_conseq_char():
    assert conseq_char("First___Name") == "First_Name"
    assert conseq_char("First  Name  ") == "First Name "
    assert conseq_char("First__Name__") == "First_Name_"
    assert conseq_char("FFirst_Name", "F") == "First_Name"

def test_trim():
    assert trim("  First Name ") == "First Name"
    assert trim("_First_Name_") == "First_Name"

def test_fmt_str():

    funcs = (
        decamel,
        invalid_first_char,
        replace_non_word,
        conseq_char,
        trim,
    )

    results1 = [fmt_str(test, *funcs) for test in tests]
    assert results1 == ['First_Name_Company', '1st_Lien', 'Loans', 'Over_Under',
        'First_Name', 'First_Name_MD']

    results2 = [fmt_str(test) for test in tests]
    assert results1 == results2

def test_fmt_attr_name():
    assert fmt_attr_name("FirstName") == "first_name"
    assert fmt_attr_name("_FirstName") == "first_name"
    assert fmt_attr_name("1stName") == "x1st_name"