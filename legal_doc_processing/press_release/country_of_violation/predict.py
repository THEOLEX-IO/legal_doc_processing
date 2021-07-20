import pdb

from legal_doc_processing import logger

from legal_doc_processing.utils import uniquize as _u
from legal_doc_processing.utils import get_label_

from legal_doc_processing.press_release.country_of_violation.countries_list import (
    countries_list,
)


def predict_country_of_violation(data: dict) -> list:
    """ """

    # authorities list
    juridiction = data.juridiction
    auth_list = data.feature_dict["extracted_authorities"].lower().split(";;")

    # cfbp and cftc -> USA
    for auth in ["cfbp", "cftc"]:
        if juridiction in auth:
            return [("United States", 1)]

    # make sent list, and filter not cooperat in sent
    sent_list = data.content_sents

    # find the list of countries
    countries_cands = list()
    for sent in sent_list:
        countries_cands.extend(get_label_(sent, "GPE", data.nlspa))
    countries_lowered = _u([i.lower().strip() for i in countries_cands])

    # filter
    _countries_list = [i.lower().strip() for i in countries_list]
    in_countries = lambda i: i.replace("the", "").strip() in _countries_list
    countries_filtered = [
        i.replace("the", "").strip() for i in countries_lowered if in_countries(i)
    ]

    # if not countries_filtered:
    #     pdb.set_trace()

    return [(i.title().strip(), 1) for i in countries_filtered]
