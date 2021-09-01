import os

import pandas as pd
from cleantext import clean
from legal_doc_processing.utils import *

from legal_doc_processing import logger

# from legal_doc_processing.legal_doc.segmentation.clean import clean_doc
# from legal_doc_processing.legal_doc.segmentation.utils import get_token, get_section_indx
from legal_doc_processing.utils import load_data
# from legal_doc_processing.legal_doc.segmentation import clean
# from notebooks.utils import *


def structure_legal_doc(text):
    import pdb;pdb.set_trace()
    list_token = get_token(text)
    idx = get_section_indx(list_token)
    j = -1
    structure = []
    k = 0
    for i in idx:
        section = {}
        section["content"] = list_token[j + 1 : i]

        section["header"] = list_token[i] + list_token[i + 1]
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

        structured_text = structure_legal_doc(cleaned_text)
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

    #  dataframe and structured_legal_doc_
    df = legal_doc_X_y(features="defendant")
    df["structured_txt"] = [structure_legal_doc(i) for i in df.txt.values]

    # extract content form paragraph i  and concatenate witj
    concat = "\n-----------------\n"

    get_c = (
        lambda li, i: (f"{concat}".join(li[i]))
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
        if len(li) > i
        else "-1"
    )

    get_c_0 = lambda li: get_c(li, 0)
    get_c_1 = lambda li: get_c(li, 1)

    df["content_0"] = df.structured_txt.apply(
        lambda struct_txt: get_c_0([d["content"] for d in struct_txt])
    )
    df["content_1"] = df.structured_txt.apply(
        lambda struct_txt: get_c_1([d["content"] for d in struct_txt])
    )

    # MAKE DF with results
    content_0_list = []
    for i, fold, txt in zip(range(len(df)), df.folder, df.content_0):
        dd = {"folder": fold, "content_0": txt}
        content_0_list.append(dd)

    content_1_list = []
    for i, fold, txt in zip(range(len(df)), df.folder, df.content_1):
        dd = {"folder": fold, "content_1": txt}
        content_1_list.append(dd)

    result_c0 = pd.DataFrame(content_0_list)
    result_c1 = pd.DataFrame(content_1_list)

    results_c0_c1 = pd.concat([result_c0, result_c1], axis=1, keys="folder")
    results_c0_c1.to_csv(
        "./data/csv/legal_doc_structure_problem_21-06-16.csv", index=False
    )
