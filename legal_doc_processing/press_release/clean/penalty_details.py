def _clean_violation(txt: str) -> str:
    """ """

    viol_list = ["misuse", "misusing", "cftc", " cea ", "(cea)"]

    for viol in viol_list:
        if viol in txt:
            return ""

    return txt


def _force_at_least_2_tokens(txt: str) -> str:
    """ """

    if not " " in txt:
        return ""

    return txt


def _force_good_verbs(txt):
    """ """

    good_verbs = [
        "pay",
        "ceas",
        "ban",
        "freez",
        "preserv",
        "penalt",
        "disgord",
        "ban",
    ]

    one_of_them = [1 for i in good_verbs if i in txt]
    if not sum(one_of_them):
        return ""

    return txt


def _clean_str_to_str(txt: str) -> str:
    """ """

    txt = txt.lower().strip()
    txt = _clean_violation(txt)
    txt = _force_at_least_2_tokens(txt)
    txt = _force_good_verbs(txt)
    txt = txt.lower().strip()

    return txt


def _clean_list_to_list(ans_list: list, clean_str=_clean_str_to_str) -> list:
    """ """

    ans_list = [clean_str(i) for i in ans_list if i.strip()]

    return ans_list


def clean_ans(ans, clean_str=_clean_str_to_str, clean_list=_clean_list_to_list):
    """ """

    # ans = copy.deepcopy(ans)

    # clean ans
    _ = [d.update({"_id": i}) for i, d in enumerate(ans)]
    _ = [d.update({"new_answer": _clean_list_to_list([d["answer"]])}) for d in ans]

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
