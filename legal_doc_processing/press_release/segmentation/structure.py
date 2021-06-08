import os
from pprint import pformat, pprint


sep = "---------------------"


def _shall_not_pass(dict_text):

    error = 0
    # len id
    if (len(dict_text["id"]) > 30) or ("--ERROR--" in dict_text["id"]):
        dict_text["id"] = "--ERROR-- " + dict_text["id"]
        error += 1

    # len date
    if (len(dict_text["date"]) > 30) or ("--ERROR--" in dict_text["date"]):
        dict_text["date"] = "--ERROR-- " + dict_text["date"]
        error += 1

    #  Washington in h1 or len h1
    if (
        ("Washington, D" in dict_text["h1"][:19])
        or (len(dict_text["h1"]) > 1000)
        or ("--ERROR--" in dict_text["h1"])
    ):
        dict_text["h1"] = "--ERROR-- " + dict_text["h1"]
        error += 1

    # Washington in article
    if ("Washington, D" not in dict_text["article"][:19]) or (
        "--ERROR--" in dict_text["article"]
    ):
        dict_text["article"] = "--ERROR-- " + dict_text["article"]
        error += 1

    dict_text["error"] = error

    return dict_text


def _clean_lines(lines):
    """ just drop ueseless lines"""

    lines = [i.strip() for i in lines]
    lines = [i for i in lines if i]

    return lines


def _find_release_number(lines):

    idx = [i for i, l in enumerate(lines) if l.lower().startswith("release num")]
    if len(idx) == 1:
        idx = idx[0]
        line = lines[idx]
        release_number = (
            line.lower()
            .replace("release", "")
            .replace("number", "")
            .replace(":", "")
            .strip()
        )
        lines.pop(idx)
        return release_number, lines

    return "--ERROR--", lines


def _find_date(lines):
    """find the date """

    if ("201" in lines[0][:25]) or ("202" in lines[0][:25]) or ("200" in lines[0][:25]):
        idx = 0
        line = lines[idx]
        lines.pop(idx)
        return line, lines

    return "--ERROR--", lines


def _find_article(lines):

    idx = [i for i, l in enumerate(lines) if l.lower().startswith("washington")]
    if len(idx) == 1:
        idx = idx[0]
        article = lines[idx:]
        lines = lines[:idx]
        return article, lines

    return "--ERROR--", lines


def _find_h1(lines):

    lines = [k.strip() for k in lines]
    return " ".join(lines)


def _clean_articles_breaks(lines):

    lines = [i.strip() for i in lines]

    rebreak = lambda txt: str(txt + "\n") if (txt[-1] == ".") else txt
    lines = [rebreak(l) for l in lines]
    text = " ".join(lines)
    text = text.replace(".\n ", ".\n")

    return text


def structure_press_release(
    txt: str, squeeze_break: bool = False, force_dict: bool = True
) -> str:

    # init dd
    dd = {
        "id": "--ERROR--",
        "date": "--ERROR--",
        "h1": "--ERROR--",
        "article": "--ERROR--",
        "error": 0,
    }

    # lines
    lines = txt.splitlines()

    # clean lines
    lines = _clean_lines(lines)
    # split items
    dd["id"], lines = _find_release_number(lines)
    dd["date"], lines = _find_date(lines)
    dd["article"], lines = _find_article(lines)
    dd["h1"] = _find_h1(lines)

    # clean articles
    dd["article"] = _clean_articles_breaks(dd["article"])

    # errors
    dd = _shall_not_pass(dd)

    return dd


if __name__ == "__main__":

    from legal_doc_processing.press_release.utils import press_release_X_y
    from legal_doc_processing.press_release.segmentation.structure import (
        structure_press_release,
    )

    # structured_press_release_list
    df = press_release_X_y(features="defendant")
    # df["structured_txt"] = [structure_press_release(i) for i in df.txt.values]

    # one = df["structured_txt"].iloc[0]
    # one_list = [(k, str(v)[:100] + "...") for k, v in one.items()]
    # one_str = "\n".join([f"{i.rjust(10)}\t:\t{j}" for i, j in one_list])
    # print(one_str)

    txt = df.txt.iloc[0]

    # init dd
    dd = {
        "id": "--ERROR--",
        "date": "--ERROR--",
        "h1": "--ERROR--",
        "article": "--ERROR--",
        "error": 0,
    }

    # lines
    lines = txt.splitlines()

    # clean lines
    lines = _clean_lines(lines)


text = [
    "helo this is",
    "a sentence.",
    "i love this one, but",
    "i need to end ",
    "on a other line.    ",
    "due to wierd word",
]
