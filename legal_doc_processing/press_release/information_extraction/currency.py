def predict_currency(obj: dict) -> list:
    """ """

    curr_dict = {"€": "EUR", "$": "USD", "£": "GBP"}

    for k in ["€", "$", "£"]:
        if (k in obj["h1"]) or (k in obj["abstract"]):
            return [(curr_dict[k], 1)]

    return [(-1, -1)]