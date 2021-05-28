import re
import heapq

import nltk

from cleantext import clean


stopwords = nltk.corpus.stopwords.words("english")


def load_data(file_path: str) -> str:
    """from file_path open read and return text; return text """

    if ".pdf" in file_path:
        raise AttributeError("Error : file recieved is a pdf, only txt supported")

    with open(file_path, "r") as f:
        txt = f.read()

    return txt


# def clean_spec_chars(text: str) -> tuple:
#     """first text cleaning based on regex, just keep text not spec chars
#     return tupple of text"""

#     # article text
#     article_text = re.sub(r"\[[0-9]*\]", " ", text)
#     article_text = re.sub(r"\s+", " ", article_text)

#     # formated text
#     formatted_article_text = re.sub("[^a-zA-Z]", " ", article_text)
#     formatted_article_text = re.sub(r"\s+", " ", formatted_article_text)

#     return article_text, formatted_article_text


# def handle_encoding(text: str) -> str:
#     """handle encoding problems and force ascii conversion ; return clean text """

#     # encoding the text to ASCII format
#     text_encode = text.encode(encoding="ascii", errors="ignore")

#     # decoding the text
#     text_decode = text_encode.decode()

#     # cleaning the text to remove extra whitespace
#     clean_text = " ".join([word for word in text_decode.split()])

#     return clean_text


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


# def get_structured_document(file):

#     text_structured = []
#     file_cleaned = clean_doc(file)
#     i = 0
#     for pages in file_cleaned:
#         text_ = {}
#         text_["content"] = pages
#         text_["id"] = i
#         if is_title(pages[0]):
#             text_["header"] = pages[0]

#         text_structured.append(text_)
#         i += 1

#     return text_structured


# def word_frequency(text):
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
