from legal_doc_processing import logger


def predict_nature_of_violations(data: dict) -> list:
    """ """

    violations = data.feature_dict["extracted_violations"].lower()

    natures = []
    if "money laundering" in violations.lower():
        natures.append("Money Laundering")

    if ("foreign corrupt practices act" or "fcpa") in violations:
        natures.append("FCPA")

    if "Foreign Bribery".lower() in violations:
        natures.append("Foreign Bribery")

    if "Homeland Security".lower() in violations:
        natures.append("Homeland Security")

    if "spoofing".lower() in violations:
        natures.append("Spoofing")

    if "Fraud Scheme".lower() in violations:
        natures.append("Fraud Scheme")

    return [(i, 1) for i in natures]
