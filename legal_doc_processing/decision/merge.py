import pandas as pd


def _merge_ans(list_ans, threshold=0.1):
    """based on new_answer we will make a groupby adding the scores for each new ans in a cumulative score
    example [{new_ans : hello, score:0.3},{new_ans : hello, score:0.3}, ]
    will become  [{new_ans : hello, score:0.6},]"""

    if len(list_ans) == 0:
        return [("--None--", -1)]
    elif len(list_ans) == 1:
        return list_ans

    # build dataframe
    dict_ans = [{"answer": i, "score": j} for i, j in list_ans]
    df = pd.DataFrame(dict_ans)
    df = df.loc[:, ["score", "answer"]]

    # group by ans and make cumutavie score of accuracy
    ll = [
        {"answer": k, "cum_score": round(v.score.sum(), 2)}
        for k, v in df.groupby("answer")
        if v.score.sum() > threshold
    ]
    ll = sorted(ll, key=lambda i: i["cum_score"], reverse=True)

    return ll