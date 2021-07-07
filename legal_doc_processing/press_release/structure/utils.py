from legal_doc_processing import logger

import re


def clean_in_line_break(txt: str) -> str:
    """transform 'hello comment\nca va'  en 'hello comment ca va' """

    break_ = "--BREAK--"
    endline_ = "--ENDLINE--"

    lines = txt.splitlines()
    lines = [i.strip() for i in lines]
    txt_1 = "\n".join(lines)

    txt_2 = txt_1.replace(".\n", f".{endline_}\n")
    txt_3 = txt_2.replace("\n\n", f"\n{break_}\n")

    txt_4 = txt_3.replace("\n", " ")
    txt_5 = txt_4.replace(f" {break_} ", break_)
    txt_6 = txt_5.replace(f"{break_}", f"\n\n")
    txt_7 = txt_6.replace(f"{endline_}", f"\n")

    txt_8 = txt_7.replace("\n\n", "\n")

    return txt_8


def clean_very_short_lines(txt: str, threshold: int = 5) -> str:
    """clean lines too short """

    lines = txt.splitlines()
    lines = [i.strip() for i in lines if len(i.strip()) > threshold]
    new_txt = "\n".join(lines)

    return new_txt


def do_strip(txt: str) -> str:
    """ """

    lines = txt.splitlines()
    lines = [i.strip() for i in lines]
    new_txt = "\n".join(lines)

    return new_txt


def find_id_line_in_intro(txt: str, len_max=35) -> str:
    """ """

    lines = [i for i in txt.splitlines() if len(i) < len_max]
    idx_list = [i for i, j in enumerate(lines) if j.lower().startswith("Release".lower())]
    if len(idx_list) != 1:
        return -1
    return idx_list[0]


def find_date_line_in_intro(txt: str, len_max=35) -> str:
    """ """

    month_list = [
        "january",
        "febr",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "novembre",
        "december",
    ]
    lines = [i for i in txt.splitlines() if len(i) < len_max]
    idx_list = list()
    for month in month_list:
        cand_list = [i for i, j in enumerate(lines) if month.lower() in j.lower()]
        idx_list.extend(cand_list)

    if len(idx_list) < 1:
        return -1
    return idx_list[0]
