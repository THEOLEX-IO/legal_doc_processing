import time
import random

import pandas as pd

from legal_doc_processing import press_release as pr
from legal_doc_processing import legal_doc as ld
from legal_doc_processing.utils import get_pipeline, get_spacy


# %time
nlpipe, nlspa = get_pipeline(), get_spacy()


test_press_txt = """
Release Number 7100-15

 

January 12, 2015

Federal Court in Florida Enters Order Freezing Assets in CFTC Foreign Currency Anti-
Fraud Action against Allied Markets LLC and its Principals Joshua Gilliland and Chawalit
Wongkhiao

CFIC Charges Jacksonville, Florida, Defendants with Operating a
Fraudulent Forex Pool and Misappropriating Customer Funds to Pay
Personal Expenses

Washington, DC — The U.S. Commodity Futures Trading Commission (CFTC) today announced that it filed a civil
enforcement Complaint in the U.S. District Court for the Middle District of Florida, charging Defendants Allied Markets
LLC, and its principals Joshua Gilliland and Chawalit Wongkhiao, all of Jacksonville, Florida, with operating a
fraudulent foreign currency (forex) commodity pool in violation of the Commodity Exchange Act (CEA) and CFTC
Regulations. In addition, none of the Defendants has ever been registered with the CFTC, as required.

"""
test_press_obj = pr.PressRelease(test_press_txt, 'cftc', nlpipe=nlpipe, nlspa=nlspa)
test_press_preds = test_press_obj.predict_all()


def decore_preds(obj, i=None, I=None) -> dict:
    """prevents errors  """

    if i and I:
        print(f"{i}/{I}", end=" ")

    t = time.time()
    try:
        print(str(obj.__repr__())[10:70])
        res = obj.predict_all()
        t = round(time.time() - t, 2)
        print((str(res)[:30]), end=" ")
        print(f"---> {t} secs <---\n")
        return res

    except Exception as e:
        t = round(time.time() - t, 2)
        print(e, end=" ")
        print(f"---> {t} secs <---\n")
        return {}


def compute_slices(len_df, batches_size_max=30):
    """ """

    len_df += 1
    batches_nb = len_df // batches_size_max
    slices = len_df // batches_nb
    extra = len_df % batches_nb

    # seps = [(0, 60), (60, 120),(120, 180), (180, 240) ]
    steps = [(i * slices, (i * slices) + slices) for i in range(batches_nb)]
    steps[-1] = (steps[-1][0], steps[-1][1] + extra)
    print(steps)

    return steps


def batch_pred_and_save(df_list, SOURCE, pred_name="__preds"):

    fn_list = list()
    rd = random.randint(1000, 9999)

    # for each sub df
    for i, sub_df in enumerate(df_list):

        print(f"---------\n{i}/{len(df_list)}\n---------\n\n")

        len_k = len(sub_df.press_obj)
        enn = enumerate(sub_df.press_obj)
        fn = f"{SOURCE}/data/csv/__{rd}__{SOURCE}_pred_df_{i}.csv"

        sub_df[pred_name] = [decore_preds(obj, k, len_k) for k, obj in enn]
        sub_df.to_csv(fn, index=False)

        fn_list.append(fn)

        time.sleep(3)

    return fn_list


def decore_dict(dd: dict, k: str) -> str:
    """ """

    try:
        return str(dd[k])
    except:
        return ""


def split_features(df, pred_name="__preds"):
    """ """

    one = df.iloc[0, :]
    keys = list(one[pred_name].keys())
    print(keys)

    for k in keys:
        df[k] = df[pred_name].apply(lambda dd: decore_dict(dd, k))

    return df
