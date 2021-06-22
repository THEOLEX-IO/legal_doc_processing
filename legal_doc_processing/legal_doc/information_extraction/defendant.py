from legal_doc_processing.utils import uniquize as _u

from legal_doc_processing.utils import merge_ans, ask_all

from legal_doc_processing.legal_doc.clean.defendant import (
    clean_ans,
    _sub_you_shall_not_pass,
)


def _question_helper(txt) -> list:
    """txt"""

    _txt = txt.lower()
    res = list()

    k_list = [
        "accused",
        "defendant",
        "violate",
        "against",
        "filed",
        "judgement",
        "complaint",
    ]
    for kk in k_list:
        if kk in _txt:
            res.append(kk)

    return res


def _question_selector(key: str) -> list:
    """based on a key from _question helper find the list of good question to ask """

    qs = list()

    if "accuse" in key:
        qs.extend(
            [
                ("Who is the accused?", "who_accused"),
                ("Who are the accused?", "who_accuseds"),
            ]
        )
    if "defendant" in key:
        qs.extend(
            [
                ("Who is the defendant?", "who_defendant"),
                ("Who are the defendants?", "who_defendants"),
                # ("what are the defendants?", "what_defendant"),
                # ("what is the defendant?", "what_defendant"),
            ]
        )
    if "violat" in key:
        qs.extend(
            [
                ("Who is the violator?", "what_violator"),
                ("Who have made the violation?", "what_violator"),
                ("Who has made the violation?", "what_violator"),
                ("Who are the violators?", "what_violators"),
                # ("What is the violator?", "what_violator"),
                # ("What are the violators?", "what_violators"),
            ]
        )
    if "against" in key:
        qs.extend(
            [
                ("Who is the victim", "what_against"),
                ("Against who is the action?", "what_against"),
                ("Who is the action against to?", "what_against"),
                ("Against who?", "what_againsts"),
                # ("What is the violator?", "what_violator"),
                # ("What are the violators?", "what_violators"),
            ]
        )
    if "filed" in key:
        qs.extend(
            [
                ("Who recieve a complaint?", "what_violator"),
                ("Who is accused?", "what_violator"),
                ("Against who is the complaint?", "what_violator"),
                # ("Who are the violators?", "what_violators"),
                # ("What is the violator?", "what_violator"),
                # ("What are the violators?", "what_violators"),
            ]
        )
    if "judgement" in key:
        qs.extend(
            [
                ("Who is pursued?", "what_judgement"),
                ("Who is inculpated?", "what_judgement"),
                ("Who is under judgement?", "what_judgement"),
                ("Who is accused?", "what_judgement"),
                ("Against who is the judgement?", "what_judgement"),
                # ("What is the violator?", "what_violator"),
                # ("What are the violators?", "what_violators"),
            ]
        )
    if "complaint" in key:
        qs.extend(
            [
                ("Who is accused?", "what_judgement"),
                ("Who is inculpated?", "what_judgement"),
                ("Who is under judgement?", "what_judgement"),
                ("Who recieved a complaint ?", "what_judgement"),
                ("Against who is the complaint?", "what_judgement"),
            ]
        )
    return qs


def predict_defendant(obj: dict, threshold=0.2, n_sents: int = 5) -> list:
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    # pipe to avoid re init a pipe each time (+/- 15 -> 60 sec)
    nlpipe, nlspa = obj["nlpipe"], obj["nlspa"]

    # pers_org_all
    pers_org_all = obj["pers_org_all"] + _u(_sub_you_shall_not_pass(obj["pers_org_all"]))
    pers_org_all = _u(pers_org_all)

    # items
    h1, abstract = obj["h1"], obj["abstract"]
    abstract_sents = obj["abstract_sents"][:n_sents]
    ans = []

    # ask method
    for sent in abstract_sents:
        key_list = _question_helper(sent)
        for key in key_list:
            # from key to questions and from questions to answers
            quest_pairs = _u(_question_selector(key))
            ans.extend(ask_all(sent, quest_pairs, nlpipe=nlpipe))

    # clean ans
    cleaned_ans = clean_ans(ans)
    answer_label = "new_answer"
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
    from legal_doc_processing.legal_doc.loader import legal_doc_X_y
    from legal_doc_processing.legal_doc.legal_doc import LegalDoc

    # laod
    nlpipe = get_pipeline()
    nlspa = get_spacy()
    nlspa.add_pipe("sentencizer")

    # data
    threshold = 0.2
    n_sents = 7
    feature = "defendant"

    # structured_press_release_r
    df = legal_doc_X_y(features="defendant")
    df = df.iloc[:2, :]
    df["obj"] = [LegalDoc(i, nlpipe=nlpipe, nlspa=nlspa) for i in df.txt.values]

    # preds
    t = time.time()
    # 28 objects --> 181 secondes so --> +/-10 secondes per objects
    df["pred_" + feature] = df.obj.apply(lambda i: i.predict(feature))
    t = time.time() - t

    # 1st one
    one = df.iloc[0, :]
    one_txt = one.txt
    one_ob = self = one.obj
    obj = self.data_