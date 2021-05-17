import tests.helpers


def list_has(value, lst):
    """search a value in a list, return a boolean True if found else False """

    for val in lst:
        if val == value:
            return True
    return False
