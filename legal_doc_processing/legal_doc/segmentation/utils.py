import asyncio

import requests

import pandas as pd
import numpy as np

import re
import heapq

import nltk

from cleantext import clean
import spacy


def is_section_num(text: str) -> bool:
    """detect if a paragrath start with Roman letter ie is a section; return bool """

    return re.search(r"^[MDCLXVIAB]+\.$", text) is not None


def ends_with_ponc(text: str, punctuation: str = "!.?") -> bool:
    """detect if a text finsih with punctation end of sentence; return bool"""

    return text[-1] in punctuation if text else False


def starts_with_upper(text: str) -> bool:
    """fist letter of a text is upper; return bool"""

    return re.match("^[A-Z]", text) is not None


def is_title(text: str, threshold=0.6) -> bool:
    """detect if text is a title if threshold % of the letters are upper; return bool """

    uppers = [word.isupper() for word in text.split(" ")]

    return sum(uppers) / len(uppers) > threshold


def clean_spec_chars(text: str) -> tuple:
    """first text cleaning based on regex, just keep text not spec chars
    return tupple of text"""

    # article text
    article_text = re.sub(r"\[[0-9]*\]", " ", text)
    article_text = re.sub(r"\s+", " ", article_text)

    # formated text
    formatted_article_text = re.sub("[^a-zA-Z]", " ", article_text)
    formatted_article_text = re.sub(r"\s+", " ", formatted_article_text)

    return article_text, formatted_article_text


def same_sentence(sent1, sent2):
    # print(sent1,"\n",sent2)

    # sent empty
    if (not sent1) or (not sent1["text"]):
        return True
    # section number
    if sent1["is_section_num"]:
        return True

    # very short sentence
    if len(sent1["text"]) < 50:
        return False

    # ponctuation
    if sent1["ends_with_ponc"]:
        return False

    if sent1["is_title"]:
        return False

    if sent2["is_title"]:
        return False

    return True


def get_token(text):
    sentence_list = nltk.sent_tokenize(text)

    return sentence_list


# def get_para(sentence_list):
#     j = 0
#     i = 0
#     para = []
#     paragraphes = {}
#     idx = 0
#     while i < len(sentence_list):
#         para = []
#         paragraphes["hearder"] = sentence_list[i]

#         while not is_section_num(sentence_list[i]):
#             para.append(sentence_list[i])
#             i += 1

#         if is_section_num(sentence_list[i - 1]):
#             paragraphes["content"] = para
#             paragraphes["id"] = idx
#             idx = idx + 1

#     return paragraphes


def get_section_indx(list_token):
    """ """

    idx = []
    for i in range(len(list_token)):
        if is_title(list_token[i]):
            idx.append(i)

    return idx


# def word_frequency(text):
#     stopwords = nltk.corpus.stopwords.words("english")
#     word_frequencies = {}
#     for word in nltk.word_tokenize(text):
#         if word not in stopwords:
#             if word not in word_frequencies.keys():
#                 word_frequencies[word] = 1
#             else:
#                 word_frequencies[word] += 1
#     return word_frequencies


# def sentence_score(sentence_list, word_frequencies):
#     sentence_scores = {}
#     for sent in sentence_list:
#         for word in nltk.word_tokenize(sent.lower()):
#             if word in word_frequencies.keys():
#                 if len(sent.split(" ")) < 30:
#                     if sent not in sentence_scores.keys():
#                         sentence_scores[sent] = word_frequencies[word]
#                     else:
#                         sentence_scores[sent] += word_frequencies[word]
#     return sentence_scores


def get_entities(section):
    entities = []
    # Load English tokenizer, tagger, parser and NER
    nlp = spacy.load("en_core_web_sm")
    # Process whole documents
    for text in section:
        text = "\n".join(section[2]["content"])
        doc = nlp(text)
        # Find named entities, phrases and concepts
        for entity in doc.ents:
            if entity.label_ == "ORG":
                entities.append([entity.text, ":       ", entity.label_])

    return entities