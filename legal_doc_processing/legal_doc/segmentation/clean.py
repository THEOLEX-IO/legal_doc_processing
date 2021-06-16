from cleantext import clean
from legal_doc_processing import utils

from legal_doc_processing.utils import *
from legal_doc_processing.legal_doc.utils import *
from legal_doc_processing.legal_doc.segmentation.utils import *


def clean_doc(file_text):
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


def clean(file):
    article_text = re.sub(r"\[[0-9]*\]", " ", file)
    article_text = re.sub(r"\s+", " ", article_text)

    formatted_article_text = re.sub("[^a-zA-Z]", " ", article_text)
    formatted_article_text = re.sub(r"\s+", " ", formatted_article_text)
    return article_text, formatted_article_text
