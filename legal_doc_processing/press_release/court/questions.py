def _question_helper(txt) -> list:
    """txt"""

    _txt = txt.lower()
    res = list()

    cands = [
        "court",
        "district",
        "tribunal",
    ]

    for cand in cands:
        if cand in _txt:
            res.append(cand)

    return res


def _question_selector(key: str) -> list:
    """based on a key from _question helper find the list of good question to ask """

    res = list()

    if "court" in key:  # court
        res.extend(
            [
                ("What is the court?", "who_court"),
            ]
        )

    return res