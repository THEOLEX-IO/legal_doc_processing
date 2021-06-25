from legal_doc_processing.press_release.utils import product_juridiction_pairs


def _filter_jur(token, cands: list = None):
    """ """

    if not cands:
        cands = product_juridiction_pairs()

    for k, v in cands.items():
        if token.lower().strip() == k.lower().strip():
            return v.upper()

    return ""


def _filter_the(txt: str) -> str:
    """ """

    if txt.lower().strip().startswith("the"):
        txt = txt[3:].strip()

    return txt


def _sub_shall_not_pass(txt) -> str:
    """ """

    txt = _filter_the(txt)

    txt = _filter_jur(txt)

    if (len(txt) < 3) or (len(txt) > 24):
        txt = ""

    return txt


def _you_shall_not_pass(txt: str) -> list:
    """ """

    txt = _sub_shall_not_pass(txt)

    if not txt:
        return []

    return [txt]


def clean_ans(ans):
    """ """

    # clean ans
    _ = [d.update({"_id": i}) for i, d in enumerate(ans)]
    _ = [d.update({"new_answer": _you_shall_not_pass(d["answer"])}) for d in ans]

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
                    "new_answer": d["new_answer"][0],
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
