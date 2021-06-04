import os


sep = "---------------------"


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

    return txt.split(sep)


def structure_press_release(txt: str) -> str:

    txt = _double_break_as_para(txt)
    txt = _del_empty_lines(txt)
    txt = _del_double_breaks(txt)
    txt = _force_strip(txt)
    lines = _split_by_para(txt)

    return lines


# if __name__ == "__main__":

#     from legal_doc_processing.utils import *

#     folder_list = os.listdir("./data/files")
#     files_list = [
#         [
#             f"./data/files/{f}/{i}"
#             for i in os.listdir(f"./data/files/{f}")
#             if ("press" in i) and ("txt" in i)
#         ]
#         for f in folder_list
#     ]
#     files_list = [i[0] for i in files_list]

#     press_txt_list = [load_data(i) for i in files_list]
#     short_press_txt_list = [i[:200] for i in press_txt_list]

#     l2 = [_double_break_as_para(txt) for txt in short_press_txt_list]
#     l3 = [_del_empty_lines(txt) for txt in l2]
#     l4 = [_del_double_breaks(txt) for txt in l3]

#     cleaned_short_press_release_list = [
#         structure_press_release(i) for i in short_press_txt_list
#     ]
