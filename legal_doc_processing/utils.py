import os
import pdb
from subprocess import call

import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

import spacy
from transformers import pipeline


from legal_doc_processing import logger


def dummy_accuracy(y, pred) -> int:
    """ """

    try:
        y, pred = int(y), int(pred)
        val = int(y == pred)
        logger.info(f"val {val} ")
        return val

    except Exception as e:
        logger.info(f"e {e} ")
        return -1

    return -2


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
    """ """

    df = pd.read_csv(path)
    return df


def uniquize(iterable: list) -> list:
    """ """

    try:
        return list(set(iterable))
    except Exception as e:
        return []


def strize(item_list, sep="\n", force_list=False):
    """ """

    # if score -1
    non_null = [(i, j) for i, j in item_list if j > -1]
    if not non_null:
        return ""

    # clean and unique
    clean_l = [str(i).replace("\n", "").strip() for i, j in non_null]
    str_cand = uniquize(clean_l)
    if not str_cand:
        return ""

    # return
    if len(str_cand) == 1:
        return str_cand[0]
    return sep.join(str_cand)


def get_spacy():
    """ """

    try:
        nlspa = spacy.load("en_core_web_sm")

    except Exception as e:
        call(["python", "-m", "spacy", "download", "en_core_web_sm"])

        nlspa = spacy.load("en_core_web_sm")
    try:
        nlspa.add_pipe("sentencizer")
        return nlspa
    except Exception as e:
        return nlspa


def _if_not_spacy(nlspa):
    """ if  not nlpipeline instance and return it else return pipeline already exists"""

    return nlspa if nlspa else get_spacy()


def get_label_(txt: str, label: str, nlspa=None) -> list:
    """check if a label in a text"""

    # print(label)
    nlspa = _if_not_spacy(nlspa)

    label = label.upper().strip()
    assert label in ["PERSON", "ORG", "MONEY", "DATE", "GPE"]

    ans = [i for i in nlspa(txt).ents if i.label_ == label]
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


def ask_all(txt, quest_pairs, sent_id=None, sent=None, nlpipe=None) -> list:
    """asl all questions and return a list of dict """

    # txt
    if not txt:
        raise AttributeError(f"Attribute error txt ; txt is {txt}, format {type(txt)}")

    # pipe
    nlpipe = _if_not_pipe(nlpipe)

    # ans
    ans = []

    # loop
    # logger.info(f"quest_pairs : {quest_pairs} , len {quest_pairs} ")
    # pdb.set_trace()

    for quest, label in quest_pairs:

        # logger.info(f"quest_pairs : {quest_pairs} ")
        ds = _ask(txt=txt, quest=quest, nlpipe=nlpipe)
        _ = [d.update({"question": quest, "quest_label": label}) for d in ds]
        if sent_id:
            _ = [d.update({"sent_id": sent_id}) for d in ds]
        if sent:
            _ = [d.update({"sent": sent}) for d in ds]

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


def main_X_y(
    path: str = "./data/csv/", y: str = "random_y", text: str = "random_text"
) -> pd.DataFrame:
    """ """

    cands = os.listdir(path)
    text_file = [i for i in cands if text in i][0]
    y_file = [i for i in cands if y in i][0]

    text_df = pd.read_csv(path + text_file)
    y_df = pd.read_csv(path + y_file)

    drop_cols = [i for i in y_df.columns if "link" in i]
    y_df.drop(drop_cols, axis=1, inplace=True)
    y_df.drop("juridiction", axis=1, inplace=True)

    new_df = text_df.merge(y_df, on="folder", how="inner", copy=True)

    return new_df


class Utils:
    """ """

    # df
    main_X_y = main_X_y

    # predict
    ask = _ask
    ask_all = ask_all
    merge_ans = merge_ans

    # pipeline
    if_not_pipe = _if_not_pipe
    get_pipeline = get_pipeline

    # spacy
    if_not_spacy = _if_not_spacy
    get_spacy = get_spacy

    # label
    get_label = get_label_

    # version
    version = "2.2.4"
