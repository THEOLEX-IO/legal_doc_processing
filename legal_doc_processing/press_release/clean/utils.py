def _clean_str_to_str(txt: str) -> str:
    """ """

    return str


def _clean_list_to_list(ans_list: list, clean_str=_clean_str_to_str) -> list:
    """ """

    ans_list = [clean_str(i) for i in ans_list if i.strip()]

    return ans_list


def clean_ans(ans, clean_str=_clean_str_to_str, clean_list=_clean_list_to_list):
    """ """

    # ans = copy.deepcopy(ans)

    # clean ans
    _ = [d.update({"_id": i}) for i, d in enumerate(ans)]
    _ = [d.update({"new_answer": clean_list([d["answer"]], clean_str)}) for d in ans]

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
