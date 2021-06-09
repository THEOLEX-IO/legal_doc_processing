import os

import pandas as pd

from legal_doc_processing.utils import (
    _if_not_pipe,
    _ask,
)

from legal_doc_processing.press_release.information_extraction.utils import (
    product_juridic_form,
)


def _clean_LLC_trailling_dot_comma(txt: str) -> str:
    """ del LLC, Llc, LTD. etc etc"""

    # llc
    list_jur_form = product_juridic_form()
    for j in list_jur_form:
        txt = txt.replace(j, "")

    # trailling . or,
    txt = txt[:-1] if txt[-1] in [",", "."] else txt
    txt = txt[:-1] if txt[-1] in [",", "."] else txt

    return txt


def _clean_and(ans_list: list) -> list:
    """we want ['alex', 'cecile', 'alex and cecile' ]  became ['alex', 'cecile'] """

    l = list()
    for ans in ans_list:
        if " and " not in ans:
            l.append(ans)
        else:
            ll = ans.split(" and ")
            ll = [i.strip() for i in ll]
            ll = list(set(ll))
            l.extend(ll)

    l = list(set(l))
    return l


def _clean_resident(txt):
    """ """

    l = txt.split(" ")
    resident = [i for i, j in enumerate(l) if j.startswith("Resident")]
    # if not resident
    if len(resident) != 1:
        return txt
    # else
    l = l[resident[0] + 1 :]

    return " ".join(l)


def _sub_you_shall_not_pass(
    ans_list,
    defendants=True,
    too_long=True,
    too_short=True,
    _lower=True,
    _and=True,
    llc=True,
    resident=True,
):
    """ """

    # strip
    ans_list = [i.strip() for i in ans_list]

    # clean defendants
    if defendants:
        ans_list = [i for i in ans_list if (i.lower() != "defendants")]
        ans_list = [i for i in ans_list if (i.lower() != "defendant")]

    # duplicate
    ans_list = set(ans_list)

    # len to long
    if too_long:
        ans_list = [i for i in ans_list if len(i) < 60]

    if too_short:
        ans_list = [i for i in ans_list if len(i) > 3]

    # all lower
    if _lower:
        ans_list = [i for i in ans_list if i.lower() != i]

    # and
    if _and:
        ans_list = _clean_and(ans_list)

    # LLC
    if llc:
        ans_list = [_clean_LLC_trailling_dot_comma(i) for i in ans_list]

    # clean resident
    if resident:
        ans_list = [_clean_resident(i) for i in ans_list]

    ans_list = set(ans_list)

    return ans_list


def _you_shall_not_pass(ans_list):
    """ """

    # fiest clean
    _ans_list = _sub_you_shall_not_pass(ans_list)

    # sep with comma
    new_list = list()
    for ans in _ans_list:
        sub_l = ans.split(",")
        new_list.extend(sub_l)

    # reclean
    _new_list = _sub_you_shall_not_pass(new_list)

    return _new_list


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

    # # shall not pass
    # ans = _you_shall_not_pass(ans)

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
    txt = "\n".join(struct_doc["article"].split("\n")[0:1])
    ans_article = _ask_all(txt, nlpipe)

    # group by ans, make cumulative sum of accuracy for eash ans and filter best ones
    ans = ans_h1 + ans_article
    ll = _clean_ans(ans)

    # extract ans
    ll = [i["answer"] for i in ll]

    # guardian
    ll = _you_shall_not_pass(ll)

    # reponse
    resp = ",".join(ll)

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