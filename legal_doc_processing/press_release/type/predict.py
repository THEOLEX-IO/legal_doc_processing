from legal_doc_processing import logger

from legal_doc_processing.utils import uniquize as _u

from legal_doc_processing.utils import merge_ans, ask_all, cosine_similarity
from legal_doc_processing.press_release.type.questions import (
    _question_helper,
    _question_selector,
    _question_lister,
)


def predict_type(
    data: dict,
    h1_len_threshold: int = 15,
    content_n_sents_threshold: int = 5,
    threshold: float = 0.25,
) -> list:
    """ """

    # sents
    h1 = [data.h1] if len(data.h1) > h1_len_threshold else [""]
    sent_list = h1 + data.content_sents[:content_n_sents_threshold]
    sent_list = [i.replace("\n", "") for i in sent_list if i]

    type_list = [
        "enforcement",
        "compliance",
        "consent order",
        "judgement",
        "negociated ageerement",
        "settlement",
        "agreement",
        "engagement",
        "order",
        "complaint",
        "decision",
    ]

    # h1
    for h in h1:
        for type_cand in type_list:
            if type_cand in h.lower():
                return [(type_cand.title().strip(), 0.5)]

    # sent list
    for sent in sent_list:
        for type_cand in type_list:
            if type_cand in sent.lower():
                return [(type_cand.title().strip(), 0.5)]

    return [("", 1)]