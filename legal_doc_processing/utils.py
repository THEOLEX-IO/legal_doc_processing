import re


def clean(text: str) -> tuple:
    """first text cleaning based on regex, just keep text not spec chars
    return tupple of text"""

    # article text
    article_text = re.sub(r"\[[0-9]*\]", " ", text)
    article_text = re.sub(r"\s+", " ", article_text)

    # formated text
    formatted_article_text = re.sub("[^a-zA-Z]", " ", article_text)
    formatted_article_text = re.sub(r"\s+", " ", formatted_article_text)

    return article_text, formatted_article_text


def unicode_(text: str) -> str:
    """handle encoding problems and force ascii conversion ; return clean text """

    # encoding the text to ASCII format
    text_encode = text.encode(encoding="ascii", errors="ignore")

    # decoding the text
    text_decode = text_encode.decode()

    # cleaning the text to remove extra whitespace
    clean_text = " ".join([word for word in text_decode.split()])

    return clean_text


def is_section_num(text: str) -> bool:
    """detect if a paragrath start with Roman letter ie is a section; return bool """

    return re.search(r"^[MDCLXVIAB]+\.$", text) is not None


def ends_with_ponc(text: str, punctuation: str = "!.?") -> bool:
    """detect if a text finsih with punctation end of sentence; return bool"""

    return text[-1] in punctuation if text else False


def start_with_upper(text: str) -> bool:
    """fist letter of a text is upper; return bool"""

    return text[0].upper() == text[0]


def is_title(text: str, threshold=0.6) -> bool:
    """detect if text is a title if threshold % of the letters are upper; return bool """

    uppers = [word.isupper() for word in text.split(" ")]
    return sum(uppers) / len(uppers) > threshold


def same_sentence(sent1: str, sent2: str, short_sentence_length: int = 50) -> bool:
    # print(sent1,"\n",sent2)

    # TODO #

    # ASK PRECISIONS

    # TODO #

    # sent empty
    if (not sent1) or (not sent1["text"]):
        return True

    # section number
    if sent1["is_section_num"]:
        return True

    # very short sentence
    if len(sent1["text"]) < short_sentence_length:
        return False

    # ponctuation
    if sent1["ends_with_ponc"]:
        return False

    # title
    if sent1["is_title"] or sent2["is_title"]:
        return False

    return True


def clean_doc(file_text: str):
    """ """
    pages = []

    # split each page
    for page in file_text.split("\x0c"):

        # clen text
        page_meta = [
            {"text": clean(para, lower=False, no_line_breaks=True).replace("_", "")}
            for para in page.split("\n")
        ]
        clean_page = []
        previous_line = {}
        text = ""
        # add meta data
        for line in page_meta:
            line["is_section_num"] = is_section_num(line["text"])
            line["is_title"] = is_title(line["text"])
            line["ends_with_ponc"] = ends_with_ponc(line["text"])
            line["is_alpha"] = sum(c.isalpha() for c in line["text"])
            line["start_with_upper"] = start_with_upper(line["text"])

            # not relevant line
            if not line["is_alpha"]:
                continue

            if not same_sentence(previous_line, line):
                if text:
                    clean_page.append(text)
                    text = ""

            previous_line = line
            text = " ".join([text, line["text"]])
        if len(clean_page):
            pages.append(clean_page)
    return pages