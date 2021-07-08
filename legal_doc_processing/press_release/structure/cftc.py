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


def give_cftc_press_release_df():
    """ """

    df = press_release_X_y(juridiction="cftc", sample=0.9)
    cols = ["folder", "press_release_text"]

    return df.loc[:, cols]


def give_cftc_press_release_file():
    """ """

    fn = "./data/files/cftc/7117-15/press-release.txt"

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
        dd["h1"], _ = extract_h1(intro_2)

        # clean article
        cleaned_article = clean_in_line_break(article)

        # end
        dd["end"], article_ok = extract_end(cleaned_article)

        # article
        dd["article"] = article_ok

    except Exception as e:
        logger.error(e)
        dd["error"] = e

    return dd


if __name__ == "__main__":

    # spac
    nlspa = get_spacy()
    nlspa.add_pipe("sentencizer")

    # load data
    txt = give_cftc_press_release_file()
    df = give_cftc_press_release_df()
    # df = df.iloc[:30, :]

    # structure
    struct_ = lambda i: structure_press_release(i, nlspa=nlspa)
    df["dd"] = df.press_release_text.apply(struct_)

    # extrcat cols
    col_list = list(df.dd.iloc[0].keys())
    for col in col_list:
        df["dd_" + col] = df.dd.apply(lambda i: i.get(col, -42))
    df.drop("dd", inplace=True, axis=1)

    # save
    df.to_csv("./data/csv/structure_press_release_cftc.csv", index=False)