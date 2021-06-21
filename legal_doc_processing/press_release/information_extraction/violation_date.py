from legal_doc_processing.press_release.information_extraction.decision_date import (
    predict_decision_date,
)


def predict_violation_date(obj: dict) -> list:

    return predict_decision_date(obj)
