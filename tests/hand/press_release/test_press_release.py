from legal_doc_processing import logger


def test_init():
    """ """

    from legal_doc_processing import logger

    logger.info("called")

    import time

    # load
    from legal_doc_processing.utils import get_pipeline, get_spacy

    nlpipe = get_pipeline()
    nlspa = get_spacy()
    nlspa.add_pipe("sentencizer")

    # dataframe
    from legal_doc_processing.press_release.utils import press_release_X_y

    df = press_release_X_y(juridiction="cftc", sample=0.1)

    # Press Releae
    from legal_doc_processing.press_release.press_release import PressRelease

    # press release
    t = time.time()
    make_pr = lambda i: PressRelease(i, nlpipe=nlpipe, nlspa=nlspa)
    df["pr"] = df.press_release_text.apply(make_pr)
    tt, ttt = round(time.time() - t, 2), round((time.time() - t) / len(df), 2)
    print(f"--> time = {tt} sec soit one obj in average {ttt} sec")
    df.drop(["press_release_text"], axis=1, inplace=True)

    # preds
    t = time.time()
    df["preds"] = df.pr.apply(lambda i: i.predict_all())
    tt, ttt = round(time.time() - t, 2), round((time.time() - t) / len(df), 2)
    print(f"--> time = {tt} sec soit one pred in average {ttt} sec")

    # labels vs "preds"
    preds_labels = list(df.preds.iloc[0].keys())
    for k in preds_labels:
        df["pred_" + k] = df.preds.apply(lambda i: i[k])
    df.drop(["preds"], axis=1, inplace=True)

    # externize
    cols = ["pr", "preds"]
    _df = df.drop(cols, axis=1, inplace=False)
    _df.to_csv("./data/csv/press_release.csv", index=False)
