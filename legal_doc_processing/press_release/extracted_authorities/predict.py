import os

from legal_doc_processing import logger

from legal_doc_processing.utils import uniquize as _u
from legal_doc_processing.utils import get_label_

from legal_doc_processing.press_release.extracted_authorities.juridiction_pairs import (
    juridiction_dict,
)


def predict_extracted_authorities(data: dict) -> list:
    """ """

    # juridiction
    juriction = [data.juriction]

    # courts
    courts = data.feature_dict["court"]
    if courts:
        courts = [i for i in courts.split(",")]

    # orgs
    all_orgs = list()
    for sent in data.content_sents:
        all_orgs.extend(get_label_(sent, "ORG", nlspa=data.nlspa))

    # filter orgs by auth
    jur_get = lambda i: juridiction_dict.get(i.lower().strip(), "")
    filtered_orgs = [jur_get(i) for i in all_orgs]
    filtered_orgs = [i.lower().strip() for i in filtered_orgs if i]

    # auths list
    auths_list = _u(juriction + courts + filtered_orgs)

    return [(i, 1) for i in auths_list]


# def predict_extracted_authorities(obj: dict) -> list:
#     """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

#     # pipe, spa
#     nlspa = obj["nlspa"]

#     # choose the item
#     h1, abstract = obj["h1"], obj["abstract"]

#     # both h1 and abstract
#     h1 = h1.strip()
#     h1 = h1 if h1[-1] != "\n" else h1[:-1]
#     h1 = h1 if h1[-1] in [".", ". "] else h1 + ". "
#     text = h1 + abstract

#     # token filter h1
#     tok_h1 = [i.text.lower() for i in nlspa(h1)]
#     jur_h1 = [_filter_jur(i) for i in tok_h1]
#     jur_h1_clean = _u([i for i in jur_h1 if i])

#     # juri h1
#     if len(jur_h1_clean) >= 1:
#         return [(i, 100) for i in jur_h1_clean]

#     # token filter abstract
#     tok_abstract = [i.text.lower() for i in nlspa(abstract)]
#     jur_abstract = [_filter_jur(i) for i in tok_abstract]
#     jur_abstract_clean = _u([i for i in jur_abstract if i])

#     # juri abstract
#     if len(jur_abstract_clean) >= 1:
#         return [(i, 1) for i in jur_abstract_clean]

#     return [(str(-3), -1)]
