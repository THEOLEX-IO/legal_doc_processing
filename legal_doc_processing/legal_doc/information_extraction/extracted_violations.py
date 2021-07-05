from legal_doc_processing import logger

from legal_doc_processing.utils import uniquize as _u

from legal_doc_processing.utils import merge_ans, ask_all

from legal_doc_processing.press_release.clean.extracted_violations import (
    _clean_str_to_str,
    _clean_list_to_list,
    clean_ans,
)

from legal_doc_processing.legal_doc.clean.defendant import (
    _sub_you_shall_not_pass,
)


def _question_helper(txt) -> list:
    """txt"""

    _txt = txt.lower()
    res = list()

    # violated
    if "violat" in _txt.lower():
        res.append("violated")

    return res


def _question_selector(key: str):
    """based on a key from _question helper find the list of good question to ask """

    qs = list()

    # violated
    if "violat" in key:
        qs.extend(
            [
                ("what is the violations?", "what_violation"),
                ("what are the violations?", "what_violations"),
            ]
        )

    # elif "filed" in key:
    #     qs = [
    #         #
    #         ("Who has filed?", "who_filed"),
    #         ("Who filed?", "who_filed"),
    #     ]
    #     res.extend(qs)
    # else:
    #     qs = [
    #         #
    #         ("Who has reason?", "who_reason"),
    #         ("Who has filed?", "who_filed"),
    #     ]
    #     res.extend(qs)

    return qs


def predict_extracted_violations(obj: dict, threshold=0.2, n_sents: int = 12):
    """ """

    # pers_org_entities_list
    pers_org_all = obj["pers_org_all"] + _u(_you_shall_not_pass(obj["pers_org_all"]))
    pers_org_all = _u(pers_org_all)

    # items
    h1, abstract = obj["h1"], obj["abstract"]
    abstract_sents = obj["abstract_sents"][:n_sents]
    ans = []

    # ask medhod
    for sent in abstract_sents:
        key_list = _question_helper(sent)
        for key in key_list:
            # print(key)
            quest_pairs = _u(_question_selector(key))
            # print(quest_pairs)
            ans.extend(ask_all(sent, quest_pairs, nlpipe=obj["nlpipe"]))

    # clean ans
    cleaned_ans = ans
    answer_label = "answer"
    if not len(cleaned_ans):
        cleaned_ans = [{answer_label: "--None--", "score": -1}]

    # merge ans
    merged_ans = merge_ans(cleaned_ans, label=answer_label)

    # filert by spacy entities
    consitant_ans = [i for i in merged_ans if i[answer_label] not in pers_org_all]

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
    feature = "nature_of_violations"

    # structured_press_release_r
    df = legal_doc_X_y(features="defendant")
    df = df.iloc[:2, :]
    df["ld"] = [LegalDoc(i, nlpipe=nlpipe, nlspa=nlspa) for i in df.txt.values]

    # preds
    t = time.time()
    # 28 objects --> 181 secondes so --> +/-10 secondes per objects
    df["pred_" + feature] = df.ld.apply(lambda i: i.predict(feature))
    t = time.time() - t

    # 1st one
    one = df.iloc[0, :]
    one_txt = one.txt
    one_ld = self = one.ld
    obj = self.data