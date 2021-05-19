import re

import spacy


nlp = spacy.load("en_core_web_sm")


def get_case(text):
    for line in text:
        if len(line) < 40:
            p = re.compile("NO[\.:]\s*.+")
            result = p.search(line.upper())
            if result:
                return result.group(0).strip()

    for line in text:
        if len(line) < 40:
            p = re.compile("\d*-?CV-\d+.*")
            result = p.search(line.upper())
            if result:
                return result.group(0).strip()
