from legal_doc_processing import logger

from legal_doc_processing.utils import uniquize as _u

from legal_doc_processing.utils import merge_ans, ask_all

from legal_doc_processing.press_release.extracted_sanctions.questions import (
    _question_helper,
    _question_selector,
    _question_lister,
    _key_list,
)


def predict_extracted_sanctions(
    data: dict,
    h1_len_threshold: int = 15,
    content_n_sents_threshold: int = 6,
    threshold: float = 0.25,
) -> list:

    # sents
    h1 = [data.h1] if len(data.h1) > h1_len_threshold else [""]
    sent_list = h1 + data.content_sents[:content_n_sents_threshold]
    sent_list = [i.replace("\n", "").strip() for i in sent_list if i]

    filter_sents = lambda sent: any([(key in sent.lower()) for key in _key_list])
    sents_ok = [(i, j) for i, j in enumerate(sent_list) if filter_sents(j)]

    # quest
    ans_list = list()
    for i, sent in sents_ok:
        key_list = _question_helper(sent)
        if key_list:
            quest_pairs = _question_lister(key_list)
            ans_list.extend(ask_all(sent, quest_pairs, sent=sent, nlpipe=data.nlpipe))

    if not ans_list:
        return [("", 1)]

    # merged_ans
    answer_label = "answer"
    merged_ans = merge_ans(ans_list, label=answer_label)

    # filter by threshold
    flatten_ans = [(i[answer_label], i["cum_score"]) for i in merged_ans]
    last_ans = [(i, j) for i, j in flatten_ans if j > threshold]

    return last_ans