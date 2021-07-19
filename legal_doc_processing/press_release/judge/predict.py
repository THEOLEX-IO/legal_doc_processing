from legal_doc_processing import logger

from legal_doc_processing.utils import uniquize as _u

from legal_doc_processing.utils import merge_ans, ask_all, get_label_
from legal_doc_processing.press_release.judge.questions import (
    _question_helper,
    _question_selector,
    _question_lister,
)
from legal_doc_processing.press_release.judge.clean import clean_ans_list, clean_ans


def predict_judge(data: dict, threshold: float = 0.75) -> list:
    """ """

    # make sent list, and filter not judge in sent
    sent_list = data.content_sents
    filter_judge = lambda j: ("judge" or "attorney") in j.lower()
    judge_sent_list = [(i, j) for i, j in enumerate(sent_list) if filter_judge(j)]

    # if no sents :
    if not judge_sent_list:
        return [("", 1)]

    # quest
    ans_list = list()
    for i, sent in judge_sent_list:
        key_list = _question_helper(sent)
        if key_list:
            quest_pairs = _question_lister(key_list)
            ans_list.extend(
                ask_all(sent, quest_pairs, sent_id=i, sent=sent, nlpipe=data.nlpipe)
            )

    # logger.info(f"ans_list : {ans_list}")

    if not len(ans_list):
        return [("", 1)]

    # clean ans
    cleaned_ans = clean_ans_list(ans_list)
    answer_label = "new_answer"

    # merge ans
    merged_ans = merge_ans(cleaned_ans, label=answer_label)

    # filter person list
    # pers_list = _u([clean_ans(i) for i in data.pers_all])  # unique
    # is_in = lambda i: i[answer_label] in pers_list
    # filtered_ans = [i for i in merged_ans if is_in(i)]

    # filter by threshold
    flatten_ans = [(i[answer_label], i["cum_score"]) for i in merged_ans]
    final_ans = [(i, j) for i, j in flatten_ans if j >= threshold]

    # if no ans :
    if not final_ans:
        return [("", 1)]

    return [final_ans[0]]
