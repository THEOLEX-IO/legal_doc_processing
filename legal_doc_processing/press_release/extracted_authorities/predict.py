import os
import pdb
from legal_doc_processing import logger

from legal_doc_processing.utils import uniquize as _u
from legal_doc_processing.utils import get_label_

from legal_doc_processing.press_release.extracted_authorities.juridiction_pairs import (
    juridiction_dict,
)


def predict_extracted_authorities(data: dict) -> list:
    """ """

    # try:

    # juridiction
    juridiction = [data.juridiction]

    logger.info(f"juridiction : {juridiction} ")

    # courts
    courts = data.feature_dict["court"]
    if courts:
        courts = [i for i in courts.split(";;")]
    else:
        courts = []

    # orgs
    all_orgs = list()
    for sent in data.content_sents:
        all_orgs.extend(get_label_(sent, "ORG", nlspa=data.nlspa))

    # filter orgs by auth
    jur_get = lambda i: juridiction_dict.get(i.lower().strip(), "")
    filtered_orgs = [jur_get(i) for i in all_orgs]
    filtered_orgs = [i.lower().strip() for i in filtered_orgs if i]

    # auths list
    auths_list = [i for i in _u(juridiction + courts + filtered_orgs) if i]

    # except Exception as e:
    #     logger.error(f"e : {e} {str(e)} ")

    #     pdb.set_trace()

    #     raise e

    return [(i, 1) for i in auths_list]