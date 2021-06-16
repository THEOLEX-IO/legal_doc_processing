import pandas as pd


from legal_doc_processing.utils import (
    _if_not_pipe,
    _if_not_spacy,
    _ask,
    get_pers,
    get_orgs,
    get_pipeline,
)


def _get_entities_pers_orgs(struct_doc: dict, n_paragraphs: int = 2, nlpspa=None) -> list:
    """get entities PERSON and ORG from h1 and sub_article """

    nlpspa = _if_not_spacy(nlpspa)

    # sub article
    sub_article = "\n".join(struct_doc["article"].split("\n")[:n_paragraphs])

    # all pers all orgs from spacy entities
    all_pers = get_pers(struct_doc["h1"], nlpspa) + get_pers(sub_article, nlpspa)
    all_orgs = get_orgs(struct_doc["h1"], nlpspa) + get_orgs(sub_article, nlpspa)
    pers_org_entities_list = all_pers + all_orgs

    # clean
    # pers_org_entities_list = _sub_you_shall_not_pass(pers_org_entities_list)

    return pers_org_entities_list


def _question_helper(txt):
    """txt"""

    # accused
    if ("accuse" in txt) and ("for" in txt):
        return "accused_for"
    elif ("accuse" in txt) and ("of" in txt):
        return "acused_of"
    # charges
    elif ("charg" in txt) and ("for" in txt):
        return "charged_for"
    elif ("charg" in txt) and ("with" in txt):
        return "charged_with"
    # violated
    elif ("violated" in txt) and ("by" in txt):
        return "violated_by"
    # judge
    elif ("judgment" in txt) and ("for" in txt):
        return "judgment_for"
    elif ("judgment" in txt) and ("in" in txt):
        return "judgment_in"
    # order
    elif ("order" in txt) and ("from" in txt):
        return "order_from"
    elif ("order" in txt) and ("for" in txt):
        return "order_for"
    # impose
    elif ("impose" in txt) and ("for" in txt):
        return "impose_for"
    # pay
    elif ("pay" in txt) and ("for" in txt):
        return "pay_for"
    else:
        return ""


def _question_selector(key: str):
    """based on a key from _question helper find the list of good question to ask """

    # accused
    if "accus" in key:
        qs = [
            #
            ("What is the accusation?", "what_acusation"),
            ("What are the accusations?", "what_acusations"),
            #
            ("They are accused of what?", "accused_what"),
            ("It is accused of what?", "accused_what"),
            ("He is accused of what?", "accused_what"),
            #
            ("For what are they accused?", "for_accused"),
            ("For what is it accused?", "for_accused"),
            ("For what is he accused?", "for_accused"),
        ]
    # charged
    elif "charge" in key:
        qs = [
            #
            ("What are the charges?", "what_charges"),
            ("What is the charge?", "what_charge"),
            #
            ("they are charged of what?", "charged_what"),
            ("He is charged of what?", "charged_what"),
            ("It is charged of what?", "charged_what"),
            #
            ("For what are they charged?", "for_charged"),
            ("For what is he charged?", "for_charged"),
            ("For what is it charged?", "for_charged"),
        ]
    # violated
    elif "violate" in key:
        qs = [
            #
            ("What are the violations?", "what_violations"),
            ("What is the violation?", "what_violation"),
            #
            ("They have violated what?", "violated_what"),
            ("He has violated what?", "violated_what"),
            ("It has violated what?", "violated_what"),
            #
            ("What have they violated?", "what_violated"),
            ("What has he violated?", "what_violated"),
            ("What has it violated?", "what_violated"),
        ]
    # judgement
    elif "judge" in key:
        qs = [
            #
            ("What is the reason of the judgement?", "what_judge"),
            ("What are the reasons of the judgement?", "what_judge"),
            #
            ("For what are they judge?", "for_what_judge"),
            ("For what are they under judgement?", "for_what_judge"),
            ("For what is he judge?", "for_what_judge"),
            ("For what is it under judgement?", "for_what_judge"),
            ("For what is he judge?", "for_what_judge"),
            ("For what is it under judgement?", "for_what_judge"),
            #
            ("They are judged for what?", "for_what_judge"),
            ("They are under judgedment for what?", "for_what_judge"),
            ("He is judged for what?", "for_what_judge"),
            ("He is under judgedment for what?", "for_what_judge"),
            ("It is judged for what?", "for_what_judge"),
            ("It is under judgedment for what?", "for_what_judge"),
        ]
    # order
    elif "order" in key:
        qs = [
            #
            ("What is the reason of the order?", "what_judge"),
            ("What are the reasons of the order?", "what_judge"),
        ]
    # impose
    elif "impose" in key:
        qs = [
            #
            ("What is the reason of the imposition?", "what_impose"),
            ("What are the reasons of the imposition?", "what_impose"),
            #
            ("For what are they imposed?", "for_imposed"),
            ("For what is he imposed?", "for_imposed"),
            ("For what is it imposed?", "for_imposed"),
        ]
    elif "pay" in key:
        qs = [
            #
            ("What is the reason of the payement?", "what_payement"),
            ("What are the reasons of the payement?", "what_payement"),
            #
            ("For what have they to pay?", "for_pay"),
            ("For what has he to pay?", "for_pay"),
            ("For what has it to pay?", "for_pay"),
        ]

    else:
        qs = [
            ("What is the accusation?", "what_acusation"),
            ("What are the accusations?", "what_acusations"),
            ("What is the reason of the payement?", "what_payement"),
            ("What are the reasons of the payement?", "what_payement"),
            ("What is the reason of the imposition?", "what_impose"),
            ("What are the reasons of the imposition?", "what_impose"),
            ("What is the reason of the order?", "what_judge"),
            ("What are the reasons of the order?", "what_judge"),
            ("What is the reason of the judgement?", "what_judge"),
            ("What are the reasons of the judgement?", "what_judge"),
            ("What are the violations?", "what_violations"),
            ("What is the violation?", "what_violation"),
            ("What are the charges?", "what_charges"),
            ("What is the charge?", "what_charge"),
        ]

    return qs


def _ask_all(txt, nlpipe) -> list:
    """first make a selection of good questions based on the text, and
    then ask the questions and return a list of dict"""

    # txt
    if not txt:
        raise AttributeError(f"Attribute error txt ; txt is {txt}, format {type(txt)}")

    # pipe
    nlpipe = _if_not_pipe(nlpipe)

    # ans
    ans = []

    key = _question_helper(txt)
    # print(key)
    quest_pairs = _question_selector(key)
    # print(quest_pairs)

    # loop
    for quest, label in quest_pairs:
        ds = _ask(txt=txt, quest=quest, nlpipe=nlpipe)
        _ = [d.update({"question": label}) for d in ds]
        ans.extend(ds)

    # sort
    ans = sorted(ans, key=lambda i: i["score"], reverse=True)

    return ans


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


def _clean_ans(ans):
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


def _merge_ans(ans, threshold=0.1):
    """based on new_answer we will make a groupby adding the scores for each new ans in a cumulative score
    example [{new_ans : hello, score:0.3},{new_ans : hello, score:0.3}, ]
    will become  [{new_ans : hello, score:0.6},]"""

    # build dataframe
    df = pd.DataFrame(ans)
    df = df.loc[:, ["score", "new_answer"]]

    # group by ans and make cumutavie score of accuracy
    ll = [
        {"new_answer": k, "cum_score": round(v.score.sum(), 2)}
        for k, v in df.groupby("new_answer")
        if v.score.sum() > threshold
    ]
    ll = sorted(ll, key=lambda i: i["cum_score"], reverse=True)

    return ll


def predict_violation(
    struct_doc: list,
    nlpipe=None,
    pers_org_entities_list=None,
    threshold=0.4,
):
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    # pipe to avoid re init a pipe each time (+/- 15 -> 60 sec)
    # win lots of time if the method is used in a loop with 100 predictions
    nlpipe = _if_not_pipe(nlpipe)

    # pers_org_entities_list
    # we will use this one later to make a filter at the end
    if not pers_org_entities_list:
        pers_org_entities_list = _get_entities_pers_orgs(struct_doc)

    # items
    # we will work on h1 and / or article but just 2 or 3 1st paragraphs
    h1 = struct_doc["h1"]
    sub_article = "\n".join(struct_doc["article"].split("\n")[:2])

    # ask medhod
    # here are the question answering and the true prediction built
    ans_h1 = _ask_all(h1, nlpipe=nlpipe)
    ans_article = _ask_all(sub_article, nlpipe=nlpipe)
    ans = ans_h1 + ans_article

    # clean ans
    # ans is a list of dict, each dict has keys such as answer, score etc
    # for each answer we will clean this answer and create a new_answer more accurate
    cleaned_ans = _clean_ans(ans)

    # merge ans
    # based on new_answer we will make a groupby adding the scores for each new ans in a cumulative score
    # example [{new_ans : hello, score:0.3},{new_ans : hello, score:0.3}, ]
    # will become  [{new_ans : hello, score:0.6},]
    merged_ans = _merge_ans(cleaned_ans)

    # filert by spacy entities
    # we are sure that a personn or an org is NOT a violation so
    # if a prediction is in pers_org_entities_list, plz drop it
    consitant_ans = [
        i for i in merged_ans if i["new_answer"] not in pers_org_entities_list
    ]

    # filter by threshold
    # we need to filter the score above which we consider that no a signe score but a
    # cumulative score (much more strong, accurante and solid) will be droped
    consitant_ans = [(i["new_answer"], i["cum_score"]) for i in consitant_ans]
    last_ans = [(i, j) for i, j in consitant_ans if j > threshold]

    return ",".join([i for i, j in last_ans])


if __name__ == "__main__":

    # import
    from legal_doc_processing.utils import get_pipeline, get_spacy, get_orgs, get_pers
    from legal_doc_processing.press_release.utils import press_release_X_y
    from legal_doc_processing.press_release.segmentation.structure import (
        structure_press_release,
    )

    # laod
    nlpipe = get_pipeline()
    nlpspa = get_spacy()

    # structured_press_release_r
    df = press_release_X_y(features="defendant")
    df["structured_txt"] = [structure_press_release(i) for i in df.txt.values]

    # one
    one = df.iloc[0, :]
    # one features
    defendant = one.defendant
    one_struct = struct_doc = one.structured_txt
    one_h1 = one_struct["h1"]
    one_article = one_struct["article"]
    sub_one_article = "\n".join(one_article.split("\n")[:2])

    # items
    h1 = struct_doc["h1"]
    sub_article = "\n".join(struct_doc["article"].split("\n")[:2])
    pred = predict_violation(one_struct, nlpipe)

    # 1 to len(df)
    print(f" {'y'.rjust(60)} -->  {'pred'} \n")
    print(160 * "-")
    for i in range(0, len(df)):
        defendant = df.defendant.iloc[i]
        i_text = df.txt.iloc[i]
        i_struct = df["structured_txt"].iloc[i]
        pred = predict_violation(i_struct, nlpipe)
        print(f" -->  {pred[:300]} \n")