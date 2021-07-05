import os

import dateparser
from legal_doc_processing.press_release.clean.decision_date import (
    _you_shall_not_pass,
)


def predict_decision_date(obj: dict) -> list:
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    date = obj["struct_text"]["date"]
    date = _you_shall_not_pass(date)

    return [(str(dateparser.parse(date)), 1)]


# if __name__ == "__main__":

#     # import
#     from legal_doc_processing.press_release.utils import press_release_X_y
#     from legal_doc_processing.press_release.structure import (
#         structure_press_release,
#     )

#     # structured_press_release_r
#     df = press_release_X_y(features="cost")
#     df["structured_txt"] = [structure_press_release(i) for i in df.txt.values]

#     df["date"] = df["structured_txt"].apply(lambda i: i["date"])
#     df["pred_date"] = df["structured_txt"].apply(lambda i: predict_decision_date(i))
