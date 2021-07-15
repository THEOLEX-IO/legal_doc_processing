from time import time

from legal_doc_processing import logger

from legal_doc_processing.utils import get_pipeline, get_spacy
from legal_doc_processing.base.base import Base
from legal_doc_processing.press_release.utils import press_release_X_y


class PressRelease(Base):
    """main press release doc class """

    def __init__(
        self,
        text: str,
        source: str,
        nlpipe=None,
        nlspa=None,
        n_lines: int = 6,
    ):

        Base.__init__(
            self,
            text=text,
            obj_name="PressRelease",
            source=source,
            nlpipe=nlpipe,
            nlspa=nlspa,
        )

        # set all
        self.set_all()


def press_release_df(juridiction="", nlspa="", nlpipe="", sample=0.25, max_init_time=3.0):
    """ """

    assert juridiction in ["cftc", "cfbp", "doj", "sec", ""]

    max_init_time = 3.0

    # load
    if not nlpipe:
        nlpipe = get_pipeline()
    if not nlspa:
        nlspa = get_spacy()
    try:
        nlspa.add_pipe("sentencizer")
    except Exception as e:
        pass

    # dataframe
    df = press_release_X_y(juridiction=juridiction, sample=sample)

    # Press Releae

    juri = juridiction.lower().strip()
    if juridiction:
        # selec juridiction
        select_jur = lambda i: str(i).lower().strip() == juri
        df = df.loc[df.juridiction.apply(select_jur), :]
        # make pr
        make_pr = lambda i: PressRelease(i, source=juri, nlpipe=nlpipe, nlspa=nlspa)
        df["pr"] = df.press_release_text.apply(make_pr)
    else:
        # make pr
        make_pr = lambda i, j: PressRelease(i, source=j, nlpipe=nlpipe, nlspa=nlspa)
        df["pr"] = [make_pr(i, j) for i, j in zip(df.press_release_text, df.juridiction)]

    return df


# def from_file(file_path, source, nlpipe=None, nlspa=None):
#     return base_from_file(file_path, source, PressRelease, nlpipe=nlpipe, nlspa=nlspa)


# def from_text(txt, source, nlpipe=None, nlspa=None):
#     return base_from_text(txt, source, PressRelease, nlpipe=nlpipe, nlspa=nlspa)


# def from_url(txt, source, nlpipe=None, nlspa=None):
#     return base_from_url(txt, source, PressRelease, nlpipe=nlpipe, nlspa=nlspa)


class _PressRelease:
    PressRelease = PressRelease
    load_X_y = press_release_X_y