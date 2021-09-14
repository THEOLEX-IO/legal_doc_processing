import os

import dateparser

from legal_doc_processing import logger
from legal_doc_processing.utils import get_label_


def predict_violation_date(data: dict) -> list:

    # sent list
    sent_list = data.content.split("\n")
    date_ok = lambda j: ("19" or "20") in j
    date_sent_list = [(i, j) for i, j in enumerate(sent_list) if date_ok(j)]

    # find date ents
    date_list = []
    for _, sent in date_sent_list:
        date_list.extend(get_label_(sent, "DATE", nlspa=data.nlspa))

    # if  not
    if not date_list:
        return [("", 1)]

    # parse date
    date_list = [dateparser.parse(i) for i in date_list if dateparser.parse(i)]

    # date sort and clean
    date = sorted(date_list)[0]
    date = str(date)[:10]

    return [(date, 1)]