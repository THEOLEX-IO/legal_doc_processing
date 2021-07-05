from itertools import product

import pandas as pd

from legal_doc_processing import logger

from legal_doc_processing.utils import (
    _if_not_spacy,
    _if_not_pipe,
    _ask,
    # get_pers,
    # get_orgs,
    get_label_,
    main_X_y,
)


# def get_entities_pers_orgs(txt: dict, n_paragraphs: int = 2, nlpspa=None) -> list:
#     """get entities PERSON and ORG from h1 and sub_article """

#     nlpspa = _if_not_spacy(nlpspa)

#     # all pers all orgs from spacy entities
#     all_pers = get_pers(txt, nlpspa)
#     all_orgs = get_orgs(txt, nlpspa)
#     pers_org_entities_list = all_pers + all_orgs

#     return pers_org_entities_list


def legal_doc_X_y(juridiction="", features="", sample=1.0):
    """ """

    # main
    main_df = main_X_y()

    # press_release_text not na
    main_df = main_df.loc[~main_df.legal_doc_text.isna(), :]

    # juridiction
    filter_jur = lambda i: juridiction.strip().lower() == str(i).strip().lower()
    jur_df = (
        main_df.loc[main_df["juridiction"].apply(filter_jur), :]
        if juridiction
        else main_df
    )

    # sample
    jur_df = jur_df.sample(frac=sample).reset_index(drop=True)

    # features
    if not features:
        drop_cols = [i for i in jur_df if ("press_" in i)]
        jur_df.drop(drop_cols, axis=1, inplace=True)
        return jur_df

    if isinstance(features, str):
        features = [features]
    keep_cols = [
        "folder",
        "document_link",
        "document_link_new",
        "legal_doc_text",
    ] + features

    features_df = jur_df.loc[:, keep_cols]

    return features_df
