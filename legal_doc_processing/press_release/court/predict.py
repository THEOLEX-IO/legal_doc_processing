from legal_doc_processing import logger


from legal_doc_processing.utils import uniquize as _u

from legal_doc_processing.utils import merge_ans, ask_all

from legal_doc_processing.press_release.court.questions import (
    _question_helper,
    _question_selector,
)


def predict_court(data: dict) -> list:
    """ """

    # make sent list, and filter not cooperat in sent
    sent_list = data.content_sents
    court_ok = lambda j: ("court" in j) or ("tribunal" in j) or ("district" in j)
    court_sent_list = [(i, j) for i, j in enumerate(sent_list) if court_ok(j.lower())]

    # if no sents :
    if not len(court_sent_list):
        return [(-1, 1)]

    # questions
    ans = list()
    for i, sent in court_sent_list:
        quest_pairs = _u(_question_selector(_question_helper(sent)))
        ans.extend(ask_all(sent, quest_pairs, sent_id=i, sent=sent, nlpipe=nlpipe))

    # answers
    ans_answer = [ans[0]["answer"]]
    clean = (
        lambda j: j.replace(".\n", ". \n").replace("\n", " ").replace("  ", " ").strip()
    )

    return [(clean(j), 1) for j in ans_answer]