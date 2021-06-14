from cleantext import clean
from legal_doc_processing.utils import *


from legal_doc_processing.legal_doc.segmentation.clean import clean_doc
from legal_doc_processing.legal_doc.segmentation.utils import get_token, get_section_indx
from legal_doc_processing.utils import load_data
from legal_doc_processing.legal_doc.segmentation import clean

def get_structure(text):
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
    if len(section)==0:
      print("This file is empty")
      return 0
    elif len(section)>2:
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
  list_files=x_data_files(root="data/files/")
  for data in list_files:
    raw_text = load_data(data)
    #clean_spec_chars
    cleaned_text = clean_spec_chars(raw_text)

    structured_text = get_structure(cleaned_text)
    header=get_header(structured_text)
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
