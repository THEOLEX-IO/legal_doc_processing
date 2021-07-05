def test_init():
    """ """

    import time

    # load
    from legal_doc_processing.utils import get_pipeline, get_spacy

    nlpipe = get_pipeline()
    nlspa = get_spacy()
    nlspa.add_pipe("sentencizer")

    # dataframe
    from legal_doc_processing.press_release.loader import press_release_X_y

    df = press_release_X_y()
    df = df.iloc[:10, :]

    # Press Releae
    from legal_doc_processing.press_release.press_release import PressRelease

    df["pr"] = df.txt.apply(lambda i: PressRelease(i, nlpipe=nlpipe, nlspa=nlspa))