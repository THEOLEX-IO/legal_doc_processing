import os
from pprint import pformat, pprint

from legal_doc_processing import logger

from legal_doc_processing.press_release.structure.utils import (
    clean_in_line_break,
    do_strip,
    clean_very_short_lines,
)


def split_intro_article_1(txt: str, n=30) -> str:
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


def extract_id_1(intro: str) -> tuple:
    """ """

    # slplit
    intro_lines = intro.splitlines()
    logger.info(intro_lines)
    intro_cleaned_lines = [i for i in intro_lines if i.strip()]
    logger.info(intro_cleaned_lines)

    # find idx and _id
    cond_ok = lambda i: (
        ("198" in i) + ("199" in i) + ("200" in i) + ("201" in i) + ("202" in i)
    ) * ("-" in i)

    idx_cands = [i for i, j in enumerate(intro_cleaned_lines) if cond_ok(j)]
    logger.info(idx_cands)

    idx = idx_cands[-1]
    _id = intro_cleaned_lines[idx]

    # clean intro
    idx_cands = [i for i, j in enumerate(intro_lines) if _id in j]
    idx = idx_cands[0]
    intro_lines[idx] = ""
    intro_ok = "\n".join(intro_lines)

    return _id, intro_ok


def extract_h1_1(intro: str) -> tuple:
    """ """

    light_intro = clean_very_short_lines(intro)
    light_intro.replace("\n\n", "\n").replace("\n\n", "\n")
    intro_lines = light_intro.splitlines()

    # clean
    del_list = ["Press Release", "immediate Release", "Home"]
    for item in del_list:
        intro_lines = [i for i in intro_lines if item.lower() not in i.lower()]

    h1 = " ".join(intro_lines).strip()
    h1 = h1 if h1[-1] == "." else h1 + "."

    if h1.startswith("r "):
        h1 = h1[2:]

    return h1, "-1"
