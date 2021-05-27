import re

import spacy
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer


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


def get_defendant(first_page):

    # Process whole documents
    nlp = spacy.load("en_core_web_sm")
    joined_first_page = "\n".join(first_page)
    doc = nlp(joined_first_page)

    # Question answering pipeline, specifying the checkpoint identifier
    nlpipe = pipeline(
        "question-answering",
        model="distilbert-base-cased-distilled-squad",
        tokenizer="distilbert-base-cased",
    )

    first_page_100 = [text for text in first_page if len(text) > 100]

    defendant_ans = nlpipe(
        question="Who is the defendant?", context=".".join(first_page_100), topk=3
    )
    return defendant_ans[0]["answer"]


def get_violeted(first_page):

    # Process whole documents
    nlp = spacy.load("en_core_web_sm")
    joined_first_page = "\n".join(first_page)
    doc = nlp(joined_first_page)

    # Question answering pipeline, specifying the checkpoint identifier
    nlpipe = pipeline(
        "question-answering",
        model="distilbert-base-cased-distilled-squad",
        tokenizer="distilbert-base-cased",
    )

    first_page_100 = [text for text in first_page if len(text) > 100]

    violeted_ans = nlpipe(
        question="Who violeted?", context=".".join(first_page_100), topk=3
    )

    return violeted_ans[0]["answer"]