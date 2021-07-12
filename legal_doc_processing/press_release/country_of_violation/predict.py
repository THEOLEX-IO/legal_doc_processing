from legal_doc_processing import logger

from legal_doc_processing.utils import uniquize as _u
from legal_doc_processing.utils import get_label_

from legal_doc_processing.press_release.country_of_violation.countries_list import (
    countries_list,
)


def predict_country_of_violation(data: dict) -> list:
    """ """

    # authorities list
    auth_list = data.feature_dict["extracted_authorities"].lower().split(",")

    # cfbp and cftc -> USA
    for auth in ["cfbp", "cftc"]:
        if auth in auth_list:
            return [("United States of America", 1)]

    # make sent list, and filter not cooperat in sent
    sent_list = data.content_sents

    # find the list of countries
    countries_cands = _u([get_label_(sent, "GPE", data.nlspa) for sent in sent_list])
    countries_lowered = [i.lower().strip() for i in countries_list]

    # filter
    in_countries = lambda i: i.strip().lower() in countries_lowered
    countries_filtered = [i for i in countries_cands if in_countries(i)]

    return [(i, 1) for i in countries_filtered]
