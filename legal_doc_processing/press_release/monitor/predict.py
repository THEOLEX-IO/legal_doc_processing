from legal_doc_processing import logger


def predict_monitor(data: dict) -> list:
    """ """

    monitor = 0

    # make sent list, and filter not cooperat in sent
    sent_list = data.content_sents
    compliant_ok = lambda j: ("monitor" in j.lower())
    compl_sent_list = [(i, j) for i, j in enumerate(sent_list) if compliant_ok(j)]

    # if no sents :
    if not len(compl_sent_list):
        return [(0, 1)]

    for sent in compl_sent_list:
        if ("indepen" and "complian" and "monitor") in sent.lower():
            return [(1, 1)]

    return [(0, 1)]