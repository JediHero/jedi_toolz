import re
from functools import reduce, partial as prtl

def compose(*funcs):
    """
    def f(x): pass
    def g(x): pass
    compose(g, f)(x) == g(f(x))
    """
    return reduce(
        lambda f, g: lambda x: f(g(x)), 
        tuple(reversed(funcs)), 
        lambda x: x
    )

def pipe(obj, *funcs):
    """
    def f(x): pass
    def g(x): pass
    pipe(x, f, g) = g(f(x))
    """
    func = compose(*funcs)
    return func(obj)

def valmap(func, d):
    return {k: func(v) for k, v in d.items()}

def keymap(func, d):
    return {func(k): v for k, v in d.items()}

def merge(base_d, *d):
    if len(d) == 0: return base_d
    if len(d) > 0: 
        return reduce(lambda acc, x: {**(acc or {}), **x}, d)

def seq(*values):
    assert len(values) > 0, "Must provide at list 1 value"
    if len(values) > 1:
        return tuple(*values)
    elif isinstance(values[0], (list, tuple)):
        return values[0]
    elif isinstance(values[0], dict):
        return tuple(k for k in values[0])
    elif isinstance(values[0], str):
        return [values[0]]
    else:
        values[0]
        

invalid = "[\s_.-]"
pipe(
    # raw text
    " .CamelCase that-isOK  ",
    # decamel
    prtl(re.sub, "(?<=[a-z])(?P<match>[A-Z])", "_\g<match>"),
    # trim
    prtl(re.sub, f"^{invalid}+|{invalid}+$", ""),
    # replace invalid with "_"
    prtl(re.sub, f"{invalid}", "_"),    
    # lower case
    str.lower,
    # capitalize case
    prtl(re.sub, "case", "CASE"),
)