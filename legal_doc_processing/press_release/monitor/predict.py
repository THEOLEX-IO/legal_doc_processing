from legal_doc_processing import logger


def predict_monitor(obj: dict) -> list:
    """ """

    monitor = 0

    for sent in obj["all_text_sents"]:
        if (
            ("indepen" in sent.lower())
            and ("complian" in sent.lower())
            and ("monitor" in sent.lower())
        ):
            monitor += 1

    return [("1", 0.8)] if monitor else [("0", 0.8)]


# if __name__ == "__main__":

#     import time
#     import pandas as pd
#     from legal_doc_processing.utils import get_pipeline, get_spacy
#     from legal_doc_processing.press_release.utils import press_release_X_y
#     from legal_doc_processing.press_release.press_release import PressRelease

#     # load
#     nlpipe = get_pipeline()
#     nlspa = get_spacy()
#     nlspa.add_pipe("sentencizer")

#     # legal_doc df AND  OBj
#     df = press_release_X_y()
#     df = df.iloc[:, :]
#     df["pr"] = df.txt.apply(lambda i: PressRelease(i, nlpipe=nlpipe, nlspa=nlspa))

#     # preds
#     t = time.time()
#     # 28 objects --> 181 secondes so --> +/-10 secondes per objects
#     df["pred_monitor"] = df.pr.apply(lambda i: i.predict("monitor"))
#     t = time.time() - t

#     # 1st one
#     one = df.iloc[0, :]
#     one_txt = one.txt
#     one_ob = obj = self = one.pr

#     # externize
#     cols = ["txt", "pr", "preds"]
#     _df = df.drop(cols, axis=1, inplace=False)
