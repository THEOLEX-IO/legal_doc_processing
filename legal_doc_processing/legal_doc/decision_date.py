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
    get_label_,
)

from legal_doc_processing.legal_doc.decision_date_clean import cleaned_ans

# from legal_doc_processing.legal_doc.utils import (
#     get_entities_pers_orgs,
# )

# from legal_doc_processing.legal_doc.extracted_authorities_clean import clean_ans

# from legal_doc_processing.legal_doc.defendant_clean import (
#     _sub_you_shall_not_pass,
# )

from legal_doc_processing.information_extraction.utils import ask_all, merge_ans


def _question_helper(txt) -> list:
    """txt"""

    _txt = txt.lower()
    res = list()

    # reason
    if "violate" in _txt.lower():
        res.append("viloate")
    # filed
    if "filed" in _txt.lower():
        res.append("filed")
    # filed
    if "filled" in _txt.lower():
        res.append("filed")

    return res


def _question_selector(key: str):
    """based on a key from _question helper find the list of good question to ask """

    res = list()

    # reason
    if "violate" in key:
        qs = [
            #
            ("When was the violation?", "when_violation"),
            ("When did the violation take place ?", "when_violation"),
            ("When did the violations take place ?", "when_violations"),
        ]
        res.extend(qs)

    # reason
    if "filed" in key:
        qs = [
            #
            ("When was filed a compliant?", "when_violation"),
            ("When was the compliant filed?", "when_violation"),
            ("When were the compliants filed?", "when_violations"),
        ]
        res.extend(qs)

    return res


def _you_shall_not_pass(date):
    """avoid passing for a studid algo """

    # validation funct
    funct = lambda i: True if str(i) in date else False

    # features to validate
    features = [(range(1979, 2023), "years"), (range(1, 32), "day")]

    # if a feature not in date retunr --None--
    for feat, _ in features:
        is_ok = bool(sum([funct(i) for i in feat]))
        if not is_ok:
            return "--None--"

    return date


def predict_decision_date(
    first_page: list,
    nlpipe=None,
    nlspa=None,
    threshold=0.2,
):

    # pipe to avoid re init a pipe each time (+/- 15 -> 60 sec)
    # win lots of time if the method is used in a loop with 100 predictions
    nlpipe = _if_not_pipe(nlpipe)
    nlspa = _if_not_spacy(nlspa)
    try:
        nlspa.add_pipe("sentencizer")
    except Exception as e:
        print(e)

    # items
    # doc / sents / ans
    doc = nlspa(first_page)
    sents = [i for i in doc.sents]
    ans = []

    # ALL DATES
    first_paragraphs = " ".join([i.text for i in sents[:6]])
    all_dates = get_label_(first_paragraphs, "DATE", None)

    # ask method
    # for each sentence
    for sent in sents:
        print(sent)
        # key list
        key_list = _question_helper(sent.text)
        for key in key_list:
            print(key)
            # from key to questions and from questions to answers
            quest_pairs = _question_selector(key)
            _ans = ask_all(sent.text, quest_pairs, nlpipe=nlpipe)
            ans.extend(_ans)

    # clean ans
    # ans is a list of dict, each dict has keys such as answer, score etc
    # for each answer we will clean this answer and create a new_answer more accurate
    cleaned_ans = clean_ans(ans)
    answer_label = "new_answer"
    if not len(cleaned_ans):
        cleaned_ans = [{answer_label: "--None--", "score": -1}]

    # merge ans
    # based on new_answer we will make a groupby adding the scores for each new ans in a cumulative score
    # example [{new_ans : hello, score:0.3},{new_ans : hello, score:0.3}, ]
    # will become  [{new_ans : hello, score:0.6},]
    merged_ans = merge_ans(cleaned_ans, label=answer_label)

    # filert by spacy entities
    # we are sure that a personn or an org is NOT a violation so
    # if a prediction is in pers_org_entities_list, plz drop it
    # consitant_ans = [i for i in merged_ans if i[answer_label] in pers_org_entities_list]

    # filter by threshold
    # we need to filter the score above which we consider that no a signe score but a
    # cumulative score (much more strong, accurante and solid) will be droped
    flatten_ans = [(i[answer_label], i["cum_score"]) for i in merged_ans]
    last_ans = [(i, j) for i, j in flatten_ans if j > threshold]

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
    threshold = 0.2

    # structured_press_release_r
    df = legal_doc_X_y()
    df["struct_doc"] = df.txt.apply(lambda i: structure_legal_doc(i))
    df["header"] = df.struct_doc.apply(lambda i: i["header"])
    df["first_page"] = df.struct_doc.apply(lambda i: i["pages"][0])

    # test one
    one = df.iloc[1, :]
    struct_doc, one_struct = one.struct_doc
    first_page = one_first_page = one.first_page
    one_doc = nlspa(one_first_page)

    # pred = predict_extracted_authorities(first_page, nlpipe=nlpipe)
