from cleantext import clean
from legal_doc_processing.utils import *


from legal_doc_processing.legal_doc.segmentation.clean import clean_doc
from legal_doc_processing.legal_doc.segmentation.utils import *


def get_structure(text):
    """ """

    list_token = get_token(text)
    idx = get_section_indx(list_token)
    j = 0

    structure = []
    k = 0
    for i in idx:
        section = {}
        section["content"] = " ".join(list_token[j:i])
        section["header"] = list_token[j]
        section["id"] = k
        structure.append(section)
        j = i
        k = k + 1

    return structure


def get_structured_document(file):
    """ """

    text_structured = []
    file_cleaned = clean_doc(file)
    i = 0
    text_ = {}
    continu = []
    sec_num = 0
    while sec_num < len(file_cleaned):
        if is_title(file_cleaned[sec_num][0]):
            continu.append(file_cleaned[sec_num])
            text_["hearder"] = file_cleaned[sec_num][0]
            sec_num += 1
            while not is_title(file_cleaned[sec_num][0]) and sec_num < (
                len(file_cleaned)
            ):
                continu.append(file_cleaned[sec_num])
                sec_num += 1
            if is_title(file_cleaned[sec_num][0]):
                text_["content"] = continu
                text_["id"] = i
                text_["hearder"] = file_cleaned[sec_num][0]
                sec_num += 1
                continu = []
                i += 1
            else:
                text_["content"] = continu
                text_["id"] = i

        text_structured.append(text_)

    return text_structured
