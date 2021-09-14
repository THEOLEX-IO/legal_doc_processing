from legal_doc_processing.utils import uniquize as _u


_key_list = [
    "require",
    "impose",
    "order",
    "pay",
    "forbid",
    "aggre",
    "penalt",
    "ban",
    "cease",
]


def _question_helper(txt: str) -> list:
    """txt"""

    _txt = txt.lower()
    res = []

    res = [k for k in _key_list if k in _txt]

    return res


def _question_selector(key: str) -> list:
    """based on a key from _question helper find the list of good question to ask """

    qs = []

    if "cease" in key:
        qs.extend(
            [
                ("What have they to do ?", "what_cease"),
            ]
        )

    if "ban" in key:
        qs.extend(
            [
                ("What are they banned from?", "what_ban"),
                ("What is the ban?? ", "what_ban"),
            ]
        )

    if "penalt" in key:
        qs.extend(
            [
                ("What is the penalty?", "what_penalt"),
                ("What are the penalties? ", "what_penalt"),
            ]
        )

    if "aggre" in key:
        qs.extend(
            [
                ("What have they agreed?", "what_agreement"),
                ("What is the agreement? ", "what_agreement"),
            ]
        )
    if "require" in key:  # accused
        qs.extend(
            [
                ("What is required?", "what_acusation"),
                ("What is required to do? ", "what_acusation"),
            ]
        )
    if "impose" in key:
        qs.extend(
            [
                ("What is imposed?", "what_acusation"),
                ("What is imposed to do?", "what_acusation"),
            ]
        )
    if "forbid" in key:
        qs.extend(
            [
                ("What is forbidden?", "what_acusation"),
            ]
        )

    if "order" in key:
        qs.extend(
            [
                ("What is ordered?", "what_acusation"),
            ]
        )

    if "pay" in key:
        qs.extend(
            [
                ("What they have to pay? ", "what_acusation"),
            ]
        )
    if not key:
        qs.extend(
            [
                ("what is the injunction?", ""),
                ("they are ordered to do what?", ""),
                ("what have they to do?", ""),
                ("What is the sentence?", "what_payement"),
                ("What is the punition?", "what_payement"),
                ("What have they to do?", "what_payement"),
                ("What are their obligations?", "what_payement"),
                ("What is the condemnation ?", ""),
                ("What is forbidden?", ""),
                ("What is imposed?", ""),
            ]
        )
    qs = _u(qs)

    return qs


def _question_lister(key_list: list) -> list:
    """from key_list return question list """

    question_list = []
    for key in key_list:
        question_list.extend(_question_selector(key))

    return _u(question_list)