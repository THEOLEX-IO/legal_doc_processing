from time import time
from legal_doc_processing import logger

from legal_doc_processing.utils import get_spacy, get_pipeline, get_label_


def test_structure(juridiction, sample=0.99):
    """ """

    assert juridiction in ["cftc", "cfbp", "doj", "sec"]

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

    df = press_release_X_y(juridiction=juridiction, sample=sample)
    cols = ["folder", "press_release_text"]
    df = df.loc[:, cols]

    # choose funct
    from legal_doc_processing.press_release.structure.cftc import (
        structure_press_release as structure_cftc,
    )
    from legal_doc_processing.press_release.structure.doj import (
        structure_press_release as structure_doj,
    )

    from legal_doc_processing.press_release.structure.cfbp import (
        structure_press_release as structure_cfbp,
    )

    from legal_doc_processing.press_release.structure.sec import (
        structure_press_release as structure_sec,
    )

    if juridiction == "cftc":
        struct_funct = structure_cftc
    if juridiction == "doj":
        struct_funct = structure_doj
    if juridiction == "sec":
        struct_funct = structure_sec
    if juridiction == "cfbp":
        struct_funct = structure_cfbp

    # structure
    struct_ = lambda i: struct_funct(i, nlspa=nlspa)
    df["dd"] = df.press_release_text.apply(struct_)

    # extrcat cols
    col_list = list(df.dd.iloc[0].keys())
    for col in col_list:
        df["dd_" + col] = df.dd.apply(lambda i: i.get(col, -42))
    df.drop("dd", inplace=True, axis=1)

    # save
    fn = f"./data/csv/structure_press_release_{juridiction}_{len(df)}_lines.csv"
    df.to_csv("./data/csv/structure_press_release_cfbp.csv", index=False)