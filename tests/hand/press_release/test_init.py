from time import time
from legal_doc_processing import logger
from legal_doc_processing.utils import get_pipeline, get_spacy
from legal_doc_processing.press_release.utils import press_release_X_y
from legal_doc_processing._press_release import PressRelease


def test_init_by(juridiction="", nlspa="", nlpipe="", sample=0.25, max_init_time=3.0):
    """ """

    assert juridiction in ["cftc", "cfbp", "doj", "sec", ""]

    max_init_time = 3.0

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
    from legal_doc_processing._press_release import PressRelease

    t = time()
    juri = juridiction
    if juridiction:
        make_pr = lambda i: PressRelease(i, source=juri, nlpipe=nlpipe, nlspa=nlspa)
        df["pr"] = df.press_release_text.apply(make_pr)
    else:
        make_pr = lambda i, j: PressRelease(i, source=j, nlpipe=nlpipe, nlspa=nlspa)
        df["pr"] = [make_pr(i, j) for i, j in zip(df.press_release_text, df.juridiction)]

    tt, ttt = round(time() - t, 2), round((time() - t) / len(df), 2)
    print(
        f"time: {tt}s, n objs : {len(df)}, avg obj init: {ttt}s (max_init_time: {max_init_time})s"
    )
    assert ttt < max_init_time

    return df


if __name__ == "__main__":

    from time import time
    from legal_doc_processing import logger
    from legal_doc_processing.utils import get_pipeline, get_spacy

    nlpipe = get_pipeline()
    nlspa = get_spacy()
    nlspa.add_pipe("sentencizer")

    # auth_list = ["cftc", "cfbp", "doj", "sec"]
    # _ = [test_preds(i, sample=0.1, nlspa=nlspa, nlpipe=nlpipe) for i in auth_list]

    df = test_init_by(sample=1, nlspa=nlspa, nlpipe=nlpipe)

    sent_funct = lambda pr: [
        i.text for i in nlspa(pr.struct_text["article"]).sents if i.text.strip()
    ]

    df["sents"] = df.pr.apply(sent_funct)

    coop_fuct = lambda sent_list: any(
        [("coopera" in i) and ("credit" in i) for i in sent_list]
    )
    idxs = df.sents.apply(coop_fuct)

    coop_df = df.loc[idxs, :]

    txt = """The criminal monetary penalty for Novartis Greece reflects a 25 percent reduction off a point near the midpoint of the U.S. Sentencing
    Guidelines range because, although Novartis Greece fully cooperated and remediated, its parent company Novartis AG was involved in similar
    conduct for which it previously reached a resolution with the SEC in March 2016."""

    from legal_doc_processing.utils import ask_all

    quest_pairs = [("what is the reduction due to cooperation?", "coop")]

    ans = ask_all(txt, quest_pairs, nlpipe)
