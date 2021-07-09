import os
import copy

import pandas as pd

from legal_doc_processing import logger

from legal_doc_processing.utils import uniquize as _u

from legal_doc_processing.press_release.monetary_sanction.clean import _cast_as_int


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


# if __name__ == "__main__":

#     import time

#     import numpy as np
#     import pandas as pd

#     from legal_doc_processing.utils import get_pipeline, get_spacy, cosine_similarity
#     from legal_doc_processing.press_release.utils import press_release_X_y
#     from legal_doc_processing.press_release.press_release import PressRelease

#     from legal_doc_processing.utils import dummy_accuracy

#     # laod
#     nlpipe = get_pipeline()
#     nlspa = get_spacy()
#     nlspa.add_pipe("sentencizer")

#     # structured_press_release_r
#     df = press_release_X_y(features="monetary_sanction")
#     df = df.iloc[:30, :]
#     df["pr"] = [PressRelease(i, nlpipe=nlpipe, nlspa=nlspa) for i in df.txt.values]

#     # preds
#     t = time.time()
#     # 28 objects --> 181 secondes so --> +/-10 secondes per objects
#     df["pred_monetary_sanction"] = df.pr.apply(lambda i: i.predict("monetary_sanction"))
#     t = time.time() - t

#     DF = pd.DataFrame(df)
#     df = pd.DataFrame(DF)

#     _zip = list(
#         zip(
#             df.monetary_sanction.values,
#             [i[0][0] for i in df.pred_monetary_sanction.values],
#         )
#     )

#     pred_performance = pd.Series([dummy_accuracy(i, j) for i, j in _zip])
#     pred_performance.mean()
