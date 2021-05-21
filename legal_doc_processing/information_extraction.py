import re

import spacy
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer


def get_case(first_page):
    for line in first_page:
        if len(line) < 40:
            p = re.compile("NO[\.:]\s*.+")
            result = p.search(line.upper())
            if result:
                return result.group(0).strip()

    for line in first_page:
        if len(line) < 40:
            p = re.compile("\d*-?CV-\d+.*")
            result = p.search(line.upper())
            if result:
                return result.group(0).strip()

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
