def predict_country_of_violation(obj: dict) -> list:
    """ """

    auth = obj["feature_dict"]["extracted_authorities"].lower()

    for kk in ["sec", "doj", "cftc"]:
        if kk in auth:
            return [("United States of America", 1)]

    return [(-1, -1)]
