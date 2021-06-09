import os
from pprint import pformat, pprint


def _shall_not_pass(dict_text: dict) -> dict:
    """avoid obvious stupid predictions """

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

    # update error count
    dict_text["error"] = error

    return dict_text


def _from_txt_to_lines(txt: str) -> list:
    """split lines but smarter  """

    txt = txt.replace("\n\n", "\n").replace("\n\n", "\n")
    lines = txt.splitlines()

    return lines


def _clean_lines(lines: list) -> list:
    """ just drop ueseless lines"""

    lines = [i.strip() for i in lines]
    lines = [i for i in lines if i]
    sep = 8
    lines_0 = [i for i in lines[:sep] if len(i) >= 7]
    lines_1 = lines[sep:]

    return lines_0 + lines_1


def _find_release_number(lines: list) -> tuple:

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


def _find_date(lines: list) -> tuple:
    """find the date """

    for i in range(0, 6):
        if (
            ("201" in lines[i][:25])
            or ("202" in lines[i][:25])
            or ("200" in lines[i][:25])
        ):
            idx = i
            line = lines[idx].strip()
            lines.pop(idx)

            return line, lines

    return "--ERROR--", lines


def _find_article(lines: list) -> tuple:

    idx = [i for i, l in enumerate(lines) if l.lower().startswith("washington")]
    if len(idx) == 1:
        idx = idx[0]
        article = lines[idx:]
        lines = lines[:idx]

        return article, lines

    return "--ERROR--", lines


def _find_h1(lines: list) -> str:

    lines = [k.strip() for k in lines]

    return " ".join(lines)


def _clean_articles_breaks(lines: list) -> str:

    lines = [i.strip() for i in lines]

    rebreak = lambda txt: str(txt + "\n") if (txt[-1] == ".") else txt
    lines = [rebreak(l) for l in lines]
    text = " ".join(lines)
    text = text.replace(".\n ", ".\n")

    return text


def structure_press_release(txt: str) -> dict:

    # init dd
    dd = {
        "id": "--ERROR--",
        "date": "--ERROR--",
        "h1": "--ERROR--",
        "article": "--ERROR--",
        "error": 0,
    }

    # lines
    lines = _from_txt_to_lines(txt)

    # clean lines
    lines = _clean_lines(lines)
    dd["lines"] = lines

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

    # import
    from legal_doc_processing.press_release.utils import press_release_X_y
    from legal_doc_processing.press_release.segmentation.structure import (
        structure_press_release,
    )

    # structured_press_release_list
    df = press_release_X_y(features="defendant")
    df["structured_txt"] = [structure_press_release(i) for i in df.txt.values]

    # one
    one_text = df.txt.iloc[0]
    one_struct = df["structured_txt"].iloc[0]
    one_list = [(k, str(v)[:100] + "...") for k, v in one_struct.items()]
    one_str = "\n".join([f"{i.rjust(10)}\t:\t{j}" for i, j in one_list])
    print(one_str + "\n")

    # two to five
    for i in range(1, 6):
        i_text = df.txt.iloc[i]
        i_struct = df["structured_txt"].iloc[1]
        i_list = [(k, str(v)[:100] + "...") for k, v in i_struct.items()]
        i_str = "\n".join([f"{i.rjust(10)}\t:\t{j}" for i, j in i_list])
        print(i_str + "\n")

    # all
    df["_id"] = df.structured_txt.apply(lambda i: i["id"])
    df["date"] = df.structured_txt.apply(lambda i: i["date"])
    df["h1"] = df.structured_txt.apply(lambda i: i["h1"])
    df["article"] = df.structured_txt.apply(lambda i: i["article"])
    df["lines"] = df.structured_txt.apply(lambda i: i["lines"])

    df["error"] = df.structured_txt.apply(lambda i: i["error"])

    # df._id
    # df.date
    # df.h1
    # df.article
    # df.error

    # find errors
    df_errors = df.loc[df.error > 0, :]
