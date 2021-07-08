import os
from pprint import pformat, pprint
import random

from legal_doc_processing import logger

from legal_doc_processing.utils import get_spacy, get_pipeline, get_label_

from legal_doc_processing.press_release.utils import press_release_X_y

from legal_doc_processing.press_release.structure.utils import (
    clean_in_line_break,
    do_strip,
    clean_very_short_lines,
)

from legal_doc_processing.press_release.structure.sec_model_1 import (
    split_intro_article_1,
    extract_id_1,
    extract_h1_1,
    extract_date_1,
)


from legal_doc_processing.press_release.structure.sec_model_2 import (
    split_intro_article_2,
    extract_id_2,
    extract_h1_2,
    extract_date_2,
)


def give_sec_press_release_df():
    """ """

    df = press_release_X_y(juridiction="sec", sample=0.9)
    cols = ["folder", "press_release_text"]

    return df.loc[:, cols]


def give_sec_press_release_file(model=1):
    """ """

    if model == 1:

        folder_list = [
            "2020-177",
            "2017-133",
            "2016-64",
            "2019-260",
            "2018-212",
            "2011-146",
            "2015-170",
            "2019-102",
            "2016-224",
            "2017-18",
            "2015-165",
            "2019-260",
            "2019-260",
            "2020-254",
            "2019-12",
            "2011-87",
            "2012-266",
            "2011-87",
            "2017-18",
            "2015-170",
        ]

    else:
        folder_list = [
            "lr17887",
            "lr21920",
            "lr20029",
            "lr21156",
            "lr20319",
            "lr21920",
            "lr21617",
            "lr18081",
            "lr20029",
            "lr21617",
            "lr21920",
            "lr20835",
            "lr17887",
            "lr20319",
            "lr21229",
        ]

    folder = random.choice(folder_list)
    fn = f"./data/files/sec/{folder}/press-release.txt"

    with open(fn, "r") as f:
        txt = f.read()

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


def define_sec_press_release_model(txt):
    """ """

    if "FOR IMMEDIATE RELEASE".lower() in txt[:1000].lower():
        return 1
    else:
        return 2


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

    sec_model = define_sec_press_release_model(txt)

    if sec_model == 2:
        try:

            # clean
            cleaned_txt = first_clean(txt)

            # intro article
            intro, article = split_intro_article_2(cleaned_txt)

            # date
            dd["date"], intro_1 = extract_date_2(intro, nlspa)

            # h1
            dd["h1"], _ = extract_h1_2(intro_1)

            # clean article
            cleaned_article = clean_in_line_break(article)
            # dd["error"] = "last line ok 117 "

            # article
            dd["article"] = cleaned_article
            # dd["error"] = "last line ok 121 "

            dd["error"] = "0"

        except Exception as e:
            logger.error(e)
            dd["error"] += str(e)

    if sec_model == 1:
        try:
            # clean
            cleaned_txt = first_clean(txt)
            # dd["error"] = "last line ok 96 "

            # intro article
            intro, article = split_intro_article_1(cleaned_txt)
            # dd["error"] = "last line ok 100 "

            # id
            dd["folder"], intro_2 = extract_id_1(intro)
            # dd["error"] = "last line ok 104 "

            # h1
            dd["h1"], _ = extract_h1_1(intro_2)
            # dd["error"] = "last line ok 108 "

            # h1
            dd["date"], _ = extract_date_1(article, nlspa)
            # dd["error"] = "last line ok 113 "

            # clean article
            cleaned_article = clean_in_line_break(article)
            # dd["error"] = "last line ok 117 "

            # article
            dd["article"] = cleaned_article
            # dd["error"] = "last line ok 121 "

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
    txt = give_sec_press_release_file(2)
    df = give_sec_press_release_df()
    # df = df.iloc[:100, :]

    # structure
    struct_ = lambda i: structure_press_release(i, nlspa=nlspa)
    df["dd"] = df.press_release_text.apply(struct_)

    # extrcat cols
    col_list = list(df.dd.iloc[0].keys())
    for col in col_list:
        df["dd_" + col] = df.dd.apply(lambda i: i.get(col, -42))
    df.drop("dd", inplace=True, axis=1)

    # save
    df.to_csv("./tmp/_WIP_structure_press_release_sec.csv", index=False)
