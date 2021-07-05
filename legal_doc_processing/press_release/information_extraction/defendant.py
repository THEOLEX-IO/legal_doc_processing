from legal_doc_processing.utils import uniquize as _u

from legal_doc_processing.utils import merge_ans, ask_all, cosine_similarity

from legal_doc_processing.press_release.clean.defendant import (
    _sub_you_shall_not_pass,
    clean_ans,
)


def _question_helper(txt) -> list:
    """txt"""

    _txt = txt.lower()
    res = list()

    cands = [
        "impose",
        "judgment",
        "order",
        "settl",
        "defendant",
        "charge",
        "against",
        "violate",
    ]

    for cand in cands:
        if cand in _txt:
            res.append(cand)

    return res


def _question_selector(key: str) -> list:
    """based on a key from _question helper find the list of good question to ask """

    res = list()

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


def predict_defendant(obj: dict, threshold: float = 0.4, n_sents: int = 3) -> list:
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    # pipe to avoid re init a pipe each time (+/- 15 -> 60 sec)
    nlpipe = obj["nlpipe"]

    # pers_org_entities_list
    pers_org_all = obj["pers_org_all"] + _u(_sub_you_shall_not_pass(obj["pers_org_all"]))
    pers_org_all = _u(pers_org_all)

    # judge
    judge_list = [i.strip().lower() for i in obj["feature_dict"]["judge"].split(",")]

    # items
    h1, abstract = obj["h1"], obj["abstract"]
    abstract_sents = obj["abstract_sents"][:n_sents]
    ans = []

    # ask medhod
    for key_h1 in _question_helper(h1):
        quest_pairs = _u(_question_selector(key_h1))
        ans.extend(ask_all(h1, quest_pairs, nlpipe=nlpipe))

    for sent in abstract_sents:
        key_list = _question_helper(sent)
        for key in key_list:
            quest_pairs = _u(_question_selector(key))
            ans.extend(ask_all(sent, quest_pairs, nlpipe=nlpipe))

    # clean ans
    cleaned_ans = clean_ans(ans)
    answer_label = "new_answer"
    if not len(cleaned_ans):
        cleaned_ans = [{answer_label: "--None--", "score": -1}]

    # merge ans
    merged_ans = merge_ans(cleaned_ans, label=answer_label)

    # filert by spacy entities
    consitant_ans = [i for i in merged_ans if i[answer_label] in pers_org_all]
    # exclude judge
    consitant_ans = [
        i for i in consitant_ans if (i[answer_label].strip().lower() not in judge_list)
    ]

    # filter by threshold
    flatten_ans = [(i[answer_label], i["cum_score"]) for i in consitant_ans]
    last_ans = [(i, j) for i, j in flatten_ans if j > threshold]

    return last_ans


if __name__ == "__main__":

    # import
    import time

    import numpy as np
    import pandas as pd

    from legal_doc_processing.utils import get_pipeline, get_spacy, cosine_similarity
    from legal_doc_processing.press_release.loader import press_release_X_y
    from legal_doc_processing.press_release.press_release import PressRelease

    # laod
    nlpipe = get_pipeline()
    nlspa = get_spacy()
    nlspa.add_pipe("sentencizer")

    # structured_press_release_r
    df = press_release_X_y(features="defendant")
    df = df.iloc[:30, :]
    df["obj"] = [PressRelease(i, nlpipe=nlpipe, nlspa=nlspa) for i in df.txt.values]

    # preds
    t = time.time()
    # 28 objects --> 181 secondes so --> +/-10 secondes per objects
    df["pred_defendant"] = df.obj.apply(lambda i: i.predict("defendant"))
    t = time.time() - t

    DF = pd.DataFrame(df)
    df = pd.DataFrame(DF)

    # eval predict defendant performance

    def decore_cosine_similarity(i: str, j: str) -> float:
        """cosine_similarity + avoid errors returning inconsistant cvalue"""

        try:
            return cosine_similarity(i, j)
        except Exception as e:
            print(e)
            return -1.0

    df["pred_defendant"] = df.obj.apply(lambda i: i.feature_dict["defendant"])

    _zip = zip(df.defendant.values, df.pred_defendant.values)
    pred_performance = pd.Series([decore_cosine_similarity(i, j) for i, j in _zip])
    pred_performance.mean()

    # # 1st one
    # one = df.iloc[0, :]
    # one_txt = one.txt
    # one_ob = obj = self = one.obj