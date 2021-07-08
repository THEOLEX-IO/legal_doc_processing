from time import time
from legal_doc_processing import logger


def test_init(max_init_time=3.0, max_pred_time=11.0):
    """ """

    max_init_time = 3.0
    max_pred_time = 11.0

    from time import time
    from legal_doc_processing import logger

    logger.info("called")

    # load
    from legal_doc_processing.utils import get_pipeline, get_spacy

    nlpipe = get_pipeline()
    nlspa = get_spacy()
    nlspa.add_pipe("sentencizer")

    # dataframe
    from legal_doc_processing.press_release.utils import press_release_X_y

    df = press_release_X_y(juridiction="doj", sample=0.1)

    # Press Releae
    from legal_doc_processing.press_release.press_release import PressRelease

    t = time()
    make_pr = lambda i: PressRelease(i, nlpipe=nlpipe, nlspa=nlspa)
    df["pr"] = df.press_release_text.apply(make_pr)
    tt, ttt = round(time() - t, 2), round((time() - t) / len(df), 2)
    print(f"time: {tt}s, avg obj init: {ttt}s (max_init_time: {max_init_time})s")
    assert ttt < max_init_time

    # preds
    t = time()
    df["preds"] = df.pr.apply(lambda i: i.predict_all())
    tt, ttt = round(time() - t, 2), round((time() - t) / len(df), 2)
    print(f"time: {tt}s, average pred: {ttt}s (max_pred_time: {max_pred_time})s")
    assert ttt < max_pred_time

    # labels vs "preds"
    preds_labels = list(df.preds.iloc[0].keys())
    for k in preds_labels:
        df["pred_" + k] = df.preds.apply(lambda i: i[k])

    # externize
    cols = ["pr", "preds", "press_release_text"]
    _df = df.drop(cols, axis=1, inplace=False)
    _df.to_csv("./data/csv/press_release_doj.csv", index=False)
