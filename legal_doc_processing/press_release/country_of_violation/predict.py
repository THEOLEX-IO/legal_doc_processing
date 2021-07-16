import pdb

from legal_doc_processing import logger

from legal_doc_processing.utils import uniquize as _u
from legal_doc_processing.utils import get_label_, ask_all

from legal_doc_processing.press_release.country_of_violation.countries_list import (
    countries_list,
)


def predict_country_of_violation(data: dict) -> list:
    """ """

    # authorities list
    juridiction = data.juridiction
    auth_list = data.feature_dict["extracted_authorities"].lower().split(";;")

    # TO BE VALIDATED WITH MARTINE CFPB & CFTC --> 99 % accuracy USA
    # cfbp and cftc -> USA
    for auth in ["cfbp", "cftc"]:
        if juridiction in auth:
            return [("United States", 1)]

    # make sent list, and filter not cooperat in sent
    sent_list = data.content_sents

    # find the list of countries
    countries_cands = list()
    for sent in sent_list:
        # find GPE
        cand = get_label_(sent, "GPE", data.nlspa)
        # extend countries_cands
        countries_cands.append([sent, cand])

    # clean empty GPE item
    countries_cands = [[i, j] for i, j in countries_cands if j]

    ans_list = list()
    for sent, country in countries_cands:
        quest = [["what is the country of violation?", "fine"]]
        
        ans = ask_all(sent, quest, sent=sent, sent_id=country, nlpipe=data.nlpipe)
        ans_list.extend(ans)

    # countries_lowered = _u([i.lower().strip() for i in countries_cands])

    # # filter
    # _countries_list = [i.lower().strip() for i in countries_list]
    # in_countries = lambda i: i.replace("the", "").strip() in _countries_list
    # countries_filtered = [
    #     i.replace("the", "").strip() for i in countries_lowered if in_countries(i)
    # ]

    return [(i, 1) for i in countries_filtered]
