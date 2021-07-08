import os
from pprint import pformat, pprint

from legal_doc_processing import logger

from legal_doc_processing.utils import get_spacy, get_pipeline, get_label_

from legal_doc_processing.press_release.utils import press_release_X_y

from legal_doc_processing.press_release.structure.utils import (
    clean_in_line_break,
    do_strip,
    clean_very_short_lines,
)


def give_sec_press_release_df():
    """ """

    df = press_release_X_y(juridiction="sec", sample=0.9)
    cols = ["folder", "press_release_text"]

    return df.loc[:, cols]


def give_sec_press_release_file():
    """ """

    fn = "./data/files/sec/2020-144/press-release.txt"

    with open(fn, "r") as f:
        txt = f.read()

    btxt = txt.encode("latin-1")
    txt_decoded = btxt.decode("utf8")

    return txt_decoded


def first_clean(txt: str) -> str:
    """ """

    btxt = txt.encode("latin-1")
    txt_decoded = btxt.decode("utf8")

    # # clean double breaks and fake lines
    # new_txt_1 = clean_in_line_break(txt)

    # strip
    new_txt_2 = do_strip(txt_decoded)

    return new_txt_2


def define_sec_press_release_model(txt):
    """ """

    if "FOR IMMEDIATE RELEASE".lower() in txt[:1000].lower():
        return 1
    else:
        return 2


def split_intro_article(txt: str, n=30) -> str:
    """ """

    txt_lines_30 = txt.splitlines()[:n]

    s0, s1, s2 = ("Washington D", "Washington, D", "Washington,D")
    is_in = lambda j: any([(j.startswith(s.lower())) for s in [s0, s1, s2]])
    idx_cands = [i for i, j in enumerate(txt_lines_30) if is_in(j.lower())]

    if not len(idx_cands):
        s = "washington"
        idx_cands = [i for i, j in enumerate(txt_lines_30) if j.lower().startswith(s)]

    idx = idx_cands[0]

    txt_lines = txt.splitlines()
    intro_lines, article_lines = txt_lines[:idx], txt_lines[idx:]

    intro, article = "\n".join(intro_lines), "\n".join(article_lines)

    return intro, article


def structure_press_release(txt, nlspa=""):
    """ """

    # spacy
    if not nlspa:
        nlspa = get_spacy()
    try:
        nlspa.add_pipe("sentencizer")
    except Exception as e:
        pass

    dd = {
        "id": "--ERROR--",
        "date": "--ERROR--",
        "h1": "--ERROR--",
        "article": "--ERROR--",
        "end": "--ERROR--",
        "error": 0,
    }

    sec_model = define_sec_press_release_model(txt)

    if sec_model == 2:

        dd["error"] = "Model not implemented"
        return dd

    try:
        cleaned_txt = first_clean(txt)

    except Exception as e:
        logger.error(e)
        dd["error"] = e

    return dd