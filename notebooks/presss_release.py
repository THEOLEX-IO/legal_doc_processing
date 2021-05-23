#!/usr/bin/env python
# coding: utf-8

# ## 1 - Impots
# --------------------


# import legal_doc_processing as ldp
# from legal_doc_processing.information_extraction import *
# from legal_doc_processing.segmentation import *
# from legal_doc_processing.utils import *


from notebooks.packages import *
from notebooks.paths import *

# path and fn
file_path = os.getcwd() + "/data"
cands = [i for i in os.listdir(file_path) if "press" in i]
assert len(cands) == 1
filename = cands[0]
one_file_path = file_path + "/" + filename


# read file
raw_text = load_data(one_file_path)
# raw_text[:300]


def extract_defendant(raw_text):
    """extract defendant """

    # extract lines with 'against'
    lines = [
        i.replace("\u200b", "").replace("\t", " ") for i in raw_text.splitlines() if i
    ]
    cands = [i for i in lines[:300] if "against" in i.lower()]

    # sep pred
    preds = [(k.split("against")[1]).strip() for k in cands if len(k) > 10]
    pred = preds[0]

    return pred
