from legal_doc_processing import logger


def predict_currency(data: dict) -> list:
    """ """

    # curr_dict = {"€": "EUR", "$": "USD", "£": "GBP"}

    # for k in ["€", "$", "£"]:
    #     if (k in obj["h1"]) or (k in obj["abstract"]):
    #         return [(curr_dict[k], 1)]

    return [(-1, -1)]