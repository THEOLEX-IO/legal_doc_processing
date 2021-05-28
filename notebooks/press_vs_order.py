import os

import pandas as pd

import legal_doc_processing as ldp
import legal_doc_processing.information_extraction as infext
import legal_doc_processing.segmentation as seg
import legal_doc_processing.utils as utls
from legal_doc_processing.information_extraction import _ask_who_is

from notebooks.packages import *
from notebooks.utils import *
from notebooks.press_release import get_press_dummy_defendant, get_press_nlp_defendant


nlpipe = get_pipeline()

if __name__ == "__main__":

    # press_list df
    press_list = pd.DataFrame(
        [
            {"root": str(os.path.dirname(i)), "press_file": os.path.basename(i)}
            for i in x_data_files(50, "press")
        ]
    )
    press_list.set_index("root", inplace=True)

    # order_list df
    order_list = pd.DataFrame(
        [
            {"root": str(os.path.dirname(i)), "order_file": os.path.basename(i)}
            for i in x_data_files(50, "order")
        ]
    )
    order_list.set_index("root", inplace=True)

    # join in a df
    df = pd.concat(
        [order_list, press_list],
        join="inner",
        axis=1,
    )
    df["root"] = [str(i) for i in df.index.values]
    df.index = range(len(df))

    # preds labmda
    jawad_preds = lambda ser: (
        ldp.read_file(ser.root + "/" + ser.order_file, nlpipe=nlpipe)
    ).predict_defendant()

    press_dummy_pred = lambda ser: get_press_dummy_defendant(
        utls.load_data(ser.root + "/" + ser.press_file)
    )

    press_nlp_pred = lambda ser: get_press_nlp_defendant(
        utls.load_data(ser.root + "/" + ser.press_file), nlpipe=nlpipe
    )

    # make preds
    df["jawad_preds"] = df.apply(jawad_preds, axis=1)
    df["press_dummy_preds"] = df.apply(press_dummy_pred, axis=1)
    df["press_nlp_preds"] = df.apply(press_nlp_pred, axis=1)
