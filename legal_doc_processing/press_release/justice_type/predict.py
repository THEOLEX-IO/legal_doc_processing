from legal_doc_processing import logger


def predict_justice_type(data: dict) -> list:
    """ """

    # juridiction = [data.juridiction]

    if ("cftc" or "cfbp" or "cfpb") in data.juridiction:
        return [("U.S. - Civil", 1)]

    if ("doj" or "sec") in data.juridiction:
        return [("U.S. - Penal", 1)]

    return [("-- DUMMY --", 1)]
