import re

import requests
import asyncio

import pandas as pd
import numpy as np

import heapq
import nltk
from cleantext import clean
import spacy
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer


def get_spacy():
    return spacy.load("en_core_web_sm")


def _if_not_spacy(nlpspa):
    """ if  not nlpipeline instance and return it else return pipeline already exists"""

    return nlpspa if nlpspa else get_spacy()


def get_label_(txt: str, label: str, nlpspa=None) -> list:
    """check if a label in a text"""

    nlpspa = _if_not_spacy(nlpspa)

    label = label.upper().strip()
    assert label in ["PERSON", "ORG", "MONEY"]

    pers = [i for i in nlpspa(txt).ents if i.label_ == label]
    pers = [str(p) for p in pers]

    return pers


def get_pers(txt: str, nlpspa=None) -> list:
    """ with spacy get entities PERSON"""

    return get_label_(txt, "PERSON", nlpspa)


def get_orgs(txt: str, nlpspa=None) -> list:
    """ with spacy get entities ORG"""

    return get_label_(txt, "ORG", nlpspa)


def get_pipeline():
    """ build and return a piplein"""

    return pipeline(
        "question-answering",
        model="distilbert-base-cased-distilled-squad",
        tokenizer="distilbert-base-cased",
    )


def _if_not_pipe(nlpipe):
    """ if  not nlpipeline instance and return it else return pipeline already exists"""

    return nlpipe if nlpipe else get_pipeline()


def _ask(txt: str, quest: str, nlpipe, topk: int = 3) -> list:
    """MAKE A QUESTION """

    # txt
    if not txt:
        raise AttributeError(f"Attribute error txt ; txt is {txt}, format {type(txt)}")

    # quest
    if not quest:
        raise AttributeError(
            f"Attribute error quest ; quest is {quest}, format {type(quest)}"
        )

    nlpipe = _if_not_pipe(nlpipe)

    return nlpipe(question=quest, context=txt, topk=topk)


def load_data(file_path: str) -> str:
    """from file_path open read and return text; return text """

    if ".pdf" in file_path:
        raise AttributeError("Error : file recieved is a pdf, only txt supported")

    with open(file_path, "r") as f:
        txt = f.read()

    return txt


def clean_spec_chars(text: str) -> tuple:
    """first text cleaning based on regex, just keep text not spec chars
    return tupple of text"""

    # article text
    article_text = re.sub(r"\[[0-9]*\]", " ", text)
    article_text = re.sub(r"\s+", " ", article_text)

    # formated text
    formatted_article_text = re.sub("[^a-zA-Z]", " ", article_text)
    formatted_article_text = re.sub(r"\s+", " ", formatted_article_text)

    return article_text, formatted_article_text


# def handle_encoding(text: str) -> str:
#     """handle encoding problems and force ascii conversion ; return clean text """
#     text_encode = text.encode(encoding="ascii", errors="ignore")

#     # cleaning the text to remove extra whitespace
#     clean_text = " ".join([word for word in text_decode.split()])

#     return clean_text


def _boot_press_release():
    """test init press release """

    from legal_doc_processing.press_release import (
        PressRelease,
        read_PressRelease,
        load_press_release_text_list,
    )

    # num = "7100-15"
    # url = f"https://storage.googleapis.com/theolex_documents_processing/cftc/text/7100-15/order-allied-markets-llc-et-al.txt"
    # nlpipe = get_pipeline()
    # pr = PressRelease("Hello World", nlpipe=nlpipe)
    # # pr.predict("all")


def _boot_legal_doc():
    """ try to build and predict a LegalDoc and an PressRelease"""

    from legal_doc_processing.legal_doc import (
        LegalDoc,
        read_LegalDoc,
        load_legal_doc_text_list,
    )

    url = ""
    nlpipe = get_pipeline()
    ld = LegalDoc("Hello World", nlpipe=nlpipe)
    # ld.predict("all")


def boot():
    """ """

    _boot_press_release()
    _boot_legal_doc()


def make_dataframe(
    path: str = "./data/csv/files.csv",
):

    # read df
    df = pd.read_csv(path)
    return df


# DEPRECATED
# def make_dataframe(path: str = "./data/csv/original_dataset.csv", n: int = 10):
#     """
#     :param path  = the path to read original dataset
#     :param n     = the n-st line to scrap, other will be droped
#     """

#     # read df
#     df = pd.read_csv(path)

#     # keep cols
#     keep_cols = [
#         "id",
#         "name",
#         "status",
#         "reference",
#         "document_link",
#         "press_release_link",
#         "monetary_sanction",
#         "currency",
#         "type",
#         "justice_type",
#         "defendant",
#         "decision_date",
#         "extracted_violations",
#     ]

#     drop_cols = [i for i in df.columns if i not in keep_cols]
#     df = df.drop(drop_cols, axis=1)

#     # fill rate
#     fill_rate = lambda col: (len(df) - sum(df[col].isna())) / len(df)
#     df_rate_fill = [(col, round(fill_rate(col), 2)) for col in df.columns]

#     # press_release and document_link
#     for col, ext in [("press_release", ".html"), ("document", ".txt")]:
#         funct = (
#             lambda i: np.nan if ("storage.google" not in i) else i.replace(".pdf", ext)
#         )
#         df[col + "_URL"] = df[col + "_link"].apply(lambda i: funct(str(i).strip()))

#     # clean lines without press or document
#     df = df.loc[~df.document_URL.isna(), :]
#     df = df.loc[~df.press_release_URL.isna(), :]
#     df.index = range(len(df))

#     def scrap(url: str):
#         """ """

#         try:
#             # print(url)
#             res = requests.get(url)

#             if res.status_code < 300:
#                 return res.text
#             else:
#                 return res.status_code

#         except Exception as e:
#             return str(e)

#     # test on 10
#     df = df.iloc[:n, :]

#     # sync version
#     for col in ["press_release", "document"]:
#         df[col + "_TEXT"] = df[col + "_URL"].apply(lambda i: scrap(str(i).strip()))

#     df.to_csv("./data/csv/dataset.csv", index=False)

#     return df
