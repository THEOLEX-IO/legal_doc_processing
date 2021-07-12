from legal_doc_processing import logger


def predict_justice_type(data: dict) -> list:
    """ """

    auths = data.feature_dict["extracted_authorities"].lower()

    if ("cftc" or "cfbp") in auths:
        return [("U.S. - Civil", 1)]

    if ("doj" or "sec") in auths:
        return [("U.S. - Penal", 1)]

    return [("-- DUMMY --", 1)]
