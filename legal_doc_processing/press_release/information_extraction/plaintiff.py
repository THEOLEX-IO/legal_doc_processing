import os

# import re
# import pickle

# import spacy
# from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer

from legal_doc_processing.utils import get_pipeline

import pandas as pd


def _ask(txt: str, quest: str, nlpipe, topk: int = 3) -> list:

    return nlpipe(question=quest, context=txt, topk=3)


def _ask_all(txt, nlpipe) -> list:
    """asl all questions and return a list of dict """

    # ans
    ans = []

    # question, funct
    quest_pairs = [
        ("Who is the plaintiff?", "ask_who_plaintiff"),
        ("Who make the charges?", "ask_who_charges"),
        ("Who make the order?", "ask_who_order"),
        ("Who enter judgement against someone", "ask_who_enter_judgement"),
    ]

    # loop
    for quest, label in quest_pairs:
        ds = _ask(txt=txt, quest=quest, nlpipe=nlpipe)
        _ = [d.update({"question": label}) for d in ds]
        ans.extend(ds)

    # sort
    ans = sorted(ans, key=lambda i: i["score"], reverse=True)

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


def predict_plaintiff(structured_press_release: list, nlpipe=None):
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    # pipe
    if not nlpipe:
        nlpipe = get_pipeline()

    # choose the item
    txt = press_release_1st["h1"]

    # ask all and get all possible response
    ans = _ask_all(txt, nlpipe)

    # group by ans, make cumulative sum of accuracy for eash ans and filter best ones
    ll = _clean_ans(ans)

    return ll


if __name__ == "__main__":

    # import
    from legal_doc_processing.utils import *
    from legal_doc_processing.press_release.segmentation.structure import (
        structure_press_release,
    )

    # file list
    folder_list = os.listdir("./data/files")
    files_list = [
        [
            f"./data/files/{f}/{i}"
            for i in os.listdir(f"./data/files/{f}")
            if ("press" in i) and ("txt" in i)
        ]
        for f in folder_list
    ]
    files_list = [i[0] for i in files_list]

    # structure all press release
    press_txt_list = [load_data(i) for i in files_list]
    press_release_list = [structure_press_release(i) for i in press_txt_list]

    # test one
    press_release_1st = press_release_list[0]
    ans = predict_plaintiff(press_release_1st)

    # test others
    ans_list = [predict_plaintiff(p) for p in press_release_list]
    clean_ans_list = [[d["answer"] for d in ll] for ll in ans_list]
    clean_ans_list = [", ".join(ll) for ll in clean_ans_list]
