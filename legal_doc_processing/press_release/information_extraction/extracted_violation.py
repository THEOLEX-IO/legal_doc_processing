from legal_doc_processing.utils import uniquize as _u

from legal_doc_processing.utils import merge_ans, ask_all

from legal_doc_processing.press_release.clean.nature_of_violations import (
    _you_shall_not_pass,
    clean_ans,
)


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
                ("What is the violation?", "what_violation"),
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


def predict_extracted_violation(obj: dict, threshold=0.4, n_sents: int = 5) -> list:
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    # pers_org_entities_list
    pers_org_all = obj["pers_org_all"] + _u(_you_shall_not_pass(obj["pers_org_all"]))
    pers_org_all = _u(pers_org_all)

    # items
    h1, abstract = obj["h1"], obj["abstract"]
    abstract_sents = obj["abstract_sents"][:n_sents]
    ans = []

    # ask medhod h1
    for key_h1 in _question_helper(h1):
        # print(f"key_h1 : {key_h1} ")
        quest_pairs = _u(_question_selector(key_h1))
        # print(f"quest_pairs : {quest_pairs} ")
        ans.extend(ask_all(h1, quest_pairs, nlpipe=obj["nlpipe"]))

    # ask medhod abstract_sents
    for sent in abstract_sents:
        key_list = _question_helper(sent)
        for key in key_list:
            # print(key)
            quest_pairs = _u(_question_selector(key))
            # print(quest_pairs)
            ans.extend(ask_all(sent, quest_pairs, nlpipe=obj["nlpipe"]))

    # clean ans
    cleaned_ans = clean_ans(ans)
    answer_label = "new_answer"
    if not len(cleaned_ans):
        cleaned_ans = [{answer_label: "--None--", "score": -1}]

    # merge ans
    merged_ans = merge_ans(cleaned_ans, label=answer_label)

    # filert by spacy entities
    consitant_ans = [i for i in merged_ans if i[answer_label] not in pers_org_all]

    # filter by threshold
    flatten_ans = [(i[answer_label], i["cum_score"]) for i in consitant_ans]
    last_ans = [(i, j) for i, j in flatten_ans if j > threshold]

    return last_ans


if __name__ == "__main__":

    # import
    import time
    from legal_doc_processing.utils import get_pipeline, get_spacy
    from legal_doc_processing.press_release.loader import press_release_X_y
    from legal_doc_processing.press_release.press_release import PressRelease

    # laod
    nlpipe = get_pipeline()
    nlspa = get_spacy()
    nlspa.add_pipe("sentencizer")

    # structured_press_release_r
    df = press_release_X_y(features="defendant")
    df = df.iloc[:7, :]
    df["obj"] = [PressRelease(i, nlpipe=nlpipe, nlspa=nlspa) for i in df.txt.values]

    # preds
    t = time.time()
    # 28 objects --> 181 secondes so --> +/-10 secondes per objects
    df["pred_nature_of_violations"] = df.obj.apply(
        lambda i: i.predict("nature_of_violations")
    )
    t = time.time() - t

    # # labels
    # preds_labels = list(df.preds.iloc[0].keys())
    # for k in preds_labels:
    #     df["pred_" + k] = df.preds.apply(lambda i: i[k])

    # 1st one
    one = df.iloc[0, :]
    one_txt = one.txt
    one_ob = obj = self = one.obj