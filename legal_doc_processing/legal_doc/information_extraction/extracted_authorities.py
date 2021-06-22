from legal_doc_processing.utils import uniquize as _u

from legal_doc_processing.utils import merge_ans, ask_all
from legal_doc_processing.utils import ask_all, merge_ans


def _question_helper(txt) -> list:
    """txt"""

    _txt = txt.lower()
    res = list()

    k_list = [
        "reason",
        # "accused",
        # "defendant",
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


def _question_selector(key: str):
    """based on a key from _question helper find the list of good question to ask """

    res = list()

    # reason
    if "reason" in key:
        qs = [
            #
            ("Who has reason?", "who_reason"),
        ]
        res.extend(qs)

    elif "filed" in key:
        qs = [
            #
            ("Who has filed?", "who_filed"),
            ("Who filed?", "who_filed"),
        ]
        res.extend(qs)
    else:
        qs = [
            #
            ("Who has reason?", "who_reason"),
            ("Who has filed?", "who_filed"),
        ]
        res.extend(qs)

    return res


def predict_extracted_authorities(obj: dict, threshold: int = 0.2, n_sents: int = 3):

    # pipe to avoid re init a pipe each time (+/- 15 -> 60 sec)
    # win lots of time if the method is used in a loop with 100 predictions
    nlpipe, nlspa = obj["nlpipe"], obj["nlspa"]

    # pers_org_all
    # we will use this one later to make a filter at the end
    pers_org_all = obj["pers_org_all"] + _u(_sub_you_shall_not_pass(obj["pers_org_all"]))
    pers_org_all = _u(pers_org_all)

    # items
    # we will work on h1 and / or article but just 2 or 3 1st paragraphs
    h1, abstract = obj["h1"], obj["abstract"]
    abstract_sents = obj["abstract_sents"][:n_sents]
    ans = []

    # ask method
    # for each sentence
    for sent in abstract_sents:
        key_list = _question_helper(sent)
        for key in key_list:
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
    consitant_ans = [i for i in merged_ans if i[answer_label] in pers_org_all]

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

    # data
    threshold = 0.2
    n_sents = 7
    feature = "extracted_authorities"

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