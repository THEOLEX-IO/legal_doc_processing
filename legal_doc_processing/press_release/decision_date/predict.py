import os

import dateparser

from legal_doc_processing import logger

# from legal_doc_processing.press_release.decision_date.clean import (
#     _you_shall_not_pass,
# )


def predict_decision_date(data: dict) -> list:
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    # date = obj["struct_text"]["date"]
    # date = _you_shall_not_pass(date)

    # return [(str(dateparser.parse(date)), 1)]

    return [(-1, -1)]
