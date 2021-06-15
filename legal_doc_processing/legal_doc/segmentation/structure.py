import os

from cleantext import clean
from legal_doc_processing.utils import *


from legal_doc_processing.legal_doc.segmentation.clean import clean_doc
from legal_doc_processing.legal_doc.segmentation.utils import get_token, get_section_indx
from legal_doc_processing.utils import load_data
from legal_doc_processing.legal_doc.segmentation import clean
from notebooks.utils import *


def structure_legal_doc(text):
    """"""

    list_token = get_token(text)
    idx = get_section_indx(list_token)

    j = 0
    structure = []
    k = 0

    for i in idx:
        section = {}
        section["content"] = list_token[j : i + 1]
        section["header"] = list_token[i]
        section["id"] = k
        structure.append(section)
        j = i + 1
        k = k + 1

    return structure


def get_header(section):

    """ """
    if len(section) == 0:
        print("This file is empty")
        return 0
    elif len(section) > 2:
        sec0 = "".join(section[0]["content"])
        sec1 = "".join(section[1]["content"])
        entete = [sec0]
        entete.append(sec1)
        header = "".join(entete)
    else:
        sec0 = "".join(section[0]["content"])
        entete = [sec0]
        header = "".join(entete)
    return header


def test_structure(root="./data/files/"):
    list_files = x_data_files(root="data/files/")
    for data in list_files:
        raw_text = load_data(data)
        # clean_spec_chars
        cleaned_text = clean_spec_chars(raw_text)

        structured_text = get_structure(cleaned_text)
        header = get_header(structured_text)
        print(structured_text[:5], "\n", header)
        print("\n................\n")


# def get_structured_document(file):
#     """ """

#     text_structured = []
#     file_cleaned = clean_doc(file)
#     i = 0
#     text_ = {}
#     continu = []
#     sec_num = 0
#     while sec_num < len(file_cleaned):
#         if is_title(file_cleaned[sec_num][0]):
#             continu.append(file_cleaned[sec_num])
#             text_["hearder"] = file_cleaned[sec_num][0]
#             sec_num += 1
#             while not is_title(file_cleaned[sec_num][0]) and sec_num < (
#                 len(file_cleaned)
#             ):
#                 continu.append(file_cleaned[sec_num])
#                 sec_num += 1
#             if is_title(file_cleaned[sec_num][0]):
#                 text_["content"] = continu
#                 text_["id"] = i
#                 text_["hearder"] = file_cleaned[sec_num][0]
#                 sec_num += 1
#                 continu = []
#                 i += 1
#             else:
#                 text_["content"] = continu
#                 text_["id"] = i

#         text_structured.append(text_)

#     return text_structured


if __name__ == "__main__":

    # import
    from legal_doc_processing.legal_doc.utils import legal_doc_X_y

    # structured_legal_doc_r
    df = legal_doc_X_y(features="defendant")
    df["structured_txt"] = [structure_legal_doc(i) for i in df.txt.values]

    # one
    one = df.iloc[0, :]
    one_folder = one.folder
    one_defendant = one.defendant
    one_text = one.txt
    one_struct = one.structured_txt

    # -------------------------
    # explore
    # -------------------------

    # 1st level
    type(one_struct)
    len(one_struct)

    # 2nd level
    type(one_struct[0])
    len(one_struct[0])
    # _ = print([type(d) for d in one_struct])
    # _ = print([len(d) for d in one_struct])

    # 3rd level (content)
    type(one_struct[0]["content"])
    len(one_struct[0]["content"])
    # _ = print([type(d["content"]) for d in one_struct])

    # for i_struct in df.structured_txt:
    #     print([len(d["content"]) for d in i_struct])

    get_c_0 = lambda li: "\n-----------------\n".join(li[0]) if len(li) > 0 else "-1"
    get_c_1 = lambda li: "\n-----------------\n".join(li[1]) if len(li) > 1 else "-1"

    df["content_0"] = df.structured_txt.apply(
        lambda struct_txt: get_c_0([d["content"] for d in struct_txt])
    )

    df["content_1"] = df.structured_txt.apply(
        lambda struct_txt: get_c_1([d["content"] for d in struct_txt])
    )

    os.system("clear")
    for tt in df.content_0:
        print(str(tt + "\n\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n"))
        input()
        os.system("clear")

    # keys = [list(i.keys()) for i in one_struct]

    # resume = (
    #     lambda dd: f"{dd['id']}\nheader {dd['header'][:30]}\ncontent {dd['content'][:130]}\n {str(30*'-')}\n "
    # )
    # resumed_struct = [resume(dd) for dd in one_struct]

    # _ = [print(i) for i in resumed_struct]

    # concat_content = ["**!!!**".join(i["content"]) for i in one_struct]

    # concat_content[0]

    # threshold = 500

    # concat_long_content = [i for i in concat_content if len(i) > threshold]

    # exploitatble = concat_long_content[0]