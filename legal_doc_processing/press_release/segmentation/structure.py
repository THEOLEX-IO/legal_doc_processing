import os
from pprint import pformat, pprint


sep = "---------------------"


def _shall_not_pass(structured_text):

    error = 0
    # len id
    if (len(structured_text["id"]) > 30) or ("--ERROR-- " in structured_text["id"]):
        structured_text["id"] = "--ERROR-- " + structured_text["id"]
        error += 1

    # len date
    if (len(structured_text["date"]) > 30) or ("--ERROR-- " in structured_text["date"]):
        structured_text["date"] = "--ERROR-- " + structured_text["date"]
        error += 1

    #  Washington in h1 or len h1
    if (
        ("Washington, D" in structured_text["h1"][:19])
        or (len(structured_text["h1"]) > 1000)
        or ("--ERROR-- " in structured_text["h1"])
    ):
        structured_text["h1"] = "--ERROR-- " + structured_text["h1"]
        error += 1

    # Washington in article
    if ("Washington, D" not in structured_text["article"][:19]) or (
        "--ERROR-- " in structured_text["article"]
    ):
        structured_text["article"] = "--ERROR-- " + structured_text["article"]
        error += 1

    structured_text["error"] = error

    return structured_text


def structure_press_release(
    txt: str, squeeze_break: bool = False, force_dict: bool = True
) -> str:

    dd = {
        "id": "--ERROR--",
        "date": "--ERROR--",
        "h1": "--ERROR--",
        "article": "--ERROR--",
    }

    # errors
    dd = _shall_not_pass(dd)

    return dd


if __name__ == "__main__":

    # import
    from legal_doc_processing.utils import get_pipeline
    from legal_doc_processing.press_release.utils import press_release_X_y
    from legal_doc_processing.press_release.segmentation.structure import (
        structure_press_release,
    )

    # pipe
    nlpipe = get_pipeline()

    # structured_press_release_list
    df = press_release_X_y(features="defendant")
    # df["structured_txt"] = [structure_press_release(i) for i in df.txt.values]

    # one = df["structured_txt"].iloc[0]
    # one_list = [(k, str(v)[:100] + "...") for k, v in one.items()]
    # one_str = "\n".join([f"{i.rjust(10)}\t:\t{j}" for i, j in one_list])
    # print(one_str)
