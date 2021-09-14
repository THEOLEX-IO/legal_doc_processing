def _question_helper(txt) -> list:
    """txt"""

    _txt = txt.lower()
    res = []

    cands = [
        # "impose",
        # "judgment",
        # "order",
        # "settl",
        # "defendant",
        # "charge",
        # "against",
        # "violate",
    ]

    for cand in cands:
        if cand in _txt:
            res.append(cand)

    return res


def _question_selector(key: str) -> list:
    """based on a key from _question helper find the list of good question to ask """

    res = []

    if "impose" in key:  # impose
        res.extend(
            [
                ("Who is imposed?", "who_imposed"),
                ("Who are imposed?", "who_imposed"),
                # ("what are the victims?", "what_victims"),
                # ("what is the victim?", "what_victim"),
            ]
        )
    if "judgment" in key:  # judgment
        res.extend(
            [
                ("Who is under judgment?", "who_judgment"),
                ("Who are under judgment?", "who_judgment"),
                ("Who is convicted", "who_convicted"),
                ("Who are convicted?", "who_convicted"),
                # ("what are the victims?", "what_victims"),
                # ("what is the victim?", "what_victim"),
            ]
        )

    if "order" in key:  # order
        res.extend(
            [
                ("Who is ordered", "who_judgment"),
                ("Who are ordered?", "who_judgment"),
                ("Who recieve an order?", "who_order"),
                # ("what are the victims?", "what_victims"),
                # ("what is the victim?", "what_victim"),
            ]
        )

    if "settl" in key:  # settl
        res.extend(
            [
                ("Who recieve a settlement", "who_settled"),
                # ("Who are settled?", "who_settled"),
                # ("Who recieve an order?", "who_order"),
                # ("what are the victims?", "what_victims"),
                # ("what is the victim?", "what_victim"),
            ]
        )

    if "defendant" in key:  # defendant
        res.extend(
            [
                ("Who is the defendant?", "who_defendant"),
                ("Who are the defendants?", "who_defendants"),
                ("What is the defendant?", "what_defendant"),
                ("What are the defendants?", "what_defendants"),
            ]
        )

    if "charge" in key:  # charge
        res.extend(
            [
                ("Who is charged", "who_charged"),
                ("Who are charged?", "who_charged"),
                # ("what are the victims?", "what_victims"),
                # ("what is the victim?", "what_victim"),
            ]
        )

    if "against" in key:  # against
        res.extend(
            [
                ("Who is the victim?", "who_victim"),
                ("Who are the victims?", "who_victims"),
                # ("what are the victims?", "what_victims"),
                # ("what is the victim?", "what_victim"),
            ]
        )

    if "defendant" in key:  # defendant
        res.extend(
            [
                ("Who is the defendant?", "who_defendant"),
                ("Who are the defendants?", "who_defendants"),
                # ("what are the defendants?", "what_defendant"),
                # ("what is the defendant?", "what_defendant"),
            ]
        )

    if "violate" in key:  # violated
        res.extend(
            [
                #
                ("Who is the violator?", "who_violator"),
                ("Who are the violators?", "who_violators"),
                ("What is the violator?", "what_violator"),
                ("What are the violators?", "what_violators"),
                ("Who has violated?", "who_violated"),
                ("Who made the violations?", "who_violation"),
            ]
        )

    return res