from legal_doc_processing.utils import uniquize as _u

from legal_doc_processing.utils import merge_ans, ask_all

from legal_doc_processing.legal_doc.clean.decision_date import (
    clean_ans,
    _sub_shall_not_pass,
)


def _question_helper(txt) -> list:
    """txt"""

    _txt = txt.lower()
    res = list()

    # reason
    if "violate" in _txt.lower():
        res.append("violate")
    # filed
    if "filed" in _txt.lower():
        res.append("filed")
    # filed
    if "filled" in _txt.lower():
        res.append("filed")

    return res


def _question_selector(key: str):
    """based on a key from _question helper find the list of good question to ask """

    res = list()

    # reason
    if "violate" in key:
        qs = [
            #
            ("When was the violation?", "when_violation"),
            ("When did the violation take place ?", "when_violation"),
            ("When did the violations take place ?", "when_violations"),
        ]
        res.extend(qs)

    # reason
    if "filed" in key:
        qs = [
            #
            ("When was filed a complaint?", "when_violation"),
            ("When was the complaint filed?", "when_violation"),
            ("When were the complaints filed?", "when_violations"),
        ]
        res.extend(qs)

    return res


def predict_decision_date(obj: dict, threshold=0.2, n_sents: int = 7) -> list:

    # pipe to avoid re init a pipe each time (+/- 15 -> 60 sec)
    # win lots of time if the method is used in a loop with 100 predictions
    nlpipe, nlspa = obj["nlpipe"], obj["nlspa"]

    # date_all
    # we will use this one later to make a filter at the end
    date_all = obj["date_all"] + [_sub_shall_not_pass(i) for i in obj["date_all"]]
    date_all = _u(date_all)

    # items
    # we will work on h1 and / or article but just 2 or 3 1st paragraphs
    h1, abstract = obj["h1"], obj["abstract"]
    abstract_sents = obj["abstract_sents"][:n_sents]
    ans = []

    # ask method
    # for each sentence
    for sent in abstract_sents:
        # print(sent)
        # key list
        key_list = _question_helper(sent)
        for key in key_list:
            # print(key)
            # from key to questions and from questions to answers
            quest_pairs = _u(_question_selector(key))
            ans.extend(ask_all(sent, quest_pairs, nlpipe=nlpipe))

    # clean ans
    # ans is a list of dict, each dict has keys such as answer, score etc
    # for each answer we will clean this answer and create a new_answer more accurate
    cleaned_ans = clean_ans(ans)
    answer_label = "new_answer"
    if not len(cleaned_ans):
        cleaned_ans = [{answer_label: "--None--", "score": -1}]

    # merge ans
    # based on new_answer we will make a groupby adding the scores for each new ans in a cumulative score
    # example [{new_ans : hello, score:0.3},{new_ans : hello, score:0.3}, ]
    # will become  [{new_ans : hello, score:0.6},]
    merged_ans = merge_ans(cleaned_ans, label=answer_label)

    # filert by spacy entities
    # we are sure that a personn or an org is NOT a violation so
    # if a prediction is in pers_org_entities_list, plz drop it
    consitant_ans = [i for i in merged_ans if i[answer_label] in date_all]

    # filter by threshold
    # we need to filter the score above which we consider that no a signe score but a
    # cumulative score (much more strong, accurante and solid) will be droped
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

    # structured_press_release_r
    df = legal_doc_X_y(features="defendant")
    df = df.iloc[:7, :]
    df["obj"] = [LegalDoc(i, nlpipe=nlpipe, nlspa=nlspa) for i in df.txt.values]

    # preds
    t = time.time()
    # 28 objects --> 181 secondes so --> +/-10 secondes per objects
    df["preds"] = df.obj.apply(lambda i: i.predict_all())
    t = time.time() - t

    # labels
    preds_labels = list(df.preds.iloc[0].keys())
    for k in preds_labels:
        df["pred_" + k] = df.preds.apply(lambda i: i[k])

    # 1st one
    one = df.iloc[0, :]
    one_txt = one.txt
    one_ob = obj = self = one.obj