import os

import pandas as pd

from legal_doc_processing.utils import (
    _if_not_pipe,
    _ask,
)


#################################################################################################

# # LLC
# def _clean_LLC_trailling_dot_comma(txt):
#     list_com = [
#         "Inc.",
#         "inc.",
#         "inc",
#         "LLC",
#         " Ltd.",
#         " Ltd",
#         "LTD",
#     ]
#     del_suffix = lambda txt, suff: " ".join([k for k in txt.split(" ") if k != suff])
#     del_trailing_point_comma = (
#         lambda txt: txt.strip()
#         if txt.strip()[-1] not in [".", ","]
#         else txt.strip()[:-1].strip()
#     )

#     for k in list_com:
#         txt = del_suffix(txt, k)
#     for i in range(2):
#         txt = del_trailing_point_comma(txt)

#     return txt


def _you_shall_not_pass(ans_list):
    """ """

    # clean
    ans_list = [i for i in ans_list if (i["answer"].lower() != "defendants")]
    ans_list = [i for i in ans_list if (i["answer"].lower() != "defendant")]

    # len
    ans_list = [i for i in ans_list if len(i["answer"]) < 50]

    return ans_list


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

    # shall not pass
    ans = _you_shall_not_pass(ans)

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


def predict_defendant(struct_doc: list, nlpipe=None):
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    # pipe
    nlpipe = _if_not_pipe(nlpipe)

    # ask h1
    ans_h1 = _ask_all(struct_doc["h1"], nlpipe)

    # ask article 3st lines
    txt = "\n".join(struct_doc["article"].split("\n")[0:2])
    ans_article = _ask_all(txt, nlpipe)

    # group by ans, make cumulative sum of accuracy for eash ans and filter best ones
    ans = ans_h1 + ans_article
    ll = _clean_ans(ans)

    # reponse
    resp = ", ".join([i["answer"] for i in ll])

    return resp


if __name__ == "__main__":

    # import
    from legal_doc_processing.utils import get_pipeline
    from legal_doc_processing.press_release.utils import press_release_X_y
    from legal_doc_processing.press_release.segmentation.structure import (
        structure_press_release,
    )

    # pipe
    nlpipe = get_pipeline()

    # structured_press_release_r
    df = press_release_X_y(features="defendant")
    df["structured_txt"] = [structure_press_release(i) for i in df.txt.values]

    # one
    defendant = df.defendant.iloc[0]
    one_text = df.txt.iloc[0]
    one_struct = df["structured_txt"].iloc[0]
    pred = predict_defendant(one_struct, nlpipe)
    print(f" {'y'.rjust(80)} -->  {'pred'} \n")
    print(160 * "-")
    print(f" {defendant.rjust(80)} -->  {pred[:60]} \n")

    # 1 to 20
    print(f" {'y'.rjust(80)} -->  {'pred'} \n")
    print(160 * "-")
    for i in range(1, 20):
        defendant = df.defendant.iloc[i]
        i_text = df.txt.iloc[i]
        i_struct = df["structured_txt"].iloc[i]
        pred = predict_defendant(i_struct, nlpipe)
        print(f" {defendant.rjust(80)} -->  {pred[:60]} \n")