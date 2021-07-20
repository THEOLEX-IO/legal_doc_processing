from legal_doc_processing import logger

from legal_doc_processing.utils import uniquize as _u

from legal_doc_processing.utils import merge_ans, ask_all, get_label_

from legal_doc_processing.press_release.court.questions import (
    _question_helper,
    _question_selector,
)

from legal_doc_processing.press_release.court.clean import final_clean


def predict_court(data: dict, threshold: float = 0.25) -> list:
    """ """

    # make sent list, and filter not cooperat in sent
    sent_list = data.content_sents
    court_ok = lambda j: ("court" or "tribunal" or "district" or "federal") in j
    court_sent_list = [(i, j) for i, j in enumerate(sent_list) if court_ok(j.lower())]

    # if no sents :
    if not len(court_sent_list):
        return [("", 1)]

    # questions
    ans_list = list()
    for i, sent in court_sent_list:
        quest_pairs = _u(_question_selector(_question_helper(sent)))
        ans_list.extend(ask_all(sent, quest_pairs, nlpipe=data.nlpipe))

    # logger.info(f"ans_list : {ans_list}")

    # threshold
    ans_list = _u([ans["answer"] for ans in ans_list if ans["score"] >= threshold])

    # if no ans :
    if not ans_list:
        return [("", 1)]

    # # filter org_list
    # org_list = get_label_(
    #     " ".join([j for _, j in court_sent_list]), "ORG", nlspa=data.nlspa
    # )
    # org_list = _u([i.lower().strip() for i in org_list])  # unique
    # is_in = lambda i: [(i.lower().strip() in org) for org in org_list]
    # ans = [i for i in ans if any(is_in(i))]

    # ans
    ans_list = [ans_list[0]]

    # clean
    ans_list = [final_clean(j) for j in ans_list]

    return [(j, 1) for j in ans_list]