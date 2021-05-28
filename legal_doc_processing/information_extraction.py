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


def ask_who_is(txt: str, who: str, nlpipe=None) -> list:
    """ init a nlpipe if needed and ask who is the who """

    # init pipleine if needed
    if not nlpipe:
        nlpipe = pipeline(
            "question-answering",
            model="distilbert-base-cased-distilled-squad",
            tokenizer="distilbert-base-cased",
        )

    # pipe and return
    return nlpipe(question=f"Who is the {who}?", context=".".join(txt), topk=3)


def get_defendant(first_page: list, nlpipe=None) -> str:
    """from a list of text lines, create a pipelie if needed and asqk question """

    # first_page_100 = [text for text in first_page if len(text) > 100]
    joined_first_page = "\n".join(first_page)

    # ask
    ans = ask_who_is(joined_first_page, "defendant", nlpipe)

    return ans[0]["answer"]


def get_violeted(first_page: list, nlpipe=None) -> str:
    """from a list of text lines, create a pipelie if needed and asqk question """

    # first_page_100 = [text for text in first_page if len(text) > 100]
    joined_first_page = "\n".join(first_page)

    # ask
    ans = ask_who_is(joined_first_page, "violated", nlpipe)

    return ans[0]["answer"]
