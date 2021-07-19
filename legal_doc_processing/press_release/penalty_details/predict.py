from legal_doc_processing import logger

from legal_doc_processing.utils import uniquize as _u


def predict_penalty_details(data: dict) -> list:
    """ """

    sanctions = data._feature_dict["_extracted_sanctions"]

    sanct_selector = lambda i: (("monetar" and "penalt") or "pay" or "$") in i.lower()
    sanctions = [(i, j) for i, j in sanctions if sanct_selector(i)]

    return sanctions
