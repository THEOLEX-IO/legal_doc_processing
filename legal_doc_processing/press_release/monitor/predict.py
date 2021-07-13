from legal_doc_processing import logger


def predict_monitor(data: dict) -> list:
    """ """

    # make sent list, and filter not cooperat in sent
    sent_list = data.content_sents
    monitor_ok = lambda j: ("monitor" in j.lower())
    monitor_sent_list = [(i, j) for i, j in enumerate(sent_list) if monitor_ok(j)]

    # if no sents :
    if not len(monitor_sent_list):
        return [(0, 1)]

    for _, sent in monitor_sent_list:
        if ("indepen" and "complian" and "monitor") in sent.lower():
            return [(1, 1)]

    return [(0, 0.55)]