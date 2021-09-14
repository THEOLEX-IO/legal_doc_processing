from legal_doc_processing.utils import uniquize as _u


def _question_helper(txt) -> list:
    """txt"""

    _txt = txt.lower()
    res = []

    cands = [
        "impose",
        "judgment",
        "order",
        "settl",
        "enters",
        "act",
    ]

    for cand in cands:
        if cand in _txt:
            res.append(cand)

    return res


def _question_selector(key: str) -> list:
    """based on a key from _question helper find the list of good question to ask """

    res = []

    if key in ["impose", "judgment", "order", "settl", "enters", "act"]:
        res.extend(
            [
                ("Who is the nature of the decision?", "nature"),
            ]
        )
    return res


def _question_lister(key_list: list) -> list:
    """from key_list return question list """

    question_list = []
    for key in key_list:
        question_list.extend(_question_selector(key))

    return _u(question_list)