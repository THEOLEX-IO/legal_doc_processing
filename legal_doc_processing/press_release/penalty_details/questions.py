from legal_doc_processing.utils import uniquize as _u


def _question_helper(txt):
    """txt"""

    _txt = txt.lower()
    res = list()

    k_list = ["require", "impose", "order", "pay", "forbid"]

    # for k in k_list:
    #     if k in _txt:
    #         res.append(k)

    res = [k for k in k_list if k in _txt]

    return res


def _question_selector(key: str):
    """based on a key from _question helper find the list of good question to ask """

    qs = list()

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

    return _u(qs)
