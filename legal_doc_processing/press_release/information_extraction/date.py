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
    structured_press_release: list,
) -> str:
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    date = structured_press_release["date"]

    date = _you_shall_not_pass(date)
    return date


if __name__ == "__main__":

    # import
    from legal_doc_processing.utils import *
    from legal_doc_processing.press_release.utils import *
    from legal_doc_processing.press_release.segmentation.structure import (
        structure_press_release,
    )

    # structured_press_release_list
    press_txt_list = load_press_release_text_list()
    structured_press_release_list = [structure_press_release(i) for i in press_txt_list]

    # test one
    structured_press_release = structured_press_release_list[0]

    ans = predict_date(structured_press_release)

    # test others
    ans_list = [predict_date(p) for p in structured_press_release_list]
