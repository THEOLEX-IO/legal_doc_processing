from itertools import product

import pandas as pd

from legal_doc_processing.utils import (
    _if_not_spacy,
    _if_not_pipe,
    get_pers,
    get_orgs,
    get_label_,
    _ask,
)


def product_juridiction_pairs():

    cftc_cands = ["cftc", "Commodity Futures Trading Commission", "c.f.t.c"]
    doj_cands = ["doj", "department of justice", "d.o.j."]
    sec_cands = ["sec", "Securities and Exchange Commission", "s.e.c."]

    cands = dict()
    for k, _list in [("cftc", cftc_cands), ("doj", doj_cands), ("sec", sec_cands)]:
        dd = {i.lower().strip(): k.lower().strip() for i in _list}
        cands.update(dd)

    return cands


def product_juridic_form():
    """ make a list of llc, LLC, LLC. etc etc """

    # cands
    cands = ["inc", "llc", "ltd", "corp"]

    # conatiner
    llc_list = list()

    # for each
    for i in cands:
        # various case
        sample = [str(i), str(i).lower(), str(i).capitalize(), str(i).upper()]
        # case * -- point ou pas -- * --  espace, ou pas --
        sample = product(sample, [", ", " ", ""], [".", ""])
        sample = [str(j + i + k) for i, j, k in sample]
        # extend
        llc_list.extend(sample)

    # sorted reverse lengt
    llc_list = [(len(i), i) for i in llc_list]
    llc_list = sorted(llc_list, reverse=True, key=lambda i: i[0])
    llc_list = [i[1] for i in llc_list]

    return llc_list


def get_entities_pers_orgs(struct_doc: dict, n_paragraphs: int = 2, nlpspa=None) -> list:
    """get entities PERSON and ORG from h1 and sub_article """

    nlpspa = _if_not_spacy(nlpspa)

    # sub article
    sub_article = "\n".join(struct_doc["article"].split("\n")[:n_paragraphs])

    # all pers all orgs from spacy entities
    all_pers = get_pers(struct_doc["h1"], nlpspa) + get_pers(sub_article, nlpspa)
    all_orgs = get_orgs(struct_doc["h1"], nlpspa) + get_orgs(sub_article, nlpspa)
    pers_org_entities_list = all_pers + all_orgs

    return pers_org_entities_list
