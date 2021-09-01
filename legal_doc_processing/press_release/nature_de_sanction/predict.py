from legal_doc_processing import logger


def predict_nature_de_sanction(data: dict) -> list:
    """ """

    sanctions = data._feature_dict["_extracted_sanctions"]

    sanct_selector = lambda i: (("monetar" and "penalt") or "pay" or "$") in i.lower()
    sanctions = [(i, j) for i, j in sanctions if not sanct_selector(i)]

    return sanctions
