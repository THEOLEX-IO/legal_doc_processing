def predict_monitor(obj: dict) -> list:
    """ """

    monitor = 0

    for sent in obj["all_text_sents"]:
        if ("indepen" in sent) and ("complian" in sent) and ("monitor" in sent):
            monitor += 1

    return [("1", 0.5)] if monitor else [("0", 0.5)]


if __name__ == "__main__":

    import time
    import pandas as pd
    from legal_doc_processing.utils import get_pipeline, get_spacy
    from legal_doc_processing.press_release.loader import press_release_X_y
    from legal_doc_processing.press_release.press_release import PressRelease

    # load
    nlpipe = get_pipeline()
    nlspa = get_spacy()
    nlspa.add_pipe("sentencizer")

    # legal_doc df AND  OBj
    df = press_release_X_y()
    df = df.iloc[:, :]
    df["pr"] = df.txt.apply(lambda i: PressRelease(i, nlpipe=nlpipe, nlspa=nlspa))

    # preds
    t = time.time()
    # 28 objects --> 181 secondes so --> +/-10 secondes per objects
    df["pred_monitor"] = df.pr.apply(lambda i: i.predict("monitor"))
    t = time.time() - t

    # 1st one
    one = df.iloc[0, :]
    one_txt = one.txt
    one_ob = obj = self = one.pr

    # externize
    cols = ["txt", "pr", "preds"]
    _df = df.drop(cols, axis=1, inplace=False)

    _zip = zip(df.monitor.values, df.pred_monitor.values)
    pred_performance = pd.Series([i==j for i, j in _zip])
    pred_performance.mean()


    
