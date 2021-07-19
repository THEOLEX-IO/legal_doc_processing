from legal_doc_processing import logger


def predict_nature_de_sanction(data: dict) -> list:
    """ """

    sanctions = data._feature_dict["_extracted_sanctions"]
    sanctions = [(i, j) for i, j in sanctions if "$" not in i]

    return sanctions
