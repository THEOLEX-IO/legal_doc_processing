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
        ("Who make the charges?", "ask_who_charges"),
        ("Who ask something?", "ask_who_ask"),
        ("Who has order something?", "ask_who_has_order"),
        ("Who enter judgement against someone", "ask_who_enter_judgement"),
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


def predict_plaintiff(structured_press_release: list, nlpipe=None):
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    # choose the item
    h1 = structured_press_release["h1"]

    # ask all and get all possible response
    ans = _ask_all(h1, nlpipe)

    # group by ans, make cumulative sum of accuracy for eash ans and filter best ones
    ll = _clean_ans(ans)

    # reponse
    resp = ", ".join([i["answer"] for i in ll])

    return resp


if __name__ == "__main__":

    # import
    from legal_doc_processing.utils import *
    from legal_doc_processing.press_release.utils import *
    from legal_doc_processing.press_release.segmentation.structure import (
        structure_press_release,
    )

    # pipe
    nlpipe = get_pipeline()

    # structured_press_release_list
    press_txt_list = load_press_release_text_list()
    structured_press_release_list = [structure_press_release(i) for i in press_txt_list]

    # test one
    structured_press_release = structured_press_release_list[0]

    all_ans_h1 = _ask_all(structured_press_release["h1"], nlpipe)
    all_ans_h2 = _ask_all(structured_press_release["h2"], nlpipe)
    all_ans_article = _ask_all(structured_press_release["article"], nlpipe)

    ans = predict_plaintiff(structured_press_release, nlpipe)

    # test others
    ans_list = [predict_plaintiff(p, nlpipe) for p in structured_press_release_list]
    clean_ans_list = [[d["answer"] for d in ll] for ll in ans_list]
    clean_ans_list = [", ".join(ll) for ll in clean_ans_list]
