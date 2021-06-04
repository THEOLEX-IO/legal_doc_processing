import os


def _double_break_as_para(txt: str) -> str:
    """add a --------- instdead of double break """

    txt = txt.replace("\n\n", "\n---------------------\n")
    txt = txt.replace("\n\n", "\n")
    txt = txt.replace("\n\n", "\n")

    return txt


def _del_empty_lines(txt: str) -> str:
    """ del empty lines """

    l = txt.splitlines()
    l = [i.strip() for i in l]
    l = [i for i in l if i]

    return "\n".join(l)


def _del_double_breaks(txt: str) -> str:
    """del double breaks and double \n\n """

    txt = txt.replace(
        "---------------------\n---------------------\n", "\n---------------------\n"
    )
    txt = txt.replace(
        "---------------------\n---------------------\n", "\n---------------------\n"
    )
    txt = txt.replace("\n\n", "\n")
    txt = txt.replace("\n\n", "\n")

    return txt


def clean_press_release(txt: str) -> str:

    txt = _double_break_as_para(txt)
    txt = _del_empty_lines(txt)
    txt = _del_double_breaks(txt)

    return txt


if __name__ == "__main__":

    from legal_doc_processing.utils import *

    folder_list = os.listdir("./data/files")
    files_list = [
        [
            f"./data/files/{f}/{i}"
            for i in os.listdir(f"./data/files/{f}")
            if ("press" in i) and ("txt" in i)
        ]
        for f in folder_list
    ]
    files_list = [i[0] for i in files_list]

    press_txt_list = [load_data(i) for i in files_list]
    short_press_txt_list = [i[:200] for i in press_txt_list]

    l2 = [double_break_as_para(txt) for txt in short_press_txt_list]
    l3 = [del_empty_lines(txt) for txt in l2]
    l4 = [del_double_breaks(txt) for txt in l3]
