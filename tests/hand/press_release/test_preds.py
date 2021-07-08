from time import time
from legal_doc_processing import logger
from legal_doc_processing.utils import get_pipeline, get_spacy
from legal_doc_processing.press_release.utils import press_release_X_y
from legal_doc_processing.press_release.press_release import PressRelease


def test_init_pred(
    juridiction, nlspa="", nlpipe="", sample=0.25, max_init_time=3.0, max_pred_time=11.0
):
    """ """

    assert juridiction in ["cftc", "cfbp", "doj", "sec"]

    max_init_time = 3.0
    max_pred_time = 11.0

    from time import time
    from legal_doc_processing import logger

    logger.info("called")

    # load
    from legal_doc_processing.utils import get_pipeline, get_spacy

    if not nlpipe:
        nlpipe = get_pipeline()
    if not nlspa:
        nlspa = get_spacy()
    try:
        nlspa.add_pipe("sentencizer")
    except Exception as e:
        pass

    # dataframe
    from legal_doc_processing.press_release.utils import press_release_X_y

    df = press_release_X_y(juridiction=juridiction, sample=sample)

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
    fn = f"./tmp/preds_press_release_{juridiction}_{len(_df)}_lines.csv"
    _df.to_csv(fn, index=False)


if __name__ == "__main__":

    from time import time
    from legal_doc_processing import logger
    from legal_doc_processing.utils import get_pipeline, get_spacy

    nlpipe = get_pipeline()
    nlspa = get_spacy()
    nlspa.add_pipe("sentencizer")

    # auth_list = ["cftc", "cfbp", "doj", "sec"]
    # _ = [test_init_pred(i, sample=0.1, nlspa=nlspa, nlpipe=nlpipe) for i in auth_list]

    test_init_pred("doj", sample=0.1, nlspa=nlspa, nlpipe=nlpipe)
