from legal_doc_processing import logger

from legal_doc_processing.utils import uniquize as _u

from legal_doc_processing.utils import merge_ans, ask_all
from legal_doc_processing.press_release.judge.questions import (
    _question_helper,
    _question_selector,
)


def predict_judge(data: dict) -> list:
    """ """

    # make sent list, and filter not judge in sent
    sent_list = data.content_sents
    judge_ok = lambda j: "judge" in j
    judge_sent_list = [(i, j) for i, j in enumerate(sent_list) if judge_ok(j.lower())]

    # person or all
    pers_org_all = data.pers_org_all  # _u(_sub_you_shall_not_pass(obj["pers_org_all"]))
    pers_org_all = _u(pers_org_all)  # unique

    # if no sents :
    if not len(judge_sent_list):
        return [("", 1)]

    # questions
    ans = list()
    for i, sent in judge_sent_list:
        quest_pairs = _u(_question_selector(_question_helper(sent)))
        ans.extend(ask_all(sent, quest_pairs, nlpipe=data.nlpipe))

    # answers
    ans_answer = [i["answer"] for i in ans]

    # filter by person
    pers_org_all = [i.lower().strip() for i in pers_org_all]
    filter_pers = lambda i: i.lower().strip() in pers_org_all
    ans_answer = [i for i in ans_answer if filter_pers(i)]

    # if not
    if not len(ans_answer):
        return [("", 1)]

    # clean
    clean = (
        lambda j: j.replace(".\n", ". \n").replace("\n", " ").replace("  ", " ").strip()
    )
    ans_answer = [clean(j) for j in ans_answer]

    return [(j, 1) for j in ans_answer]
