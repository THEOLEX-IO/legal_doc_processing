from legal_doc_processing.utils import uniquize as _u

from legal_doc_processing.utils import merge_ans, ask_all
from legal_doc_processing.press_release.clean.penalty_details import clean_ans


def _question_helper(txt):
    """txt"""

    _txt = txt.lower()
    res = list()

    k_list = ["require", "impose", "order", "pay", "forbid"]

    # for k in k_list:
    #     if k in _txt:
    #         res.append(k)

    res = [k for k in k_list if k in _txt]

    return res


def _question_selector(key: str):
    """based on a key from _question helper find the list of good question to ask """

    qs = list()

    if "require" in key:  # accused
        qs.extend(
            [
                ("What is required?", "what_acusation"),
                ("What is required to do? ", "what_acusation"),
            ]
        )
    if "impose" in key:
        qs.extend(
            [
                ("What is imposed?", "what_acusation"),
                ("What is imposed to do?", "what_acusation"),
            ]
        )
    if "forbid" in key:
        qs.extend(
            [
                ("What is forbidden?", "what_acusation"),
            ]
        )

    if "order" in key:
        qs.extend(
            [
                ("What is ordered?", "what_acusation"),
            ]
        )

    if "pay" in key:
        qs.extend(
            [
                ("What they have to pay? ", "what_acusation"),
            ]
        )

    qs.extend(
        [
            ("what is the injunction?", ""),
            ("they are ordered to do what?", ""),
            ("what have they to do?", ""),
            ("What is the sentence?", "what_payement"),
            ("What is the punition?", "what_payement"),
            ("What have they to do?", "what_payement"),
            ("What are their obligations?", "what_payement"),
            ("What is the condemnation ?", ""),
            ("What is forbidden?", ""),
            ("What is imposed?", ""),
        ]
    )

    return _u(qs)


def predict_penalty_details(obj: dict, threshold=0.4, n_sents: int = 5) -> list:
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    # extracted_violation
    extracted_violation = obj["_feature_dict"]["extracted_violation"]
    extracted_violation = [i.lower().strip() for i, j in extracted_violation]

    # items
    h1, abstract = obj["h1"], obj["abstract"]
    abstract_sents = obj["abstract_sents"][:n_sents]
    ans = []

    # ask medhod h1
    for key_h1 in _question_helper(h1):
        # print(f"key_h1 : {key_h1} ")
        quest_pairs = _u(_question_selector(key_h1))
        # print(f"quest_pairs : {quest_pairs} ")
        ans.extend(ask_all(h1, quest_pairs, nlpipe=obj["nlpipe"]))

    # ask medhod abstract_sents
    for sent in abstract_sents:
        key_list = _question_helper(sent)
        for key in key_list:
            # print(key)
            quest_pairs = _u(_question_selector(key))
            # print(quest_pairs)
            ans.extend(ask_all(sent, quest_pairs, nlpipe=obj["nlpipe"]))

    # clean ans
    cleaned_ans = clean_ans(ans)
    answer_label = "new_answer"
    if not len(cleaned_ans):
        cleaned_ans = [{answer_label: "--None--", "score": -1}]

    # merge ans
    merged_ans = merge_ans(cleaned_ans, label=answer_label)

    # filert by spacy entities
    consitant_ans = [
        i for i in merged_ans if i[answer_label] if i not in extracted_violation
    ]

    # filter by threshold
    flatten_ans = [(i[answer_label], i["cum_score"]) for i in consitant_ans]
    last_ans = [(i, j) for i, j in flatten_ans if j > threshold]

    return [i.lower() for i in last_ans]


if __name__ == "__main__":

    import time
    from legal_doc_processing.utils import get_pipeline, get_spacy
    from legal_doc_processing.press_release.loader import press_release_X_y
    from legal_doc_processing.press_release.press_release import PressRelease

    # load
    nlpipe = get_pipeline()
    nlspa = get_spacy()
    nlspa.add_pipe("sentencizer")

    # legal_doc df AND  OBj
    df = press_release_X_y()
    df = df.iloc[:, :]
    df["pr"] = df.txt.apply(lambda i: PressRelease(i, nlpipe=nlpipe, nlspa=nlspa))

    # preds
    t = time.time()
    # 28 objects --> 181 secondes so --> +/-10 secondes per objects
    df["pred_penalty"] = df.pr.apply(lambda i: i.predict("penalty_details"))
    t = time.time() - t

    # 1st one
    one = df.iloc[0, :]
    one_txt = one.txt
    one_ob = obj = self = one.pr

    # externize
    cols = ["txt", "pr", "preds"]
    _df = df.drop(cols, axis=1, inplace=False)
