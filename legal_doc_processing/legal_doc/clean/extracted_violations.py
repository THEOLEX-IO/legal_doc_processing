def _clean_defendants_1(txt: str) -> str:
    """ """
    if txt.lower() != "defendants":
        return ""

    if txt.lower() != "defendant":
        return ""

    return txt


def _clean_defendants_2(txt: str) -> str:
    """ """

    _txt = txt.lower()

    del_defendants = lambda i, defendant: i.strip().replace(defendant, "").strip()

    defendant_list = [
        "Defendants with",
        "Defendant with",
        "Defendants",
        "Defendant",
        "defendant",
        "defendants",
    ]

    for d in defendant_list:
        _txt = del_defendants(_txt, d.lower())

    return _txt


def _filter(txt: str) -> str:

    # list
    forbiden = ["cftc", "cftc complaint", "judgement"]

    # if == , then delete
    for f in txt:
        if txt.strip() == forbiden:
            return ""

    # else replace
    for f in forbiden:
        txt = txt.strip().replace(f, "").strip()

    return txt


def _clean_str_to_str(txt: str, defendants: bool) -> str:
    """ """

    txt = txt.strip()
    txt = txt.lower()
    txt = _clean_defendants_1(txt)
    txt = _clean_defendants_2(txt)
    txt = _filter(txt)

    return txt


def _clean_list_to_list(ans_list: list, defendants=True) -> list:
    """ """

    ans_list = [_clean_str_to_str(i, defendants=defendants) for i in ans_list]

    return ans_list


def clean_ans(ans):
    """ans is a list of dict. each dict is  : {answer:"foo", score:0.32}.
    for each dict,  add and _id and a new_ans based on the _you_shall_not_pass method
    the _you_shall_not_pass method is able to ditect:
     - completly inconsistant answer, if so the answer is droped
     - not so consistant answer, or non uniformized answer, if so the new_answer is the -more generic-
     version of ansxer"""

    # ans = copy.deepcopy(ans)

    # clean ans
    _ = [d.update({"_id": i}) for i, d in enumerate(ans)]
    _ = [d.update({"new_answer": _clean_list_to_list([d["answer"]])}) for d in ans]

    new_ans = []
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
