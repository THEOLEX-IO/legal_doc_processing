from itertools import product

import pandas as pd

from legal_doc_processing.utils import (
    _if_not_spacy,
    _if_not_pipe,
    _ask,
    get_pers,
    get_orgs,
    get_label_,
)


def ask_all(txt, quest_pairs, nlpipe) -> list:
    """asl all questions and return a list of dict """

    # txt
    if not txt:
        raise AttributeError(f"Attribute error txt ; txt is {txt}, format {type(txt)}")

    # pipe
    nlpipe = _if_not_pipe(nlpipe)

    # ans
    ans = []

    # loop
    for quest, label in quest_pairs:
        ds = _ask(txt=txt, quest=quest, nlpipe=nlpipe)
        _ = [d.update({"question": label}) for d in ds]
        ans.extend(ds)

    # sort
    ans = sorted(ans, key=lambda i: i["score"], reverse=True)

    return ans


def merge_ans(ans, label="new_answer", threshold=0.1):
    """based on new_answer we will make a groupby adding the scores for each new ans in a cumulative score
    example [{new_ans : hello, score:0.3},{new_ans : hello, score:0.3}, ]
    will become  [{new_ans : hello, score:0.6},]"""

    # build dataframe
    df = pd.DataFrame(ans)

    # check
    if not label in df.columns:
        raise AttributeError(
            f"pb  label in df.columns --> label is {label } cols are {df.columns}"
        )

    # select
    droped = [i for i in df.columns if i not in ["score", label]]
    df = df.drop(droped, axis=1, inplace=False)

    # group by ans and make cumutavie score of accuracy
    ll = [
        {label: k, "cum_score": round(v.score.sum(), 2)}
        for k, v in df.groupby(label)
        if v.score.sum() > threshold
    ]
    ll = sorted(ll, key=lambda i: i["cum_score"], reverse=True)

    return ll