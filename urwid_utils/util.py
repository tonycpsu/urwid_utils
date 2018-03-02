# -*- coding: utf-8 -*-

import re

CONST_NAME_CRE = re.compile(r'^[A-Z][A-Z0-9_]+$')

def is_valid_identifier(name):
    """Pedantic yet imperfect. Test to see if "name" is a valid python identifier
    """
    if not isinstance(name, str):
        return False
    if '\n' in name:
        return False
    if name.strip() != name:
        return False
    try:
        code = compile('\n{0}=None'.format(name), filename='<string>', mode='single')
        exec(code)
        return True
    except SyntaxError:
        return False


def get_const_identifiers(*args):
    dargs = []
    for arg in args:
        try:
            dargs.append(dict(arg))
        except TypeError:
            dargs.append(vars(arg))

    const = {}
    for item in dargs:
        for name, value in item.items():
            if not CONST_NAME_CRE.match(name):
                continue
            if not is_valid_identifier(name):
                continue
            const[name] = value

    return const
