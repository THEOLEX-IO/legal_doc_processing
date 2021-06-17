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


def _get_entities_pers_orgs(txt: dict, n_paragraphs: int = 2, nlpspa=None) -> list:
    """get entities PERSON and ORG from h1 and sub_article """

    # TODO
    # THIS ONE SHOULD BE REFACTORED AND USED IN UTILS

    nlpspa = _if_not_spacy(nlpspa)

    # all pers all orgs from spacy entities
    all_pers = get_pers(txt, nlpspa)
    all_orgs = get_orgs(txt, nlpspa)
    pers_org_entities_list = all_pers + all_orgs

    return pers_org_entities_list


def _ask_all(txt, nlpipe) -> list:
    """asl all questions and return a list of dict """

    # txt
    if not txt:
        raise AttributeError(f"Attribute error txt ; txt is {txt}, format {type(txt)}")

    # pipe
    nlpipe = _if_not_pipe(nlpipe)

    # ans
    ans = []

    # question, funct
    quest_pairs = [
        ("Who are the defendants?", "who_defendant"),
        ("Who is the defendant?", "who_defendant"),
        # ("Who is charged?", "ask_who_charged"),
        # ("Who is the against?", "ask_who_against"),
        # ("Who is the victim?", "ask_who_victim"),
        # ("Who is the defendant?", "ask_who_defendant"),
        # ("Who violated?", "ask_who_violated"),
        # # ("Who has to pay?", "ask_who_pay"),
        # ("Who is accused?", "ask_who_accused"),
    ]

    # loop
    for quest, label in quest_pairs:
        ds = _ask(txt=txt, quest=quest, nlpipe=nlpipe)
        _ = [d.update({"question": label}) for d in ds]
        ans.extend(ds)

    # sort
    ans = sorted(ans, key=lambda i: i["score"], reverse=True)

    # clean manuals
    ans = [i for i in ans if (i["answer"].lower() != "defendants")]
    ans = [i for i in ans if (i["answer"].lower() != "cftc")]

    return ans


def _clean_ans(ans, threshold=0.00):
    """ """

    # build dataframe
    df = pd.DataFrame(ans)
    df = df.loc[:, ["score", "answer"]]

    # group by ans and make cumutavie score of accuracy
    ll = [
        {"answer": k, "cum_score": v.score.sum()}
        for k, v in df.groupby("answer")
        if v.score.sum() > threshold
    ]
    ll = sorted(ll, key=lambda i: i["cum_score"], reverse=True)

    return ll


def predict_defendant(
    first_page: list, nlpipe=None, nlspa=None, pers_org_entities_list=None
):
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    # pipe to avoid re init a pipe each time (+/- 15 -> 60 sec)
    # win lots of time if the method is used in a loop with 100 predictions
    nlpipe = _if_not_pipe(nlpipe)
    nlspa = _if_not_spacy(nlspa)
    nlspa.add_pipe("sentencizer")

    # doc / sents / ans
    doc = nlspa(first_page)
    sents = [i for i in doc.sents]
    ans = []

    # defendant
    def_sents = [i for i in sents if "defendant" in i.text.lower()]
    for sen in def_sents:
        ans.extend(_ask_all(sen.text, nlpipe=nlpipe))

    # pers_org_entities_list
    # we will use this one later to make a filter at the end
    if not pers_org_entities_list:
        pers_org_entities_list = _get_entities_pers_orgs(first_page)

    # # ask all and get all possible response
    # ans = _ask_all(txt, nlpipe)

    # # group by ans, make cumulative sum of accuracy for eash ans and filter best ones
    # ll = _clean_ans(ans)

    # # reponse
    # resp = ", ".join([i["answer"] for i in ll])

    # return resp

    return "-- None --"


if __name__ == "__main__":

    # import
    from legal_doc_processing.utils import get_pipeline, get_spacy, get_orgs, get_pers
    from legal_doc_processing.legal_doc.utils import legal_doc_X_y
    from legal_doc_processing.legal_doc.segmentation.clean import clean_doc, alex_clean
    from legal_doc_processing.legal_doc.segmentation.structure import (
        structure_legal_doc,
    )

    # laod
    nlpipe = get_pipeline()
    nlpspa = get_spacy()
    nlpspa.add_pipe("sentencizer")

    # structured_press_release_r
    df = legal_doc_X_y(features="defendant")
    df["struct_doc"] = df.txt.apply(lambda i: alex_clean(i))
    df["header"] = df.struct_doc.apply(lambda i: i["header"])
    df["first_page"] = df.struct_doc.apply(lambda i: i["pages"][0])

    # test one
    one = df.iloc[0, :]
    one_struct = one.struct_doc
    first_page = one_first_page = one.first_page
    one_doc = nlpspa(one_first_page)

    sents = [i for i in one_doc.sents]
    sents = [i.text for i in sents]
    sents = [
        (
            i.replace("\n.", "$$$$")
            .replace("\n", " ")
            .replace("  ", " ")
            .replace("  ", " ")
            .replace("$$$$", "\n")
        )
        for i in sents
    ]

    sents = " ".join(sents)

    one_doc = nlpspa(sents)
    sents = [i for i in one_doc.sents]

    def_sents = [i for i in sents if "defendant" in i.text.lower()]

    ans_0 = _ask_all(def_sents[0].text, nlpipe=nlpipe)
    ans_1 = _ask_all(def_sents[1].text, nlpipe=nlpipe)