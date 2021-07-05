from legal_doc_processing import logger


def predict_currency(obj: dict) -> list:
    """ """

    for k in ["€", "$", "£"]:
        if (k in obj["h1"]) or (k in obj["abstract"]):
            return [(k, 1)]

    return [(-1, -1)]
