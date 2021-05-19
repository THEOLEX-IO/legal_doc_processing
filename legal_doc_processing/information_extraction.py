import re

import spacy
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer

from legal_doc_processing.utils import clean_doc

# nlp = spacy.load("en_core_web_sm")


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


def get_defendant(clean_text):

    nlp = pipeline(
        "question-answering",
        model="distilbert-base-cased-distilled-squad",
        tokenizer="distilbert-base-cased",
    )

    first_page = [text for text in clean_text[0] if len(text) > 5]

    pred = nlp(question="Who is the defendant?", context=formatted_article_text, topk=2)
    return pred[0]["answer"]