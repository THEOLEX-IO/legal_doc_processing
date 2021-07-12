from legal_doc_processing import logger

from legal_doc_processing.utils import uniquize as _u

from legal_doc_processing.utils import merge_ans, ask_all


def predict_cooperation_credit(data: dict, threshold=0.4, n_sents: int = 5) -> list:
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    # make sent list, and filter not cooperat in sent
    sent_list = data.content_sents
    coop_sent_list = [(i, j) for i, j in enumerate(sent_list) if "cooperat" in j.lower()]

    # if no sents :
    if not len(coop_sent_list):
        return [(-1, 1)]

    clean = lambda j: j.replace(".\n", ". \n").replace("\n", "")
    return [(clean(j), 1) for _, j in coop_sent_list]
