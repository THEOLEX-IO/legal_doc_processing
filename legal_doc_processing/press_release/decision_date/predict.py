import os

import dateparser

from legal_doc_processing import logger
from legal_doc_processing.utils import get_label_
from legal_doc_processing.press_release.decision_date.clean import force_dateformat

# from legal_doc_processing.press_release.decision_date.clean import (
#     _you_shall_not_pass,
# )


def predict_decision_date(data: dict) -> list:
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    if data.date:
        return [(force_dateformat(data.date), 1)]

    # sent list
    sent_list = data.content.split("\n")
    date_ok = lambda j: ("19" or "20") in j
    date_sent_list = [(i, j) for i, j in enumerate(sent_list) if date_ok(j)]

    # find date ents
    date_list = list()
    for _, sent in date_sent_list:
        date_list.extend(get_label_(sent, "DATE", nlspa=data.nlspa))

    # if  not
    if not date_list:
        return [("1900-01-01", 1)]

    # parse date
    date_list = [dateparser.parse(i) for i in date_list if dateparser.parse(i)]

    # date sort and clean
    date = sorted(date_list)[-1]
    date = str(date)[:10]

    return [(force_dateformat(data.date), 1)]
