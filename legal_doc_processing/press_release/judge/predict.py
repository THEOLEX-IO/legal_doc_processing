from legal_doc_processing import logger

from legal_doc_processing.utils import uniquize as _u

from legal_doc_processing.utils import merge_ans, ask_all, get_label_
from legal_doc_processing.press_release.judge.questions import (
    _question_helper,
    _question_selector,
)


def predict_judge(data: dict, threshold: float = 0.25) -> list:
    """ """

    # make sent list, and filter not judge in sent
    sent_list = data.content_sents
    filter_judge = lambda j: "judge" in j
    judge_sent_list = [(i, j) for i, j in enumerate(sent_list) if filter_judge(j.lower())]

    # if no sents :
    if not len(judge_sent_list):
        return [("", 1)]

    # questions
    ans_list = list()
    for i, sent in judge_sent_list:
        quest_pairs = _u(_question_selector(_question_helper(sent)))
        ans_list.extend(ask_all(sent, quest_pairs, nlpipe=data.nlpipe))

    logger.info(f"ans_list : {ans_list}")

    # threshold
    ans_list = _u([ans["answer"] for ans in ans_list if ans["score"] >= threshold])

    # if no ans :
    if not ans:
        return [("", 1)]

    # # filter person list
    # pers_list = get_label_(
    #     " ".join([j for _, j in judge_sent_list]), "PERSON", nlspa=data.nlspa
    # )
    # pers_list = _u([i.lower().strip() for i in pers_list])  # unique
    # is_in = lambda i: [
    #     (i.lower().replace("judge", "").strip() in pers) for pers in pers_list
    # ]
    # ans = [i for i in ans if any(is_in(i))]

    # if no ans :
    if not ans:
        return [("", 1)]

    # ans
    ans = [ans[0]]

    # clean
    clean = (
        lambda j: j.replace(".\n", ". \n").replace("\n", " ").replace("  ", " ").strip()
    )
    ans = [clean(j) for j in ans]

    return [(j, 1) for j in ans]
