def _question_helper(txt) -> list:
    """txt"""

    _txt = txt.lower()
    res = []

    cands = ["court", "district", "tribunal", "federal"]

    for cand in cands:
        if cand in _txt:
            res.append(cand)

    return res


def _question_selector(key: str) -> list:
    """based on a key from _question helper find the list of good question to ask """

    res = []

    if "court" in key:  # court
        res.extend(
            [
                ("What is the court?", "who_court"),
            ]
        )
        return res

    if "district" in key:  # court
        res.extend(
            [
                ("What is the court?", "who_court"),
            ]
        )
        return res

    if "federal" in key:  # federal
        res.extend(
            [
                ("What is the court?", "who_court"),
            ]
        )
        return res

    if "tribunal" in key:  # tribunal
        res.extend(
            [
                ("What is the tribunal?", "who_court"),
            ]
        )

    return res