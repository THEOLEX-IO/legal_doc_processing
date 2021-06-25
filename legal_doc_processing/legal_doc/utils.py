from itertools import product

import pandas as pd

from legal_doc_processing.utils import (
    _if_not_spacy,
    _if_not_pipe,
    _ask,
    # get_pers,
    # get_orgs,
    get_label_,
)


# def get_entities_pers_orgs(txt: dict, n_paragraphs: int = 2, nlpspa=None) -> list:
#     """get entities PERSON and ORG from h1 and sub_article """

#     nlpspa = _if_not_spacy(nlpspa)

#     # all pers all orgs from spacy entities
#     all_pers = get_pers(txt, nlpspa)
#     all_orgs = get_orgs(txt, nlpspa)
#     pers_org_entities_list = all_pers + all_orgs

#     return pers_org_entities_list
