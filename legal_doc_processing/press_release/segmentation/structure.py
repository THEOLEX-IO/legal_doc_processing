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


def _double_break_as_para(txt: str, sep: str = "---------------------") -> str:
    """add a --------- instdead of double break """

    txt = txt.replace("\n\n", f"\n{sep}\n")
    txt = txt.replace("\n\n", "\n")
    txt = txt.replace("\n\n", "\n")

    return txt


def _del_empty_lines(txt: str) -> str:
    """del empty lines """

    l = txt.splitlines()
    l = [i.strip() for i in l]
    l = [i for i in l if i]

    return "\n".join(l)


def _del_double_breaks(txt: str, sep: str = "---------------------") -> str:
    """del double breaks and double \n\n """

    txt = txt.replace(f"{sep}\n{sep}\n", f"\n{sep}\n")
    txt = txt.replace(f"{sep}\n{sep}\n", f"\n{sep}\n")
    txt = txt.replace("\n\n", "\n")
    txt = txt.replace("\n\n", "\n")

    return txt


def _force_strip(txt: str) -> str:
    """force a strip of each line """

    lines = txt.splitlines()
    txt = "\n".join([i.strip() for i in lines])

    return txt


def _split_by_para(txt: str, sep: str = "---------------------") -> list:
    """split a txt in list with ------ sep """

    txt = txt.replace("\n" + sep + "\n", sep)
    lines = txt.split(sep)

    return lines


def _squeeze_fake_break(txt: str) -> str:
    """try to squeeze fake \n and have good sentece structure
    example 'this is\n a sentence' become 'this is a sentence'"""

    txt = txt.replace(".\n", "!!!!!")
    txt = txt.replace("\n", " ")
    txt = txt.replace("!!!!!", ".\n")

    return txt


def _build_press_release(
    lines: list,
    squeeze_break: bool = True,
) -> dict:
    """create a dict of key, values """

    dd = {}
    key_i_list = [
        ("id", 0),
        ("date", 1),
        ("h1", 2),
        ("h2", 3),
        ("update", -1),
        ("contact", -2),
    ]
    for key, i in key_i_list:
        dd[key] = lines[i] if not squeeze_break else _squeeze_fake_break(lines[i])

    _lines = [_squeeze_fake_break(i) for i in lines[4:-2]]
    dd["article"] = "\n".join(_lines)

    return dd


def structure_press_release(
    txt: str, squeeze_break: bool = False, force_dict: bool = True
) -> str:

    txt = _double_break_as_para(txt)
    txt = _del_empty_lines(txt)
    txt = _del_double_breaks(txt)
    txt = _force_strip(txt)
    lines = _split_by_para(txt)

    if squeeze_break:
        lines = [_squeeze_fake_break(txt) for txt in lines]

    if force_dict:
        dd = _build_press_release(lines)

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
    df["structured_txt"] = [structure_press_release(i) for i in df.txt.values]

    one = df["structured_txt"].iloc[0]
    one_list = [(k, str(v)[:100] + "...") for k, v in one.items()]
    one_str = "\n".join([f"{i.rjust(10)}\t:\t{j}" for i, j in one_list])
    print(one_str)

    # df["id"] = df.structured_txt.apply(lambda i: i.get("id")[:100])
    # df["date"] = df.structured_txt.apply(lambda i: i.get("date")[:100])
