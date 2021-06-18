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

from legal_doc_processing.press_release.utils import (
    product_juridic_form,
)
from legal_doc_processing.press_release.utils import get_entities_pers_orgs


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


def _clean_resident(txt: str) -> str:
    """delete resident """

    l = txt.split(" ")
    resident = [i for i, j in enumerate(l) if j.startswith("Resident")]
    # if not resident
    if len(resident) != 1:
        return txt
    # else
    l = l[resident[0] + 1 :]

    return " ".join(l)


def _clean_defendants(ans_list: list) -> list:
    """delete defenants """

    ans_list = [i for i in ans_list if (i.lower() != "defendants")]
    ans_list = [i for i in ans_list if (i.lower() != "defendant")]

    del_defendants = lambda i, defendant: i.strip().replace(defendant, "").strip()

    defendant_list = ["Defendants", "Defendant", "defendant", "defendants"]

    for d in defendant_list:
        ans_list = [del_defendants(i, d) for i in ans_list]

    return ans_list


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
    """welcome in the rocky horror picture function
    here we are gonna take an list of text and make a bunch of horrible but
    working cleaning operation.
    the goal is to make each answer more -generic- to make merge more easy and to avoid a list of
    very close but slicely  different answer
    example ["alex", "Alex", "Alex LLC", "Alex LLC and paul"] become ["alex", "paul"]"""

    # strip
    ans_list = [i.strip() for i in ans_list]

    # clean defendants
    if defendants:
        ans_list = _clean_defendants(ans_list)

    # dummy words
    forbiden = [
        "Judge",
        "Civil Monetary Penalty",
        "Anti-Money Laundering",
        "Swap Reporting Violations",
        "Commodity Industry",
        "Personal Expenses",
        "Commodity Futures",
        "Commodity Exchange ",
        "CFTC",
        "U.S. District Court",
        "Commodity Exchange",
        "an Unregistered",
        "Swap Dealer",
        "Commodity Trading",
        "Commodity Pool ",
    ]

    for f in forbiden:
        ans_list = [i for i in ans_list if (f.lower() not in i.lower())]

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
    """make _sub_shall_not_pass twice due to the -and- problem :
    ["alex and paul",] should become become ["alex", paul"]
    if so we need to clean twice"""

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


def _clean_ans(ans):
    """ans is a list of dict. each dict is  : {answer:"foo", score:0.32}.
    for each dict,  add and _id and a new_ans based on the _you_shall_not_pass method
    the _you_shall_not_pass method is able to ditect:
     - completly inconsistant answer, if so the answer is droped
     - not so consistant answer, or non uniformized answer, if so the new_answer is the -more generic-
     version of ansxer "
     last but not least, and answer could be 'foo and bar' but this is indeed 2 answers
     'foo' and 'bar'. In this case we will create from one dict 2 dicts with same properties but separate
     new_ans
     before ans is a list of one dict -> [{answer:"foo and bar", score :0.123456},]
     after ans is a list of 2 dicts ->   [{new_answer:'foo', answer:"foo and bar", score :0.123456},
                                         {new_answer:'bar', answer:"foo and bar", score :0.123456}]"""

    # ans = copy.deepcopy(ans)

    # clean ans
    _ = [d.update({"_id": i}) for i, d in enumerate(ans)]
    _ = [d.update({"new_answer": _you_shall_not_pass([d["answer"]])}) for d in ans]

    new_ans = list()
    for i, d in enumerate(ans):
        if len(d["new_answer"]) == 0:
            # ans.pop(i)
            pass
        if len(d["new_answer"]) == 1:
            # d["new_answer"] = list(d["new_answer"])[0]
            new_ans.append(
                {
                    "_id": d["_id"],
                    "question": d["question"],
                    "start": d["start"],
                    "end": d["end"],
                    "score": d["score"],
                    "answer": d["answer"],
                    "new_answer": list(d["new_answer"])[0],
                }
            )
            # ans.pop(i)
        if len(d["new_answer"]) > 1:
            l = [
                {
                    "_id": d["_id"],
                    "question": d["question"],
                    "start": d["start"],
                    "end": d["end"],
                    "score": d["score"],
                    "answer": d["answer"],
                    "new_answer": k,
                }
                for k in d["new_answer"]
            ]
            new_ans.extend(l)
            # ans.pop(i)

    return new_ans
