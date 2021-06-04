# import re
# import pickle

# import spacy
# from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer
from legal_doc_processing.information_extraction.utils import get_pipeline


def ask_who_charged(first_page: list, nlpipe=None) -> str:
    """from a list of text lines, create a pipelie if needed and asqk question """

    # first_page_100 = [text for text in first_page if len(text) > 100]

    # ask
    ans = nlpipe(question="Who is charged?", context=txt, topk=3)

    return ans


def ask_who_accused(first_page: list, nlpipe=None) -> str:
    """from a list of text lines, create a pipelie if needed and asqk question """

    # ask
    ans = nlpipe(question="Who is accused?", context=txt, topk=3)

    return ans


def ask_who_violated(first_page: list, nlpipe=None) -> str:
    """from a list of text lines, create a pipelie if needed and asqk question """

    # ask
    ans = nlpipe(question="Who has violated?", context=txt, topk=3)

    return ans


def ask_who_pay(first_page: list, nlpipe=None) -> str:
    """from a list of text lines, create a pipelie if needed and asqk question """

    # ask
    ans = nlpipe(question="Who has to pay?", context=txt, topk=3)

    return ans


def ask_who_defendant(first_page: list, nlpipe=None) -> str:
    """from a list of text lines, create a pipelie if needed and asqk question """

    # ask
    ans = nlpipe(question="Who is the defendant?", context=txt, topk=3)

    return ans


def get_defendant(first_page: list, nlpipe=None) -> str:
    """from a list of text lines, create a pipelie if needed and asqk question """

    # ask
    ans = nlpipe(question="Who is the defendant?", context=txt, topk=3)

    return ans[0]["answer"]


if __name__ == "__main__":

    ans = []

    funct_quest_pairs = [
        (ask_who_charged, "ask_who_charged"),
        (ask_who_defendant, "ask_who_defendant"),
        (ask_who_violated, "ask_who_violated"),
        (ask_who_pay, "ask_who_pay"),
        (ask_who_accused, "ask_who_accused"),
    ]

    for funct, quest in funct_quest_pairs:
        ds = funct(txt, ld.nlpipe)
        _ = [d.update({"question": quest}) for d in ds]
        ans.extend(ds)

    ans = sorted(ans, key=lambda i: i["score"], reverse=True)
