from legal_doc_processing.utils import uniquize as _u


def _question_helper(txt):
    """txt"""

    _txt = txt.lower()
    res = list()

    # involving

    if "involving" in _txt:
        res.append("involving")

    # failed
    if "failed to" in _txt:
        res.append("failed")

    # settle
    if "settle" in _txt:
        res.append("settle")

    # accused
    if ("accuse" in _txt) and ("for" in _txt):
        res.append("accused_for")
    if ("accuse" in _txt) and ("of" in _txt):
        res.append("accused_of")

    # charges
    if ("charg" in _txt) and ("for" in _txt):
        res.append("charged_for")
    if ("charg" in _txt) and ("with" in _txt):
        res.append("charged_with")

    # violated
    if ("violat" in _txt) and ("by" in _txt):
        res.append("violated_by")
    if ("allege" and "violate") in _txt:
        res.append("violated_by")

    # judge
    if ("judgment" in _txt) and ("for" in _txt):
        res.append("judgment_for")
    if ("judgment" in _txt) and ("in" in _txt):
        res.append("judgment_in")

    # order
    if ("order" in _txt) and ("from" in _txt):
        res.append("order_from")
    if ("order" in _txt) and ("for" in _txt):
        res.append("order_for")

    # impose
    if ("impose" in _txt) and ("for" in _txt):
        res.append("impose_for")

    # pay
    if ("pay" in _txt) and ("for" in _txt):
        res.append("pay_for")

    # allege
    if "allege" in _txt:
        res.append("allege")

    # suit
    if ("suit" and "against") in _txt:
        res.append("suit")

    return res


def _question_selector(key: str):
    """based on a key from _question helper find the list of good question to ask """

    qs = list()

    if "involving" in key:
        qs.extend(
            [
                ("What is involved?", "what_involved?"),
            ]
        )
    if "failed" in key:
        qs.extend(
            [
                ("What have they failed to do?", "what_failed"),
            ]
        )

    if "settle" in key:
        qs.extend(
            [
                ("What are the reason of the settlement?", "what_settlement"),
                # ("They are accused of what?", "accused_what"),
                # ("What is the reason of the accusation?", "what_accusation"),
            ]
        )
    if "allege" in key:  # accused
        qs.extend(
            [
                ("What are the allegations?", "what_acusation"),
                ("What is alleged?", "what_acusation"),
                # ("They are accused of what?", "accused_what"),
                # ("What is the reason of the accusation?", "what_accusation"),
            ]
        )

    if "accus" in key:  # accused
        qs.extend(
            [
                ("What is the accusation?", "what_acusation"),
                ("They are accused of what?", "accused_what"),
                ("What is the reason of the accusation?", "what_accusation"),
            ]
        )
    # charged
    elif "charge" in key:
        qs.extend(
            [
                ("What are the charges?", "what_charges"),
                ("For what are they charged?", "for_charged"),
                ("For what is he charged?", "for_charged"),
                ("For what is it charged?", "for_charged"),
            ]
        )

    if "suit" in key:
        qs.extend(
            [
                ("What are the violations?", "what_violations"),
                ("what are the reason of the persuit? ", "what_suit"),
            ]
        )

    if "violate" in key:  # violated
        qs.extend(
            [
                ("What are the violations?", "what_violations"),
                # ("They have violated what?", "violated_what"),
                # ("He has violated what?", "violated_what"),
                # ("It has violated what?", "violated_what"),
                ("What have they violated?", "what_violated"),
                ("What has he violated?", "what_violated"),
                ("What has it violated?", "what_violated"),
            ]
        )

    if "judge" in key:  # judgement
        qs.extend(
            [
                # ("What is the reason of the judgement?", "what_judge"),
                ("What are the reasons of the judgement?", "what_judge"),
                ("For what are they judged?", "for_what_judge"),
                ("For what are they under judgement?", "for_what_judge"),
                ("For what is he judge?", "for_what_judge"),
                # ("For what is it under judgement?", "for_what_judge"),
                # ("For what is he judge?", "for_what_judge"),
                # ("For what is it under judgement?", "for_what_judge"),
                # ("They are judged for what?", "for_what_judge"),
                # ("They are under judgedment for what?", "for_what_judge"),
                # ("He is judged for what?", "for_what_judge"),
                # ("He is under judgedment for what?", "for_what_judge"),
                # ("It is judged for what?", "for_what_judge"),
                # ("It is under judgedment for what?", "for_what_judge"),
            ]
        )

    if "order" in key:  # order
        qs.extend(
            [
                ("What is the reason of the order?", "what_judge"),
                ("What are the reasons of the order?", "what_judge"),
            ]
        )
    if "impose" in key:  # impose
        qs.extend(
            [
                ("What is the reason of the imposition?", "what_impose"),
                ("What are the reasons of the imposition?", "what_impose"),
                ("For what are they imposed?", "for_imposed"),
                ("For what is he imposed?", "for_imposed"),
                # ("For what is it imposed?", "for_imposed"),
            ]
        )
    if "pay" in key:  # pay
        qs.extend(
            [
                # ("What is the reason of the payement?", "what_payement"),
                # ("What are the reasons of the payement?", "what_payement"),
                ("What is the reason of the sanction ? ", "what_pay"),
                ("What are the violations? ", "what_pay")
                # ("What has he to pay for?", ""),
                # ("What have they to pay for?", ""),
            ]
        )

    if not qs:
        qs.extend(
            [
                ("What was the bad action?", "what_payement"),
                ("What is the bad action?", "what_payement"),
                ("What has he done wrong?", "what_payement"),
                ("What have they done wrong?", "what_payement"),
            ]
        )

    return qs


def _question_lister(key_list: list) -> list:
    """from key_list return question list """

    question_list = []
    for key in key_list:
        question_list.extend(_question_selector(key))

    return _u(question_list)