def _clean_on(txt: str) -> str:
    """ """

    _txt = txt.lower().strip()

    if _txt.startswith("on "):
        return _txt.replace("on ", "").strip().lower()

    return txt


def _clean_the_present(txt: str) -> str:
    """ """

    _txt = txt.lower().strip()
    if _txt == "present":
        return ""

    if "the present" in _txt:
        return ""

    return txt


def _strip_trailling_comma_dot(txt: str) -> str:
    """ """

    if not len(txt):
        return ""

    if txt[0] in [",", "."]:
        txt = txt[1:]

    if txt[-1] in [",", "."]:
        txt = txt[:-1]

    txt = txt.strip()

    return txt


def _sub_shall_not_pass(txt: str) -> str:
    """ """

    txt = txt.lower().strip()

    txt = _clean_on(txt)

    txt = _clean_the_present(txt)

    txt = _strip_trailling_comma_dot(txt)

    if (len(txt) < 3) or (len(txt) > 24):
        txt = ""

    return txt


def _you_shall_not_pass(txt: str) -> list:
    """ """

    txt = _sub_shall_not_pass(txt)

    if not txt:
        return []

    return [txt]


def clean_ans(ans: list) -> list:
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
    _ = [d.update({"new_answer": _you_shall_not_pass(d["answer"])}) for d in ans]

    new_ans = list()
    for i, d in enumerate(ans):
        if len(d["new_answer"]) == 0:
            # ans.pop(i)
            pass
        elif len(d["new_answer"]) == 1:
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
        elif len(d["new_answer"]) > 1:
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
