import asyncio

import requests

import pandas as pd
import numpy as np

import re
import heapq

import nltk

from cleantext import clean

# nltk.download("stopwords")
stopwords = nltk.corpus.stopwords.words("english")


def load_data(file_path: str) -> str:
    """from file_path open read and return text; return text """

    if ".pdf" in file_path:
        raise AttributeError("Error : file recieved is a pdf, only txt supported")

    with open(file_path, "r") as f:
        txt = f.read()

    return txt


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


def get_token(text):
    sentence_list = nltk.sent_tokenize(text)
    sentence_list
    return sentence_list


def get_para(sentence_list):
    j = 0
    i = 0
    para = []
    paragraphes = {}
    idx = 0
    while i < len(sentence_list):
        para = []
        paragraphes["hearder"] = sentence_list[i]

        while not is_section_num(sentence_list[i]):
            para.append(sentence_list[i])
            i += 1

        if is_section_num(sentence_list[i - 1]):
            paragraphes["content"] = para
            paragraphes["id"] = idx
            idx = idx + 1

    return paragraphes


def get_section_indx(list_token):

    idx = []
    for i in range(len(list_token)):
        if is_title(list_token[i]):
            idx.append(i)

    return idx


def get_structure(text):
    list_token = get_token(text)
    idx = get_section_indx(list_token)
    j = 0

    structure = []
    k = 0
    for i in idx:
        section = {}
        section["content"] = " ".join(list_token[j:i])
        section["header"] = list_token[j]
        section["id"] = k
        structure.append(section)
        j = i
        k = k + 1

    return structure


def clean_doc(
    file_text,
):
    """ """

    pages = []
    for page in file_text.split("\x0c"):

        # clen text
        page_meta = [{"text": clean(para)} for para in page.split("\n")]
        clean_page = []
        previous_line = {}
        text = ""

        # add meta data
        for line in page_meta:
            line["is_section_num"] = is_section_num(str(line["text"]))
            line["is_title"] = is_title(str(line["text"]))
            line["ends_with_ponc"] = ends_with_ponc(str(line["text"]))
            line["is_alpha"] = sum(c.isalpha() for c in str(line["text"]))
            line["start_with_upper"] = starts_with_upper(str(line["text"]))

            # not relevant line
            if not line["is_alpha"]:
                continue

            if not same_sentence(previous_line, line):
                if text:
                    clean_page.append(text)
                    text = ""

            previous_line = line
            text = " ".join([text, str(line["text"])])

        if len(clean_page):
            pages.append(clean_page)

    return pages


def get_structured_document(file):
    text_structured = []
    file_cleaned = clean_doc(file)
    i = 0
    text_ = {}
    continu = []
    sec_num = 0
    while sec_num < len(file_cleaned):
        if is_title(file_cleaned[sec_num][0]):
            continu.append(file_cleaned[sec_num])
            text_["hearder"] = file_cleaned[sec_num][0]
            sec_num += 1
            while not is_title(file_cleaned[sec_num][0]) and sec_num < (
                len(file_cleaned)
            ):
                continu.append(file_cleaned[sec_num])
                sec_num += 1
            if is_title(file_cleaned[sec_num][0]):
                text_["content"] = continu
                text_["id"] = i
                text_["hearder"] = file_cleaned[sec_num][0]
                sec_num += 1
                continu = []
                i += 1
            else:
                text_["content"] = continu
                text_["id"] = i

        text_structured.append(text_)

    return text_structured


def word_frequency(text):
    stopwords = nltk.corpus.stopwords.words("english")
    word_frequencies = {}
    for word in nltk.word_tokenize(text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    return word_frequencies


def sentence_score(sentence_list, word_frequencies):
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(" ")) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    return sentence_scores


def make_dataframe(
    path: str = "./data/csv/original_dataset.csv", n: int = 10
) -> pd.DataFrame:
    """on basis of csv dataframe with all features, data clean, scrap googleapi and insert text in the dataframe
    :param path  = the path to read original dataset
    :param n     = the n-st line to scrap, other will be droped
    :return      = a dataframe with original data cleaned + text of main doc and press release
    """

    # read df
    df = pd.read_csv(path)

    # keep cols
    keep_cols = [
        "id",
        "name",
        "status",
        "reference",
        "document_link",
        "press_release_link",
        "monetary_sanction",
        "currency",
        "type",
        "justice_type",
        "defendant",
        "decision_date",
        "extracted_violations",
    ]

    drop_cols = [i for i in df.columns if i not in keep_cols]
    df = df.drop(drop_cols, axis=1)

    # fill rate
    fill_rate = lambda col: (len(df) - sum(df[col].isna())) / len(df)
    df_rate_fill = [(col, round(fill_rate(col), 2)) for col in df.columns]

    # press_release and document_link
    for col, ext in [("press_release", ".html"), ("document", ".txt")]:
        funct = (
            lambda i: np.nan if ("storage.google" not in i) else i.replace(".pdf", ext)
        )
        df[col + "_URL"] = df[col + "_link"].apply(lambda i: funct(str(i).strip()))

    # clean lines without press or document
    df = df.loc[~df.document_URL.isna(), :]
    df = df.loc[~df.press_release_URL.isna(), :]
    df.index = range(len(df))

    def scrap(url: str):
        """ """

        try:
            print(url)
            res = requests.get(url)

            if res.status_code < 300:
                return res.text
            else:
                return res.status_code

        except Exception as e:
            return str(e)

    # test on 10
    df = df.iloc[:n, :]

    # sync version
    for col in ["press_release", "document"]:
        df[col + "_TEXT"] = df[col + "_URL"].apply(lambda i: scrap(str(i).strip()))

    df.to_csv("./data/csv/dataset.csv", index=False)

    return df