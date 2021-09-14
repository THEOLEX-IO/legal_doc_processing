import random
from time import time

from legal_doc_processing import logger

from legal_doc_processing.utils import get_pipeline, get_spacy
from legal_doc_processing.press_release.press_release import (
    PressRelease,
    press_release_df,
)
import pytest

# @pytest.mark.skip(reason="no way of currently testing this")
@pytest.mark.xfail(raises=ValueError)
def test_preds_by(
    juridiction="", nlspa=None, nlpipe=None, sample=0.25, max_pred_time=11.0
):
    """ """

    logger.info("called")

    juridiction = ""
    nlspa = None
    nlpipe = None
    sample = 0.1
    max_pred_time = 11.0

    if juridiction not in ["cftc", "cfbp", "doj", "sec", ""]:
        raise AssertionError

    if not nlpipe:
        nlpipe = get_pipeline()
    if not nlspa:
        nlspa = get_spacy()

    df = press_release_df(
        juridiction=juridiction, sample=sample, nlspa=nlspa, nlpipe=nlpipe
    )

    t = time()
    df["preds"] = df.pr.apply(lambda i: i.predict_all())
    tt, ttt = round(time() - t, 2), round((time() - t) / len(df), 2)
    print(
        f"time: {tt}s, n objs : {len(df)}, average pred: {ttt}s (max_pred_time: {max_pred_time})s"
    )
    if ttt >= max_pred_time:
        raise AssertionError

    # labels vs "preds"
    preds_labels = list(df.preds.iloc[0].keys())
    for k in preds_labels:
        df["pred_" + k] = df.preds.apply(lambda i: i[k])

    # externize
    cols = ["pr", "preds", "press_release_text"]
    _df = df.drop(cols, axis=1, inplace=False)
    ra = random.randint(1000, 9999)
    fn = f"./tmp/preds_press_release_{juridiction}_{len(_df)}_lines_{ra}.csv"
    _df.to_csv(fn, index=False)


if __name__ == "__main__":

    nlpipe = get_pipeline()
    nlspa = get_spacy()
    nlspa.add_pipe("sentencizer")

    auth_list = ["cftc", "cfbp", "doj", "sec"]
    try:
        _ = [test_preds_by(i, sample=0.1, nlspa=nlspa, nlpipe=nlpipe) for i in auth_list]
    except:
        pass
    # test_preds_by("cftc", sample=0.1, nlspa=nlspa, nlpipe=nlpipe)
