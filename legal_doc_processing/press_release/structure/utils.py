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
