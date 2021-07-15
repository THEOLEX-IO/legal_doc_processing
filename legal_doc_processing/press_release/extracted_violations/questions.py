def _question_helper(txt):
    """txt"""

    _txt = txt.lower()
    res = list()

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

    return res


def _question_selector(key: str):
    """based on a key from _question helper find the list of good question to ask """

    qs = list()

    if "accus" in key:  # accused
        qs.extend(
            [
                ("What is the accusation?", "what_acusation"),
                ("What are the accusations?", "what_acusations"),
                ("They are accused of what?", "accused_what"),
                ("It is accused of what?", "accused_what"),
                ("He is accused of what?", "accused_what"),
                ("What is the reason of the accusation?", "what_accusation"),
            ]
        )
    # charged
    elif "charge" in key:
        qs.extend(
            [
                ("What are the charges?", "what_charges"),
                ("What is the charge?", "what_charge"),
                ("they are charged of what?", "charged_what"),
                ("He is charged of what?", "charged_what"),
                # ("It is charged of what?", "charged_what"),
                ("For what are they charged?", "for_charged"),
                ("For what is he charged?", "for_charged"),
                ("For what is it charged?", "for_charged"),
            ]
        )

    if "violate" in key:  # violated
        qs.extend(
            [
                ("What are the violations?", "what_violations"),
                ("What is the violations?", "what_violation"),
                ("They have violated what?", "violated_what"),
                ("He has violated what?", "violated_what"),
                ("It has violated what?", "violated_what"),
                ("What have they violated?", "what_violated"),
                ("What has he violated?", "what_violated"),
                ("What has it violated?", "what_violated"),
            ]
        )

    if "judge" in key:  # judgement
        qs.extend(
            [
                ("What is the reason of the judgement?", "what_judge"),
                ("What are the reasons of the judgement?", "what_judge"),
                ("For what are they judge?", "for_what_judge"),
                ("For what are they under judgement?", "for_what_judge"),
                ("For what is he judge?", "for_what_judge"),
                ("For what is it under judgement?", "for_what_judge"),
                ("For what is he judge?", "for_what_judge"),
                ("For what is it under judgement?", "for_what_judge"),
                ("They are judged for what?", "for_what_judge"),
                ("They are under judgedment for what?", "for_what_judge"),
                ("He is judged for what?", "for_what_judge"),
                ("He is under judgedment for what?", "for_what_judge"),
                ("It is judged for what?", "for_what_judge"),
                ("It is under judgedment for what?", "for_what_judge"),
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
                ("For what is it imposed?", "for_imposed"),
            ]
        )
    if "pay" in key:  # pay
        qs.extend(
            [
                ("What is the reason of the payement?", "what_payement"),
                ("What are the reasons of the payement?", "what_payement"),
                ("For what have they to pay?", "for_pay"),
                ("For what has he to pay?", "for_pay"),
                ("For what has it to pay?", "for_pay"),
                ("What has he to pay for?", ""),
                ("What have they to pay for?", ""),
            ]
        )

    qs.extend(
        [
            ("What was the bad action?", "what_payement"),
            ("What is the bad action?", "what_payement"),
            ("What has he done wrong?", "what_payement"),
            ("What have they done wrong?", "what_payement"),
        ]
    )

    return qs