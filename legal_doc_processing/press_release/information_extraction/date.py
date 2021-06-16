import os


def _you_shall_not_pass(date):
    """avoid passing for a studid algo """

    # validation funct
    funct = lambda i: True if str(i) in date else False

    # features to validate
    features = [(range(1979, 2023), "years"), (range(1, 32), "day")]

    # if a feature not in date retunr --None--
    for feat, _ in features:
        is_ok = bool(sum([funct(i) for i in feat]))
        if not is_ok:
            return "--None--"

    return date


def predict_date(
    struct_doc: list,
) -> str:
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    date = struct_doc["date"]

    date = _you_shall_not_pass(date)
    return date


if __name__ == "__main__":

    # import
    from legal_doc_processing.press_release.utils import press_release_X_y
    from legal_doc_processing.press_release.segmentation.structure import (
        structure_press_release,
    )

    # struct_doc_list and date
    df = press_release_X_y(features="defendant")
    df["structured_txt"] = [structure_press_release(i) for i in df.txt.values]
    df["date"] = df["structured_txt"].apply(lambda i: i["date"])
    df["pred_date"] = df["structured_txt"].apply(lambda i: predict_date(i))
