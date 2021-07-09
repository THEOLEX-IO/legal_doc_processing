from legal_doc_processing import logger

from legal_doc_processing.press_release.decision_date.predict import predict_decision_date


def predict_violation_date(obj: dict) -> list:

    return predict_decision_date(obj)
