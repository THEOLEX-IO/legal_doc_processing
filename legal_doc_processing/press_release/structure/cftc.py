import os
from pprint import pformat, pprint

from legal_doc_processing import logger

from legal_doc_processing.utils import get_spacy, get_pipeline, get_label_

from legal_doc_processing.press_release.structure.utils import (
    clean_in_line_break,
    do_strip,
    find_id_line_in_intro,
    find_date_line_in_intro,
    clean_very_short_lines,
)


# def give_cftc_press_release():
#     """ """

#     fn = "./data/files/cftc/7117-15/press-release.txt"

#     with open(fn, "r") as f:
#         txt = f.read()

#     return txt


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

    if len(date_list) > 0:
        date = date_list[0]
    else:
        date = -1

    return date, intro


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

        # # id
        # dd["id"], intro_1 =  extract_id(intro, nlspa)

        # # date
        # dd["date"], intro_2 =  extract_date(intro_1, nlspa)

        # # h1
        # dd["h1"], intro_3 = extract_h1(intro_2, nlspa)

        # idx id and date
        idx_id_line = find_id_line_in_intro(intro)
        idx_date_line = find_date_line_in_intro(intro)

        # split extract
        intro_lines = intro.splitlines()
        if idx_id_line != -1:
            dd["id"] = intro_lines[idx_id_line]

        if idx_date_line != -1:
            dd["date"] = intro_lines[idx_date_line]

        # h1
        intro_lines[idx_id_line] = ""
        intro_lines[idx_date_line] = ""

        intro_intermediate = "\n".join(intro_lines)
        dd["h1"] = clean_very_short_lines(intro_intermediate)

        # end
        dd["end"], article_ok = extract_end(article)

        # article
        dd["article"] = article_ok

    except Exception as e:
        logger.error(e)
        dd["error"] = e

    return dd