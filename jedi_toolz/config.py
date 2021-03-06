# AUTOGENERATED! DO NOT EDIT! File to edit: config.ipynb (unless otherwise specified).

__all__ = "set_path as_dict as_records select example_ini".split()

# Internal Cell
from configparser import ConfigParser
import os
from pathlib import Path
from typing import Dict, List, Optional, Union

environ = "JEDI_TOOLZ_PATH"

PathOrStr = Optional[Union[str,Path]]

def set_path(config_path: PathOrStr=None) -> Path:
    """Returns the path to the jedi_toolz.ini file or the path
    to the config_path.ini file.
    """
    if config_path:
        return Path(config_path).expanduser()
    elif os.getenv(environ):
        return Path(os.getenv(environ)).expanduser()
    else:
        raise ValueError(
            f"Either {environ} environment variable must exist "
            "or config_path must be provided."
        )


def as_dict(config_path: PathOrStr=None) -> Dict[str,str]:
    """Returns configurations as a nested dict. Keys and values are strings."""
    location = set_path(config_path)
    cfg = ConfigParser()
    cfg.read(location)
    sections = cfg.sections()
    result = {}
    for section in sections:
        options = {k: v for k, v in cfg[section].items()}
        result[section] = options
    return result

def as_records(config_path: PathOrStr=None) -> List[Dict[str,str]]:
    """Returns configurations as a list of dicts."""
    return [
        {"section": section, "option": option, "value": value}
        for section, options in as_dict(config_path).items()
        for option, value in options.items()
    ]

def select(section: str, option: Optional[str]=None, config_path: PathOrStr=None) -> Union[Dict[str, str], str]:
    """Returns the configuration a nested dict or value."""
    settings = as_dict(config_path)
    if option:
        return settings[section][option]
    else:
        return settings[section]

def example_ini():
    """Creates an example.ini file and returns it's path."""
    path = Path.cwd() / "tests/example.ini"
    with path.open(mode="w") as file:
        file.writelines([
            "[test1]\n",
            "value1 = 5\n",
            "value2 = 6\n",
            "\n",
            "[test2]\n",
            "valuea = ABC\n",
            "valueb = 123\n",
        ])
    return path