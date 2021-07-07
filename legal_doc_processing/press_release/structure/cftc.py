import os
from pprint import pformat, pprint

from legal_doc_processing import logger

from legal_doc_processing.utils import get_spacy, get_pipeline, get_label_

from legal_doc_processing.press_release.structure.utils import (
    clean_in_line_break,
    do_strip,
    clean_very_short_lines,
)


# def give_cftc_press_release():
#     """ """

#     fn = "./data/files/cftc/7117-15/press-release.txt"

#     with open(fn, "r") as f:
#         txt = f.read()

#     btxt = txt.encode("latin-1")
#     txt_decoded = btxt.decode("utf8")

#     return txt_decoded


# txt = give_cftc_press_release()


def first_clean(txt: str) -> str:
    """ """

    # clean double breaks and fake lines
    new_txt_1 = clean_in_line_break(txt)

    # strip
    new_txt_2 = do_strip(new_txt_1)

    return new_txt_2


def split_intro_article(txt: str) -> str:
    """ """

    splitter = "\nWashington DC"

    idx = txt.lower().find(splitter.lower())
    intro, article = txt[:idx], txt[idx + 1 :]

    return intro, article


def extract_date(intro: str, nlspa) -> tuple:
    """ """

    date_list = get_label_(intro, label="DATE", nlspa=nlspa)

    # if date_list
    if len(date_list) > 0:
        date = date_list[0]
    else:
        date = -1

    # if not return dummy
    if date == -1:
        return -1, intro

    # find date_line
    intro_lines = intro.splitlines()
    idx_list = [i for i, j in enumerate(intro_lines) if date.lower() in j.lower()]
    idx = idx_list[0]

    # clean intro
    intro_lines[idx] = ""
    intro_ok = "\n".join(intro_lines)

    return date, intro_ok


def extract_id(intro: str, len_max=35) -> tuple:
    """ """

    # find id list
    # intro_lines = [i for i in intro.splitlines() if len(i) < len_max]
    intro_lines = [i for i in intro.splitlines()]

    idx_list = [
        i for i, j in enumerate(intro_lines) if j.lower().startswith("Release".lower())
    ]

    # return dummy
    if len(idx_list) != 1:
        return -1, intro

    # clean intro
    idx = idx_list[0]
    _id = intro_lines[idx]
    intro_lines[idx] = ""
    intro_ok = "\n".join(intro_lines)

    return _id, intro_ok


def extract_h1(intro: str) -> tuple:
    """ """

    light_intro = clean_very_short_lines(intro)
    light_intro.replace("\n\n", "\n").replace("\n\n", "\n")
    intro_lines = light_intro.splitlines()
    h1 = ". ".join(intro_lines).strip()
    h1 = h1 if h1[-1] == "." else h1 + "."

    return h1, "-1"


def extract_end(article: str, n: int = -2) -> tuple:
    """ """

    split_article = article.split("\n\n")
    article_ok = "\n\n".join(split_article[:n])
    end = "\n\n".join(split_article[n:])

    return end, article_ok


def structure_press_release(txt, nslspa=""):
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

    try:

        # clean
        cleaned_txt = first_clean(txt)

        # intro article
        intro, article = split_intro_article(cleaned_txt)

        # date
        dd["date"], intro_1 = extract_date(intro, nlspa)

        # id
        dd["id"], intro_2 = extract_id(intro_1)

        # h1
        dd["h1"], intro_3 = extract_h1(intro_2)

        # end
        dd["end"], article_ok = extract_end(article)

        # article
        dd["article"] = article_ok

    except Exception as e:
        logger.error(e)
        dd["error"] = e

    return dd