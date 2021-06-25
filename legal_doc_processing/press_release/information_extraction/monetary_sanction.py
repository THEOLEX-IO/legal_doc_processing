import os
import copy

import pandas as pd


from legal_doc_processing.utils import uniquize as _u

from legal_doc_processing.press_release.clean.monetary_sanction import _cast_as_int


def predict_monetary_sanction(obj: dict) -> list:
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    # pipe, spa
    nlpipe, nlspa = obj["nlpipe"], obj["nlspa"]

    # items
    h1, abstract = obj["h1"], obj["abstract"]

    # get_label_ h1,predict
    money_h1 = _u(obj["cost_h1"])
    money_h1_clean = _u(_cast_as_int(money_h1))

    # cost in h1
    if len(money_h1_clean) == 1:
        return [(str(money_h1_clean[0]), 1)]
    if len(money_h1_clean) > 1:
        return [(str(-2), 1)]

    # get_label abstract,predict
    money_abstract = _u(obj["cost_abstract"])
    money_abstract_clean = _u(_cast_as_int(money_abstract))

    # cost in article
    if len(money_abstract_clean) == 1:
        return [(str(money_abstract_clean[0]), 1)]
    elif len(money_abstract_clean) > 1:
        return [(str(max(money_abstract_clean)), 1)]
    else:
        return [(str(-1), -1)]

    return [(str(-3),)]


# #     return resp
# if __name__ == "__main__":

#     # import
#     from legal_doc_processing.utils import get_pipeline, get_spacy, get_label_
#     from legal_doc_processing.press_release.loader import press_release_X_y
#     from legal_doc_processing.press_release.structure import structure_press_release

#     # laod
#     nlpipe = get_pipeline()
#     nlspa = get_spacy()

#     # structured_press_release_r
#     df = press_release_X_y(features="cost")
#     df["structured_txt"] = [structure_press_release(i) for i in df.txt.values]

#     # one
#     one = df.iloc[0, :]
#     # one features
#     cost = one.cost
#     one_struct = struct_doc = one.structured_txt
#     one_h1 = one_struct["h1"]
#     one_article = one_struct["article"]
#     sub_one_article = "\n".join(one_article.split("\n")[:2])

#     # # ents
#     # money_h1 = get_label_(one_h1, "MONEY", nlspa)
#     # money_article = get_label_(sub_one_article, "MONEY", nlspa)

#     # # 1 to len(df)
#     # print(f" {'y'.rjust(30)} -->  {'pred'} \n")
#     # print(160 * "-")
#     # for i in range(0, len(df)):
#     #     cost = df.cost.iloc[i]
#     #     i_text = df.txt.iloc[i]
#     #     i_struct = df["structured_txt"].iloc[i]

#     #     i_h1 = i_struct["h1"]
#     #     i_article = i_struct["article"]
#     #     sub_i_article = "\n".join(i_article.split("\n")[:2])
#     #     pred_ans = predict_cost(i_struct, nlspa=nlspa, nlpipe=nlpipe)
#     #     print(f" {str(cost).rjust(30)} --> pred : {pred_ans}")
