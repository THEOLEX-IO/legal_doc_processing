import re

import spacy
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer

from legal_doc_processing.utils import clean_doc

nlp = spacy.load("en_core_web_sm")


nlp = pipeline(
    "question-answering",
    model="distilbert-base-cased-distilled-squad",
    tokenizer="distilbert-base-cased",
)


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
