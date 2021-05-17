import tests.helpers


def list_has(value, lst):
    """search a value in a list, return a boolean True if found else False """

    return bool([1 for i in lst if i == value])