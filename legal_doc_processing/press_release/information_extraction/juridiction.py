import os

import pandas as pd

from legal_doc_processing.utils import (
    _if_not_pipe,
    _if_not_spacy,
    get_spacy,
    _ask,
)

from legal_doc_processing.press_release.information_extraction.utils import (
    product_juridiction_pairs,
)


def _filter_jur(token, cands: list = None):
    """ """

    if not cands:
        cands = product_juridiction_pairs()

    for k, v in cands.items():
        if token.lower().strip() == k.lower().strip():
            return v.upper()

    return ""


def predict_juridiction(struct_doc: list, nlpipe=None, nlpspa=None):
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    # pipe, spa
    nlpipe = _if_not_pipe(nlpipe)
    nlpspa = _if_not_spacy(nlpspa)

    # choose the item
    h1 = struct_doc["h1"]
    sub_article = "\n".join(struct_doc["article"].split("\n")[:2])

    # token filter h1
    tok_h1 = [i.text.lower() for i in nlpspa(h1)]
    jur_h1 = [_filter_jur(i) for i in tok_h1]
    jur_h1_clean = list(set([i for i in jur_h1 if i]))

    # juri h1
    if len(jur_h1_clean) == 1:
        return jur_h1_clean[0]
    if len(jur_h1_clean) > 1:
        return ",".join(jur_h1_clean)

    # token filter sub_article
    tok_sub_article = [i.text.lower() for i in nlpspa(sub_article)]
    jur_sub_article = [_filter_jur(i) for i in tok_sub_article]
    jur_sub_article_clean = list(set([i for i in jur_sub_article if i]))

    # juri sub_article
    if len(jur_sub_article_clean) == 1:
        return jur_sub_article_clean[0]
    if len(jur_sub_article_clean) > 1:
        return ",".join(jur_sub_article_clean)

    return str(-3)


if __name__ == "__main__":

    # import
    from legal_doc_processing.utils import get_pipeline, get_spacy, get_label_
    from legal_doc_processing.press_release.utils import press_release_X_y
    from legal_doc_processing.press_release.segmentation.structure import (
        structure_press_release,
    )

    # laod
    nlpipe = get_pipeline()
    nlpspa = get_spacy()

    # structured_press_release_r
    df = press_release_X_y(features="juridiction")
    df["structured_txt"] = [structure_press_release(i) for i in df.txt.values]

    # one
    one = df.iloc[0, :]
    # one features
    # cost = one.cost
    one_struct = struct_doc = one.structured_txt
    one_h1 = one_struct["h1"]
    one_article = one_struct["article"]
    sub_one_article = "\n".join(one_article.split("\n")[:2])
    # pred_h1  ⁼ predict_juridiction(one_h1)
    # pred_sub_article  ⁼ predict_juridiction(one_h1)
    pred = predict_juridiction(one_struct, nlpipe=nlpipe, nlpspa=nlpspa)

    # 1 to len(df)
    print(f" {'y'.rjust(30)} -->  {'pred'} \n")
    print(160 * "-")
    for i in range(0, len(df)):
        juridiction = df.juridiction.iloc[i]
        i_text = df.txt.iloc[i]
        i_struct = df["structured_txt"].iloc[i]
        pred_ans = predict_juridiction(i_struct, nlpspa=nlpspa, nlpipe=nlpipe)
        print(f" {str(juridiction).rjust(30)} --> pred : {pred_ans}")
