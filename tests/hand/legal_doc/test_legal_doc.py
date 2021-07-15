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
    from legal_doc_processing.legal_doc.utils import legal_doc_X_y

    df = legal_doc_X_y(juridiction="cftc", sample=0.1)

    # Press Releae
    from legal_doc_processing.legal_doc.legal_doc import LegalDoc

    t = time()
    make_ld = lambda i: LegalDoc(i, nlpipe=nlpipe, nlspa=nlspa)
    df["ld"] = df.legal_doc_text.apply(make_ld)
    tt, ttt = round(time() - t, 2), round((time() - t) / len(df), 2)
    print(f"time: {tt}s, avg obj init: {ttt}s (max_init_time: {max_init_time})s")
    assert ttt < max_init_time

    # preds
    t = time()
    df["preds"] = df.ld.apply(lambda i: i.predict_all())
    tt, ttt = round(time() - t, 2), round((time() - t) / len(df), 2)
    print(f"time: {tt}s, average pred: {ttt}s (max_pred_time: {max_pred_time})s")
    assert ttt < max_pred_time

    # labels vs "preds"
    preds_labels = list(df.preds.iloc[0].keys())
    for k in preds_labels:
        df["pred_" + k] = df.preds.apply(lambda i: i[k])

    # externize
    cols = ["ld", "preds", "legal_doc_text"]
    _df = df.drop(cols, axis=1, inplace=False)
    _df.to_csv("./data/csv/legal_doc.csv", index=False)