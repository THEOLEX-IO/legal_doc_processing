# import re
# from itertools import product

# import requests
# import asyncio

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# import heapq
# import nltk
# from cleantext import clean
import spacy
from transformers import pipeline

# AutoModelForTokenClassification, AutoTokenizer


def sub_cosine_similarity(list_corpus: list) -> object:
    """ """

    vect = TfidfVectorizer(min_df=1, stop_words="english")

    tfidf = vect.fit_transform(list_corpus)
    pairwise_similarity = tfidf * tfidf.T

    return pairwise_similarity


def cosine_similarity(y: str, pred: str) -> float:
    """eval accuracy based on cosine similarity of 2 list of answers """

    # check if args are OK

    # separer y et pred (string avec virgugles) en liste de string
    y_list = [i.strip().lower() for i in y.split(",")]
    pred_list = [i.strip().lower() for i in pred.split(",")]

    # add artificialy pred at begin of y_list
    y_pred_list = [[i] + y_list for i in pred_list]

    # poiur chaque candidat pred -> evaluer la cosine similarity
    cos_y_pred_arrays = [sub_cosine_similarity(i).toarray() for i in y_pred_list]

    # prendre pour chaque pred le 1er ligne et oublier le 1er chiffre (cf matrice identité probkem)
    cos_y_pred_list = np.array([i[0][1:] for i in cos_y_pred_arrays])

    # prendre le max de chaque lignes
    max_cos_y_pred = np.array([max(i) for i in cos_y_pred_list])

    # soit retour de la liste restante
    # soit mean de cette list

    return max_cos_y_pred.mean()


def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)  # only difference # correct solution:


def load_data(file_path: str) -> str:
    """from file_path open read and return text; return text """

    if ".pdf" in file_path:
        raise AttributeError("Error : file recieved is a pdf, only txt supported")

    with open(file_path, "r") as f:
        txt = f.read()

    return txt


def make_dataframe(path: str = "./data/csv/files.csv"):

    # read df
    df = pd.read_csv(path)
    return df


def uniquize(iterable: list) -> list:
    """ """

    try:
        return list(set(iterable))
    except Exception as e:
        return []


def strize(item_list):
    """ """

    non_null = [(i, j) for i, j in item_list if j > 0]
    if not non_null:
        return ""

    clean_l = lambda item_list: [str(i).strip() for i, j in non_null]

    unique_l = uniquize(clean_l)

    return ",".join(clean_l(unique_l))


def get_spacy():
    return spacy.load("en_core_web_sm")


def _if_not_spacy(nlpspa):
    """ if  not nlpipeline instance and return it else return pipeline already exists"""

    return nlpspa if nlpspa else get_spacy()


def get_label_(txt: str, label: str, nlpspa=None) -> list:
    """check if a label in a text"""

    # print(label)
    nlpspa = _if_not_spacy(nlpspa)

    label = label.upper().strip()
    assert label in ["PERSON", "ORG", "MONEY", "DATE"]

    ans = [i for i in nlpspa(txt).ents if i.label_ == label]
    ans = [str(p) for p in ans]

    return ans


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


def ask_all(txt, quest_pairs, nlpipe) -> list:
    """asl all questions and return a list of dict """

    # txt
    if not txt:
        raise AttributeError(f"Attribute error txt ; txt is {txt}, format {type(txt)}")

    # pipe
    nlpipe = _if_not_pipe(nlpipe)

    # ans
    ans = []

    # loop
    for quest, label in quest_pairs:
        ds = _ask(txt=txt, quest=quest, nlpipe=nlpipe)
        _ = [d.update({"question": label}) for d in ds]
        ans.extend(ds)

    # sort
    ans = sorted(ans, key=lambda i: i["score"], reverse=True)

    return ans


def merge_ans(ans, label="new_answer", threshold=0.1):
    """based on new_answer we will make a groupby adding the scores for each new ans in a cumulative score
    example [{new_ans : hello, score:0.3},{new_ans : hello, score:0.3}, ]
    will become  [{new_ans : hello, score:0.6},]"""

    # build dataframe
    df = pd.DataFrame(ans)

    # check
    if not label in df.columns:
        raise AttributeError(
            f"pb  label in df.columns --> label is {label } cols are {df.columns}"
        )

    # select
    droped = [i for i in df.columns if i not in ["score", label]]
    df = df.drop(droped, axis=1, inplace=False)

    # group by ans and make cumutavie score of accuracy
    ll = [
        {label: k, "cum_score": round(v.score.sum(), 2)}
        for k, v in df.groupby(label)
        if v.score.sum() > threshold
    ]
    ll = sorted(ll, key=lambda i: i["cum_score"], reverse=True)

    return ll


# def get_pers(txt: str, nlpspa=None) -> list:
#     """ with spacy get entities PERSON"""

#     return get_label_(txt, "PERSON", nlpspa)


# def get_orgs(txt: str, nlpspa=None) -> list:
#     """ with spacy get entities ORG"""

#     return get_label_(txt, "ORG", nlpspa)


# def clean_spec_chars(text: str) -> tuple:
#     """first text cleaning based on regex, just keep text not spec chars
#     return tupple of text"""

#     # article text
#     article_text = re.sub(r"\[[0-9]*\]", " ", text)
#     article_text = re.sub(r"\s+", " ", article_text)

#     # formated text
#     formatted_article_text = re.sub("[^a-zA-Z]", " ", article_text)
#     formatted_article_text = re.sub(r"\s+", " ", formatted_article_text)

#     return article_text, formatted_article_text


# def handle_encoding(text: str) -> str:
#     """handle encoding problems and force ascii conversion ; return clean text """
#     text_encode = text.encode(encoding="ascii", errors="ignore")

#     # cleaning the text to remove extra whitespace
#     clean_text = " ".join([word for word in text_decode.split()])

#     return clean_text


# def _boot_press_release():
#     """test init press release """

#     # from legal_doc_processing.press_release import (
#     #     PressRelease,
#     #     read_PressRelease,
#     #     load_press_release_text_list,
#     # )

#     # num = "7100-15"
#     # url = f"https://storage.googleapis.com/theolex_documents_processing/cftc/text/7100-15/order-allied-markets-llc-et-al.txt"
#     # nlpipe = get_pipeline()
#     # pr = PressRelease("Hello World", nlpipe=nlpipe)
#     # # pr.predict("all")

#     pass


# def _boot_legal_doc():
#     """ try to build and predict a LegalDoc and an PressRelease"""

#     from legal_doc_processing.legal_doc import (
#         LegalDoc,
#         read_LegalDoc,
#         load_legal_doc_text_list,
#     )

#     url = ""
#     nlpipe = get_pipeline()
#     ld = LegalDoc("Hello World", nlpipe=nlpipe)
#     # ld.predict("all")


# def boot():
#     """ """

#     _boot_press_release()
#     _boot_legal_doc()


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
