"""jedi_toolz is a python package containing many utilities to simplify working
with data.

jedi_toolz is divided into the following sub-modules:

config: Provides helper functions to extract the contents of a .ini
configuration file.

data: Provides many helper functions for checking the type of data passed and
converting dict objects to tables and record objects.

domo: Connects to a DOMO instance using credentials defined in a .ini config
file and provides several helper functions.

show: Provides several functions for printing tabular data. Utilized the
tabulate package.

xlsx: Provides functions for exporting and formatting data in a .xlsx file. Uses
openpyxl to export and read data.

str_funcs: Provides utility functions for format strings primarily used as column
names into valid or prettier formats by adding or removing underscores,
spaces, etc.
"""

from jedi_toolz import config
from jedi_toolz.show import *
from jedi_toolz.xlsx import *
from jedi_toolz import domo
from jedi_toolz.data import *
from jedi_toolz.str_funcs import *