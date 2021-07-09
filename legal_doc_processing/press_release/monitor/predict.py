from legal_doc_processing import logger


def predict_monitor(data: dict) -> list:
    """ """

    # monitor = 0

    # for sent in obj["all_text_sents"]:
    #     if (
    #         ("indepen" in sent.lower())
    #         and ("complian" in sent.lower())
    #         and ("monitor" in sent.lower())
    #     ):
    #         monitor += 1

    # return [("1", 0.8)] if monitor else [("0", 0.8)]

    return [(-1, -1)]