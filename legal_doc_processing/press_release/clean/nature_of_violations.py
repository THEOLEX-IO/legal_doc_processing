def _clean_defendants(ans_list: list) -> list:
    """delete defenants """

    ans_list = [i for i in ans_list if (i.lower() != "defendants")]
    ans_list = [i for i in ans_list if (i.lower() != "defendant")]

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
        ans_list = [del_defendants(i, d) for i in ans_list]

    return ans_list


def _you_shall_not_pass(ans_list, defendants=True):
    """ """

    # strip
    ans_list = [i.strip() for i in ans_list]

    # clean defendants
    if defendants:
        ans_list = _clean_defendants(ans_list)

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
