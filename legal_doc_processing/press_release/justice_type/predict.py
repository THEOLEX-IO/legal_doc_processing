from legal_doc_processing import logger


def predict_justice_type(data: dict) -> list:
    """ """

    auths = data.features_dict["extracted_authorities"]

    if "cftc" or "cfpb" in auths:
        return ["U.S. - Civil"]

    return [(-1, -1)]
