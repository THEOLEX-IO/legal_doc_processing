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

    # quest
    ans_list = list()
    for sent in sent_list:
        key_list = _question_helper(sent)
        if key_list:
            quest_pairs = _question_lister(key_list)
            ans_list.extend(ask_all(sent, quest_pairs, sent=sent, nlpipe=data.nlpipe))

    if not ans_list:
        return [("", 1)]

    # filter by threshold
    answer_label = "answer"
    flatten_ans = [(i[answer_label], i["cum_score"]) for i in ans_list]
    last_ans = [(i, j) for i, j in flatten_ans if j > threshold]

    return last_ans