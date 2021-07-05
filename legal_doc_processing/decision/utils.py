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


def decision_X_y(juridiction="", features="", sample=1.0):
    """ """

    # main
    main_df = main_X_y()

    # press_release_text not na
    at_least_one_na = main_df.press_release_text.isna() + main_df.legal_doc_text.isna()
    main_df = main_df.loc[~at_least_one_na, :]

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
        "press_release_link",
        "press_release_link_new",
        "press_release_text",
        "legal_doc_text",
        "document_link",
        "document_link_new",
        "legal_doc_text",
    ] + features

    features_df = jur_df.loc[:, keep_cols]

    return features_df
