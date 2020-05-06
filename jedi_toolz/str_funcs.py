import re
from toolz.curried import pipe, curry
from datetime import date
from typing import Callable

__all__ = (
    "today_str resub decamel invalid_first_char replace_non_word "
    "conseq_char trim fmt_str".split()
)
def today_str(pattern: str="%Y-%m-%d"):
    """Formats Today's Date as a string given a strftime pattern."""
    return date.today().strftime(pattern)

@curry
def resub(pat: str, repl: str, string: str):
    """curried version of re.sub. Used to build up several string
    replacements into a single function. See fmt_str.
    """
    return re.sub(pat, repl, string)

@curry
def decamel(string: str, replace_char: str="_") -> str:
    """Adds a sep character to a camelCase string.
    >>> decamel('FirstNameMD')
    'First_Name_MD'
    """
    return resub("(?<=[a-z])(?P<match>[A-Z])",
        f"{replace_char}\g<match>", string)

@curry
def invalid_first_char(string: str, append_char: str="x") -> str:
    """Appends an valid character invalid characters at the start of a string.
    >>> invalid_first_char('1stLien')
    'x1stLien'
    """
    return resub("(?P<match>^[0-9])", f"{append_char}\g<match>", string)

@curry
def replace_non_word(string: str, replace_char:str="_") -> str:
    """Replaces any character that is not a-z or A-Z or 0-9 or _
    with the replace_char.
    >>> replace_non_word('Over/Under')
    'Over_Under'
    >>> replace_non_word('% Total')
    '__Total'
    """
    return resub("\W", f"{replace_char}", string)

@curry
def conseq_char(string: str, chars: str="_ ") -> str:
    """Replaces consecutive characters with a single character.
    >>> conseq_char('First__Name___MD')
    'First_Name_MD'
    """
    result = string
    for char in chars:
        result = resub(f"{char}+", f"{char}", result)
    return result

@curry
def trim(string: str, char: str="[\s_]") -> str:
    """Replaces characters at the beginning and end of string.
    By default will replace white space and "_" characters.
    >>> trim('_First_Name_')
    'First_Name'
    >>> trim(' first name   ')
    'first name'
    """
    return resub(f"^{char}+|{char}+$", "", string)

# If this is changed, update the doc string for fmt_str
FMT_STR_COLUMN_FORMATS = (decamel, invalid_first_char, replace_non_word,
    conseq_char, trim)

FMT_STR_PRETTY_COLUMN_FORMATS = (decamel, invalid_first_char, replace_non_word,
    conseq_char, trim, resub("_", " "))

FMT_STR_ATTR_FORMATS = (decamel, invalid_first_char, replace_non_word,
    conseq_char)

StrFunc = Callable[[str],str]

def fmt_str(string, *funcs: StrFunc) -> str:
    """Applies a series of functions to string. By default, uses the
    FMT_STR_COLUMN_FORMATS tuple which contains the following functions which are
    applied in order:
    1. decamel
    2. invalid_first_char
    3. replace_non_word
    4. conseq_char
    5. trim

    tests = ["  1stLien", "% Loans  ", "_Over/Under", "First Name", "FirstNameMD"]...
    >>> fmt_str('  1stLien')
    '1st_Lien'
    >>> fmt_str('% Loans  ')
    'Loans'
    >>> fmt_str('_Over/Under')
    'Over_Under'
    >>> fmt_str('First Name')
    'First_Name'
    >>> fmt_str('FirstNameMD')
    'First_Name_MD'

    User can provide own list of funcs instead of the defaults.
    However, each func must accept only 1 arg. funcs are applied from
    left to right.

    >>> fmt_str('FirstName/Company', decamel, replace_non_word, str.lower)
    'first_name_company'
    """
    if len(funcs) == 0:
        return pipe(string, *FMT_STR_COLUMN_FORMATS)
    else:
        return pipe(string, *funcs)