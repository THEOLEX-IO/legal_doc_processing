from legal_doc_processing.utils import uniquize as _u
from legal_doc_processing.utils import merge_ans, ask_all
from legal_doc_processing.legal_doc.clean.extracted_authorities import _filter_jur


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

    qs = list()

    if "reason" in key:
        qs.extend(
            [
                ("Who has reason?", "who_reason"),
            ]
        )
    elif "filed" in key:
        qs.extend(
            [
                ("Who has filed?", "who_filed"),
                ("Who filed?", "who_filed"),
            ]
        )
    # else:
    #     qs.extend(
    #         [
    #             ("Who has reason?", "who_reason"),
    #             ("Who has filed?", "who_filed"),
    #         ]
    #     )

    return qs


def predict_extracted_authorities(obj: dict, threshold: int = 0.2, n_sents: int = 3):

    # pipe, spa
    nlspa = obj["nlspa"]

    # choose the item
    h1, abstract = obj["h1"], obj["abstract"]

    # token filter abstract
    tok_abstract = [i.text.lower() for i in nlspa(abstract)]
    jur_abstract = [_filter_jur(i) for i in tok_abstract]
    jur_abstract_clean = _u([i for i in jur_abstract if i])

    # juri abstract
    if len(jur_abstract_clean) >= 1:
        return [(i, 1) for i in jur_abstract_clean]

    return [(str(-3), -1)]


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