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


def get_pipeline():
    """ build and return a piplein"""

    return pipeline(
        "question-answering",
        model="distilbert-base-cased-distilled-squad",
        tokenizer="distilbert-base-cased",
    )


# nltk.download("stopwords")
stopwords = nltk.corpus.stopwords.words("english")


def boot():

    from legal_doc_processing.legal_doc import LegalDoc
    from legal_doc_processing.press_release import PressRelease

    hello = LegalDoc("Hello World")
    hello = PressRelease("Hello World")


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

#     # encoding the text to ASCII format
#     text_encode = text.encode(encoding="ascii", errors="ignore")

#     # decoding the text
#     text_decode = text_encode.decode()

#     # cleaning the text to remove extra whitespace
#     clean_text = " ".join([word for word in text_decode.split()])

#     return clean_text


def make_dataframe(
    path: str = "./data/csv/original_dataset.csv", n: int = 10
) -> pd.DataFrame:
    """on basis of csv dataframe with all features, data clean, scrap googleapi and insert text in the dataframe
    :param path  = the path to read original dataset
    :param n     = the n-st line to scrap, other will be droped
    :return      = a dataframe with original data cleaned + text of main doc and press release
    """

    # read df
    df = pd.read_csv(path)

    # keep cols
    keep_cols = [
        "id",
        "name",
        "status",
        "reference",
        "document_link",
        "press_release_link",
        "monetary_sanction",
        "currency",
        "type",
        "justice_type",
        "defendant",
        "decision_date",
        "extracted_violations",
    ]

    drop_cols = [i for i in df.columns if i not in keep_cols]
    df = df.drop(drop_cols, axis=1)

    # fill rate
    fill_rate = lambda col: (len(df) - sum(df[col].isna())) / len(df)
    df_rate_fill = [(col, round(fill_rate(col), 2)) for col in df.columns]

    # press_release and document_link
    for col, ext in [("press_release", ".html"), ("document", ".txt")]:
        funct = (
            lambda i: np.nan if ("storage.google" not in i) else i.replace(".pdf", ext)
        )
        df[col + "_URL"] = df[col + "_link"].apply(lambda i: funct(str(i).strip()))

    # clean lines without press or document
    df = df.loc[~df.document_URL.isna(), :]
    df = df.loc[~df.press_release_URL.isna(), :]
    df.index = range(len(df))

    def scrap(url: str):
        """ """

        try:
            print(url)
            res = requests.get(url)

            if res.status_code < 300:
                return res.text
            else:
                return res.status_code

        except Exception as e:
            return str(e)

    # test on 10
    df = df.iloc[:n, :]

    # sync version
    for col in ["press_release", "document"]:
        df[col + "_TEXT"] = df[col + "_URL"].apply(lambda i: scrap(str(i).strip()))

    df.to_csv("./data/csv/dataset.csv", index=False)

    return df
