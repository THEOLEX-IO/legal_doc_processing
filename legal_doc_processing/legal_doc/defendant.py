import os
import copy

import pandas as pd

from legal_doc_processing.utils import (
    _if_not_pipe,
    _if_not_spacy,
    _ask,
    get_pers,
    get_orgs,
    get_pipeline,
)

from legal_doc_processing.legal_doc.utils import (
    get_entities_pers_orgs,
)

from legal_doc_processing.information_extraction.defendant import (
    _sub_you_shall_not_pass,
    _clean_ans,
)

from legal_doc_processing.information_extraction.utils import ask_all, merge_ans


def _question_helper(txt) -> list:
    """txt"""

    _txt = txt.lower()
    res = list()

    # defendant
    if "defendant" in _txt:
        res.append("defendant")
    # violated
    if "violate" in _txt:
        res.append("violate")

    return res


def _question_selector(key: str):
    """based on a key from _question helper find the list of good question to ask """

    res = list()

    # defendant
    if "defendant" in key:
        qs = [
            #
            ("Who is the defendant?", "who_defendant"),
            ("Who are the defendants?", "who_defendants"),
            ("what are the defendants?", "what_defendant"),
            ("what is the defendant?", "what_defendant"),
        ]
        res.extend(qs)

    elif "violate" in key:
        qs = [
            #
            ("Who is the violator?", "what_violator"),
            ("Who are the violators?", "what_violators"),
            ("What is the violator?", "what_violator"),
            ("What are the violators?", "what_violators"),
        ]
        res.extend(qs)
    else:
        qs = [
            #
            ("Who is the defendant?", "who_defendant"),
            ("Who are the defendants?", "who_defendants"),
            ("what are the defendants?", "what_defendant"),
            ("what is the defendant?", "what_defendant"),
            #
            ("Who is the violator?", "what_violator"),
            ("Who are the violators?", "what_violators"),
            ("What is the violator?", "what_violator"),
            ("What are the violators?", "what_violators"),
        ]
        res.extend(qs)

    return res


def predict_defendant(
    first_page: list,
    nlpipe=None,
    nlspa=None,
    pers_org_entities_list=None,
    threshold=0.4,
):
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    # pipe to avoid re init a pipe each time (+/- 15 -> 60 sec)
    # win lots of time if the method is used in a loop with 100 predictions
    nlpipe = _if_not_pipe(nlpipe)
    nlspa = _if_not_spacy(nlspa)
    nlspa.add_pipe("sentencizer")

    # pers_org_entities_list
    # we will use this one later to make a filter at the end
    if not pers_org_entities_list:
        pers_org_entities_list = get_entities_pers_orgs(first_page)
    pers_org_entities_list = _sub_you_shall_not_pass(pers_org_entities_list)

    # items
    # doc / sents / ans
    doc = nlspa(first_page)
    sents = [i for i in doc.sents]
    ans = []

    # ask method
    # for each sentence
    for sent in sents:
        # key list
        key_list = _question_helper(sent.text)
        for key in key_list:
            # from key to questions and from questions to answers
            quest_pairs = _question_selector(key)
            _ans = ask_all(sent.text, quest_pairs, nlpipe=nlpipe)
            ans.extend(_ans)

    # clean ans
    # ans is a list of dict, each dict has keys such as answer, score etc
    # for each answer we will clean this answer and create a new_answer more accurate
    cleaned_ans = _clean_ans(ans)

    # merge ans
    # based on new_answer we will make a groupby adding the scores for each new ans in a cumulative score
    # example [{new_ans : hello, score:0.3},{new_ans : hello, score:0.3}, ]
    # will become  [{new_ans : hello, score:0.6},]
    merged_ans = merge_ans(cleaned_ans, label="new_answer")

    # filert by spacy entities
    # we are sure that a personn or an org is NOT a violation so
    # if a prediction is in pers_org_entities_list, plz drop it
    consitant_ans = [i for i in merged_ans if i["new_answer"] in pers_org_entities_list]

    # filter by threshold
    # we need to filter the score above which we consider that no a signe score but a
    # cumulative score (much more strong, accurante and solid) will be droped
    consitant_ans = [(i["new_answer"], i["cum_score"]) for i in consitant_ans]
    last_ans = [(i, j) for i, j in consitant_ans if j > threshold]

    return last_ans


if __name__ == "__main__":

    # import
    from legal_doc_processing.utils import get_pipeline, get_spacy, get_orgs, get_pers
    from legal_doc_processing.legal_doc.loader import legal_doc_X_y
    from legal_doc_processing.legal_doc.structure import structure_legal_doc

    # laod
    nlpipe = get_pipeline()
    nlspa = get_spacy()
    nlspa.add_pipe("sentencizer")

    # structured_press_release_r
    df = legal_doc_X_y(features="defendant")
    df["struct_doc"] = df.txt.apply(lambda i: structure_legal_doc(i))
    df["header"] = df.struct_doc.apply(lambda i: i["header"])
    df["first_page"] = df.struct_doc.apply(lambda i: i["pages"][0])

    # test one
    one = df.iloc[0, :]
    one_struct = one.struct_doc
    first_page = one_first_page = one.first_page
    one_doc = nlspa(one_first_page)
