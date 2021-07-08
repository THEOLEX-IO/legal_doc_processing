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


def give_doj_press_release_df():
    """ """

    df = press_release_X_y(juridiction="doj", sample=0.9)
    cols = ["folder", "press_release_text"]

    return df.loc[:, cols]


def give_doj_press_release_file():
    """ """

    fn = "./data/files/doj/airbus-se/press-release.txt"

    with open(fn, "r") as f:
        txt = f.read()

    # btxt = txt.encode("latin-1")
    # txt_decoded = btxt.decode("utf8")

    return txt


def first_clean(txt: str) -> str:
    """ """

    btxt = txt.encode("latin-1")
    txt_decoded = btxt.decode("utf8")

    # clean double breaks and fake lines
    new_txt_1 = clean_in_line_break(txt_decoded)

    # strip
    new_txt_2 = do_strip(new_txt_1)

    return new_txt_2


def split_intro_article(txt: str) -> str:
    """ """

    splitter = "for IMMEDIATE RELEASE"
    lines = txt.splitlines()

    # identifie and split
    idx_lines = [i for i, j in enumerate(lines) if splitter.lower() in j.lower()]
    logger.info(idx_lines)
    assert len(idx_lines) > 0
    idx = idx_lines[0]
    intro_lines, article_lines = lines[: idx + 1], lines[idx + 1 :]

    # rejoin
    intro = "\n".join(intro_lines)
    article = "\n".join(article_lines)

    # find h1 in article
    article_lines = article.splitlines()

    first_true_sent_list = [
        i for i, j in enumerate(article_lines[:20]) if j.strip().endswith(".")
    ]
    first_true_sent_idx = first_true_sent_list[0]

    # swap h1 from article to intro
    intro_ok = intro + "\n" + "\n".join(article_lines[:first_true_sent_idx])
    article_ok = "\n".join(article_lines[first_true_sent_idx:])

    return intro_ok, article_ok


def extract_date(intro: str, nlspa) -> tuple:
    """ """

    date_list = get_label_(intro, label="DATE", nlspa=nlspa)

    if len(date_list) > 0:
        date = date_list[0]
    else:
        date = "-1"

    return date, intro


def extract_h1(intro: str, nlspa) -> tuple:
    """ """

    light_intro = clean_very_short_lines(intro)
    intro_lines = intro.splitlines()
    idx_list = [
        i for i, j in enumerate(intro_lines) if "IMMEDIATE RELEASE".lower() in j.lower()
    ]
    idx = idx_list[0]
    h1_lines = intro_lines[idx + 1 :]
    h1 = ". ".join(h1_lines).strip()
    h1 = h1 if h1[-1] == "." else h1 + "."

    return h1, intro


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

        # intro article
        intro, article = split_intro_article(cleaned_txt)

        # date
        dd["date"], intro = extract_date(intro, nlspa)

        # h1
        dd["h1"], intro = extract_h1(intro, nlspa)

        # article
        dd["article"] = article

    except Exception as e:
        logger.error(e)
        dd["error"] = str(e)

    return dd


if __name__ == "__main__":

    # spac
    nlspa = get_spacy()
    nlspa.add_pipe("sentencizer")

    # load data
    txt = give_doj_press_release_file()
    df = give_doj_press_release_df()
    # df = df.iloc[:10, :]

    # structure
    struct_ = lambda i: structure_press_release(i, nlspa=nlspa)
    df["dd"] = df.press_release_text.apply(struct_)

    # extrcat cols
    col_list = list(df.dd.iloc[0].keys())
    for col in col_list:
        df["dd_" + col] = df.dd.apply(lambda i: i.get(col, -42))
    df.drop("dd", inplace=True, axis=1)

    # save
    df.to_csv("./data/csv/structure_press_release_doj.csv", index=False)