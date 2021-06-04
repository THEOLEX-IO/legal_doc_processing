import re
import pickle

import spacy
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer


def get_pipeline():
    """ build and return a piplein"""

    return pipeline(
        "question-answering",
        model="distilbert-base-cased-distilled-squad",
        tokenizer="distilbert-base-cased",
    )


def save_pipeline():
    """init a pipeline and save in a pk """

    with open("./utils/pipe.pk", "wb") as f:
        nlpipe = get_pipeline()
        obj = pickle.dumps(nlpipe)
        f.write(obj)


def load_pipeline():
    """load apickled object """

    with open("./utils/pipe.pk", "rb") as f:
        cand = f.read()
    nlpipe = pickle.loads(cand)

    return nlpipe


def get_case(first_page, length_treshold=50):
    """parse the first page line by line, matching a
    regex pattern refering to case feature
    example 'NO.: 14-CV-81216'
    return the result"""

    # dump small char lines
    first_page = [i for i in first_page if len(i) < length_treshold]

    # format result
    format_result = (
        lambda i: i.group(0)
        .upper()
        .replace("NO.", "")
        .replace("NO", "")
        .replace(":", "")
        .strip()
    )

    # first search smthg with - 99-CV-99999 -
    p = re.compile("\d*-?CV-\d+.*")
    for line in first_page:
        result = p.search(line.upper())
        if result:
            return format_result(result)

    # first search smthg with - No.: -
    p = re.compile("NO[\.:]\s*.+")
    for line in first_page:
        result = p.search(line.upper())
        if result:
            return format_result(result)

    return "-- error : case not founded --"
