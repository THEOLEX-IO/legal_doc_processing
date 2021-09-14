import os
from pprint import pformat, pprint

from legal_doc_processing import logger

from legal_doc_processing.utils import get_label_

from legal_doc_processing.press_release.structure.utils import (
    clean_in_line_break,
    do_strip,
    clean_very_short_lines,
)


def _detect_true_text_id(txt_lines: str, line_length_txt=50, n_lines=4) -> int:
    """ """

    # find a first candidate for a REAL senetence
    # i, len char the line, the line itself
    cands_1st = [(i, len(j), j) for i, j in enumerate(txt_lines)]

    # then we want the len of this line, the len of the n+1 line, idem n+2, n+3
    cands_2nd = [
        (
            i,
            [cands_1st[i + k][1] for k in range(n_lines)],
            k,
        )
        for i, j, k in cands_1st[: -(n_lines + 1)]
    ]

    # we want to know if the 3 next lines will be len() > threshold
    cands_3rd = [(i, sum([kk > line_length_txt for kk in j]), k) for i, j, k in cands_2nd]

    # if not all then True
    cands_5th = [(i, j, k) for i, j, k in cands_3rd if j >= n_lines]

    if not cands_5th:
        return -1
    else:
        return cands_5th[0][0]


def split_intro_article_2(txt: str, n=30) -> str:
    """ """

    txt_other = txt.splitlines()[n:]
    txt_lines_30 = txt.splitlines()[:n]

    # find v.
    cand_list = ["SEC v.", "Commission v."]
    cond_ok = lambda i: any([cand.lower() in i.lower() for cand in cand_list])
    idx_v_cands = [i for i, j in enumerate(txt_lines_30) if cond_ok(j)]
    # logger.info(idx_v_cands)

    # cut v.
    idx_v_plus_1 = idx_v_cands[0] + 1
    pre_txt_lines = txt_lines_30[:idx_v_plus_1]
    post_txt_lines = txt_lines_30[idx_v_plus_1:]

    # true text begins at
    idx_true_txt = _detect_true_text_id(post_txt_lines)

    A_post_txt_lines = post_txt_lines[:idx_true_txt]
    B_post_txt_lines = post_txt_lines[idx_true_txt:]

    intro = "\n".join(pre_txt_lines + A_post_txt_lines)
    article = "\n".join(B_post_txt_lines + txt_other)

    return intro, article


def extract_id_2(intro: str) -> tuple:
    """ """

    # slplit
    # intro_lines = intro.splitlines()
    # logger.info(intro_lines)
    # intro_cleaned_lines = [i for i in intro_lines if i.strip()]
    # logger.info(intro_cleaned_lines)

    # # find v.
    # cand_list = ["SEC v.", "Commission v."]
    # cond_ok = lambda i: any([cand.lower() in i.lower() for cand in cand_list])
    # idx_v_cands = [i for i, j in enumerate(intro_lines) if cond_ok(j)]
    # logger.info(idx_v_cands)

    # idx_v = idx_v_cands[0] + 1
    # _id = intro_cleaned_lines[idx]

    # # clean intro
    # idx_cands = [i for i, j in enumerate(intro_lines) if _id in j]
    # idx = idx_cands[0]
    # intro_lines[idx] = ""
    # intro_ok = "\n".join(intro_lines)

    # return _id, intro_ok

    pass


def extract_date_2(intro: str, nlspa) -> tuple:
    """ """

    date_list = get_label_(intro, label="DATE", nlspa=nlspa)

    # if date_list
    if len(date_list) > 0:
        date = date_list[0]
    else:
        return "-1", intro

    # find date_line
    intro_lines = intro.splitlines()
    idx_list = [i for i, j in enumerate(intro_lines) if date.lower() in j.lower()]
    idx = idx_list[0]

    # clean intro
    intro_lines[idx] = ""
    intro_ok = "\n".join(intro_lines)

    return date, intro_ok


def extract_h1_2(intro: str) -> tuple:
    """ """

    intro_lines = intro.splitlines()

    # find v.
    cand_list = ["SEC v.", "Commission v."]
    cond_ok = lambda i: any([cand.lower() in i.lower() for cand in cand_list])
    idx_v_cands = [i for i, j in enumerate(intro_lines) if cond_ok(j)]
    # logger.info(idx_v_cands)

    # cut v.
    idx_v_plus_1 = idx_v_cands[0] + 1
    post_txt_lines = intro_lines[idx_v_plus_1:]

    # clean
    clean_list = [
        "CV-",
        "Case No.",
        "Release",
        "No.",
        "United States District",
        "(GEB)",
        "D.N.J.",
        "ET AL",
        "U.S.D.C.",
        "D.D.C.",
        "District of",
        "S.D.N.Y",
        ")",
    ]
    for clean_i in clean_list:
        post_txt_lines = [i for i in post_txt_lines if clean_i.lower() not in i.lower()]

    post_txt_lines = [i.strip() for i in post_txt_lines]

    if post_txt_lines[0] == "":
        post_txt_lines = post_txt_lines[1:]

    post_txt_lines = [(". " if i == "" else i) for i in post_txt_lines]

    h1 = "".join(post_txt_lines).strip()
    h1 = h1 if h1[-1] == "." else h1 + "."
    h1 = h1 if h1[-1] == "." else h1 + "."

    return h1, "-1"
