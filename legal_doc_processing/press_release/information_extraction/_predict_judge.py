from legal_doc_processing.utils import uniquize as _u

from legal_doc_processing.utils import merge_ans, ask_all


def _question_helper(txt) -> list:
    """txt"""

    _txt = txt.lower()
    res = list()

    cands = [
        #######################################
        # your  tags here
        #######################################
    ]

    for cand in cands:
        if cand in _txt:
            res.append(cand)

    return res


def _question_selector(key: str) -> list:
    """based on a key from _question helper find the list of good question to ask """

    res = list()

    #######################################

    # if " -- YOUR TAG -- " in key:
    #     res.extend(
    #         [
    #             ("-- YOUR QUESTION -- ", "who_question"),
    #         ]
    #     )

    #######################################

    return res


def _predict_judge(obj: dict, threshold: float = 0.4, n_sents: int = 3) -> list:
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    # pipe to avoid re init a pipe each time (+/- 15 -> 60 sec)
    nlpipe = obj["nlpipe"]

    # pers_org_entities_list
    pers_org_all = obj["pers_org_all"] + # _u(_sub_you_shall_not_pass(obj["pers_org_all"]))
    pers_org_all = _u(pers_org_all)


    # items
    abstract_sents = obj["abstract_sents"][:n_sents]
    ans = []


    for sent in abstract_sents:
        key_list = _question_helper(sent)
        for key in key_list:
            quest_pairs = _u(_question_selector(key))
            ans.extend(ask_all(sent, quest_pairs, nlpipe=nlpipe))

    # clean ans
    cleaned_ans = ans
    answer_label = "answer"
    if not len(cleaned_ans):
        cleaned_ans = [{answer_label: "--None--", "score": -1}]

    # merge ans
    merged_ans = merge_ans(cleaned_ans, label=answer_label)

    # filert by spacy entities
    consitant_ans = [i for i in merged_ans if i[answer_label] in pers_org_all]

    # filter by threshold
    flatten_ans = [(i[answer_label], i["cum_score"]) for i in consitant_ans]
    last_ans = [(i, j) for i, j in flatten_ans if j > threshold]

    return last_ans




if __name__ == "__main__":

    # import
    import time
    from legal_doc_processing.utils import get_pipeline, get_spacy
    from legal_doc_processing.press_release.loader import press_release_X_y
    from legal_doc_processing.press_release.press_release import PressRelease

    # laod
    nlpipe = get_pipeline()
    nlspa = get_spacy()
    nlspa.add_pipe("sentencizer")

    # structured_press_release_r
    df = press_release_X_y(features="defendant")
    df = df.iloc[:7, :]
    df["obj"] = [PressRelease(i, nlpipe=nlpipe, nlspa=nlspa) for i in df.txt.values]

    # preds
    t = time.time()
    # 28 objects --> 181 secondes so --> +/-10 secondes per objects
    df["pred_judge"] = df.obj.apply(lambda i: i.predict("judge"))
    t = time.time() - t

    # # labels
    # preds_labels = list(df.preds.iloc[0].keys())
    # for k in preds_labels:
    #     df["pred_" + k] = df.preds.apply(lambda i: i[k])

    # 1st one
    one = df.iloc[0, :]
    one_txt = one.txt
    one_ob = obj = self = one.obj