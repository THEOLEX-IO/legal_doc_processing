import os

import pandas as pd

from legal_doc_processing.utils import (
    _if_not_pipe,
    _ask,
)


def _ask_all(txt, nlpipe) -> list:
    """asl all questions and return a list of dict """

    # pipe
    nlpipe = _if_not_pipe(nlpipe)

    # ans
    ans = []

    # question, funct
    quest_pairs = [
        ("Who is charged?", "ask_who_charged"),
        ("Who is the against?", "ask_who_against"),
        ("Who is the victim?", "ask_who_victim"),
        ("Who is the defendant?", "ask_who_defendant"),
        ("Who has violated?", "ask_who_violated"),
        ("Who has to pay?", "ask_who_pay"),
        ("Who is accused?", "ask_who_accused"),
    ]

    # loop
    for quest, label in quest_pairs:
        ds = _ask(txt=txt, quest=quest, nlpipe=nlpipe)
        _ = [d.update({"question": label}) for d in ds]
        ans.extend(ds)

    # sort
    ans = sorted(ans, key=lambda i: i["score"], reverse=True)

    # clean
    ans = [i for i in ans if (i["answer"].lower() != "defendants")]

    return ans


def _clean_ans(ans, threshold=0.5):
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


def predict_defendant(structured_legal_doc: list, nlpipe=None):
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    # pipe
    nlpipe = _if_not_pipe(nlpipe)

    # choose the item
    txt = structured_legal_doc["h1"]

    # ask all and get all possible response
    ans = _ask_all(txt, nlpipe)

    # group by ans, make cumulative sum of accuracy for eash ans and filter best ones
    ll = _clean_ans(ans)

    # reponse
    resp = ", ".join([i["answer"] for i in ll])

    return resp


if __name__ == "__main__":

    # import
    from legal_doc_processing.utils import *
    from legal_doc_processing.legal_doc.utils import *

    # from legal_doc_processing.legal_doc.segmentation.structure import (
    #     structure_legal_doc,
    # )

    # pipe
    nlpipe = get_pipeline()

    # structured_legal_doc_list
    legal_doc_txt_list = load_legal_doc_text_list()
    structured_legal_doc_list = [structure_legal_doc(i) for i in legal_doc_txt_list]

    # test one
    structured_legal_doc = structured_legal_doc_list[0]

    all_ans_h1 = _ask_all(structured_legal_doc["h1"], nlpipe)
    all_ans_h2 = _ask_all(structured_legal_doc["h2"], nlpipe)
    all_ans_article = _ask_all(structured_legal_doc["article"], nlpipe)

    ans = predict_defendant(structured_legal_doc, nlpipe)

    # test others
    ans_list = [predict_defendant(p, nlpipe) for p in structured_legal_doc_list]
    clean_ans_list = [[d["answer"] for d in ll] for ll in ans_list]
    clean_ans_list = [", ".join(ll) for ll in clean_ans_list]

# # import re
# # import pickle

# # import spacy
# # from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer
# from legal_doc_processing.utils import get_pipeline


# def ask_who_charged(first_page: list, nlpipe=None) -> str:
#     """from a list of text lines, create a pipelie if needed and asqk question """

#     # first_page_100 = [text for text in first_page if len(text) > 100]

#     # ask
#     ans = nlpipe(question="Who is charged?", context=txt, topk=3)

#     return ans


# def ask_who_accused(first_page: list, nlpipe=None) -> str:
#     """from a list of text lines, create a pipelie if needed and asqk question """

#     # ask
#     ans = nlpipe(question="Who is accused?", context=txt, topk=3)

#     return ans


# def ask_who_violated(first_page: list, nlpipe=None) -> str:
#     """from a list of text lines, create a pipelie if needed and asqk question """

#     # ask
#     ans = nlpipe(question="Who has violated?", context=txt, topk=3)

#     return ans


# def ask_who_pay(first_page: list, nlpipe=None) -> str:
#     """from a list of text lines, create a pipelie if needed and asqk question """

#     # ask
#     ans = nlpipe(question="Who has to pay?", context=txt, topk=3)

#     return ans


# def ask_who_defendant(first_page: list, nlpipe=None) -> str:
#     """from a list of text lines, create a pipelie if needed and asqk question """

#     # ask
#     ans = nlpipe(question="Who is the defendant?", context=txt, topk=3)

#     return ans


# def get_defendant(first_page: list, nlpipe=None) -> str:
#     """from a list of text lines, create a pipelie if needed and asqk question """

#     # ask
#     ans = nlpipe(question="Who is the defendant?", context=txt, topk=3)

#     return ans[0]["answer"]


# if __name__ == "__main__":

#     ans = []

#     funct_quest_pairs = [
#         (ask_who_charged, "ask_who_charged"),
#         (ask_who_defendant, "ask_who_defendant"),
#         (ask_who_violated, "ask_who_violated"),
#         (ask_who_pay, "ask_who_pay"),
#         (ask_who_accused, "ask_who_accused"),
#     ]

#     for funct, quest in funct_quest_pairs:
#         ds = funct(txt, ld.nlpipe)
#         _ = [d.update({"question": quest}) for d in ds]
#         ans.extend(ds)

#     ans = sorted(ans, key=lambda i: i["score"], reverse=True)
