import os

import pandas as pd

import legal_doc_processing as ldp
from legal_doc_processing.information_extraction import *
from legal_doc_processing.information_extraction import _ask_who_is
from legal_doc_processing.segmentation import *
from legal_doc_processing.utils import *

from notebooks.packages import *
from notebooks.utils import *


nlpipe = get_pipeline()


def get_press_dummy_defendant(raw_text):
    """extract defendant """

    # extract lines with 'against'
    lines = [
        i.replace("\u200b", "").replace("\t", " ") for i in raw_text.splitlines() if i
    ]
    cands = [i for i in lines[:300] if "against" in i.lower()]

    # sep pred
    preds = [
        k.lower()
        .split("against")[1]
        .split("for")[0]
        .replace("defendant", "")
        .replace("defendants", "")
        .strip()
        .capitalize()
        for k in cands
        if len(k) > 5
    ]

    if preds:
        return preds[0]

    return "-- None --"


def get_press_nlp_defendant(raw_text, nlpipe=None):

    ans = _ask_who_is(raw_text, "defendant", nlpipe=nlpipe)

    return ans[0].get("answer")


if __name__ == "__main__":

    # file_path
    file_path_list = x_data_files(30, "press")

    # read file
    raw_text_list = [load_data(file_path) for file_path in file_path_list]
    raw_text_list[0]

    # clean and first
    clean_pages_list = [clean_doc(raw_text) for raw_text in raw_text_list]
    first_page_list = [pages[0] for pages in clean_pages_list]
    first_page_list[0]
    joined_first_page_list = ["\n".join(l) for l in first_page_list]

    # pred defendant dummy
    pred_dummy_list = [get_press_dummy_defendant(txt) for txt in joined_first_page_list]
    pred_dummy_list

    # zip
    list(zip(file_path_list, pred_dummy_list))

    # pred defendant nlp
    pred_nlp_list = [
        get_press_nlp_defendant(txt, nlpipe=nlpipe) for txt in joined_first_page_list
    ]
    pred_nlp_list

    # zip
    list(zip(file_path_list, pred_nlp_list))

    # pandas
    pseudo_df = list(
        zip(
            map(os.path.basename, file_path_list),
            map(os.path.dirname, [i.replace("data/", "") for i in file_path_list]),
            pred_dummy_list,
            pred_nlp_list,
        )
    )

    df = pd.DataFrame(pseudo_df, columns=["basename", "dir", "pred_pummy", "pred_lnp"])
    df