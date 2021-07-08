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


def give_cfbp_press_release_df():
    """ """

    df = press_release_X_y(juridiction="cfbp", sample=0.9)
    cols = ["folder", "press_release_text"]

    return df.loc[:, cols]


def give_cfbp_press_release_file():
    """ """

    fn = "./data/files/cfbp/phloans/press-release.txt"

    with open(fn, "r") as f:
        txt = f.read()

    # btxt = txt.encode("latin-1")
    # txt_decoded = btxt.decode("utf8")

    return txt


def first_clean(txt: str) -> str:
    """ """

    btxt = txt.encode("latin-1")
    txt_decoded = btxt.decode("utf8")

    # # clean double breaks and fake lines
    # new_txt_1 = clean_in_line_break(txt)

    # strip
    new_txt_2 = do_strip(txt_decoded)

    return new_txt_2


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


def extract_date(intro: str, nlspa) -> tuple:
    """ """

    date_list = get_label_(intro, label="DATE", nlspa=nlspa)

    # if date_list
    if len(date_list) > 0:
        date = date_list[0]
    else:
        date = "-1"

    # if not return dummy
    if date == "-1":
        return date, intro

    # find date_line
    intro_lines = intro.splitlines()
    idx_list = [i for i, j in enumerate(intro_lines) if date.lower() in j.lower()]
    idx = idx_list[0]
    date = intro_lines[idx]

    # clean intro
    intro_lines[idx] = ""
    intro_ok = "\n".join(intro_lines)

    return date, intro_ok


def extract_h1(intro: str) -> tuple:
    """ """

    intro_lines = intro.splitlines()
    intro = "\n".join(intro_lines[2:])

    light_intro = clean_very_short_lines(intro)
    light_intro.replace("\n\n", "\n").replace("\n\n", "\n")
    intro_lines = light_intro.splitlines()

    h1 = " ".join(intro_lines).strip()
    h1 = h1 if h1[-1] == "." else h1 + "."

    # if h1.startswith("r "):
    #     h1 = h1[2:]

    return h1, "-1"


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
        "folder": "--ERROR--",
        "date": "--ERROR--",
        "h1": "--ERROR--",
        "article": "--ERROR--",
        "end": "--ERROR--",
        "error": "0",
    }

    try:
        # clean
        cleaned_txt = first_clean(txt)
        # dd["error"] = "last line ok 96 "

        # intro article
        intro, article = split_intro_article_1(cleaned_txt)
        # dd["error"] = "last line ok 100 "

        # date
        dd["date"], intro_1 = extract_date(intro, nlspa)

        # h1
        dd["h1"], _ = extract_h1(intro_1)

        # clean article
        cleaned_article = clean_in_line_break(article)

        # article
        dd["article"] = cleaned_article

        dd["error"] = "0"

    except Exception as e:
        logger.error(e)
        dd["error"] += str(e)

    return dd


if __name__ == "__main__":

    # spac
    nlspa = get_spacy()
    nlspa.add_pipe("sentencizer")

    # load data
    txt = give_cfbp_press_release_file()
    df = give_cfbp_press_release_df()
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
    df.to_csv("./data/csv/structure_press_release_cfbp.csv", index=False)