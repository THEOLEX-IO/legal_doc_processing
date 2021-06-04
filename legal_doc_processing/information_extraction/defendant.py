import re
import pickle

import spacy
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer


def ask_who_charged(first_page: list, nlpipe=None) -> str:
    """from a list of text lines, create a pipelie if needed and asqk question """

    # first_page_100 = [text for text in first_page if len(text) > 100]
    joined_first_page = "\n".join(first_page)

    # ask
    ans = nlpipe(question=f"Who is charged?", context=txt, topk=3)

    return ans


def ask_who_accused(first_page: list, nlpipe=None) -> str:
    """from a list of text lines, create a pipelie if needed and asqk question """

    # first_page_100 = [text for text in first_page if len(text) > 100]
    joined_first_page = "\n".join(first_page)

    # ask
    ans = nlpipe(question=f"Who is accused?", context=txt, topk=3)

    return ans


def ask_who_violated(first_page: list, nlpipe=None) -> str:
    """from a list of text lines, create a pipelie if needed and asqk question """

    # first_page_100 = [text for text in first_page if len(text) > 100]
    joined_first_page = "\n".join(first_page)

    # ask
    ans = nlpipe(question=f"Who has violated?", context=txt, topk=3)

    return ans


def ask_who_pay(first_page: list, nlpipe=None) -> str:
    """from a list of text lines, create a pipelie if needed and asqk question """

    # first_page_100 = [text for text in first_page if len(text) > 100]
    joined_first_page = "\n".join(first_page)

    # ask
    ans = nlpipe(question=f"Who has to pay?", context=txt, topk=3)

    return ans


def ask_who_defendant(first_page: list, nlpipe=None) -> str:
    """from a list of text lines, create a pipelie if needed and asqk question """

    # first_page_100 = [text for text in first_page if len(text) > 100]
    joined_first_page = "\n".join(first_page)

    # ask
    ans = nlpipe(question=f"Who is the defendant?", context=txt, topk=3)

    return ans


def get_defendant(first_page: list, nlpipe=None) -> str:
    """from a list of text lines, create a pipelie if needed and asqk question """

    # first_page_100 = [text for text in first_page if len(text) > 100]
    joined_first_page = "\n".join(first_page)

    # ask
    ans = nlpipe(question=f"Who is the defendant?", context=txt, topk=3)

    return ans[0]["answer"]
