from cleantext import clean
from legal_doc_processing import utils

from legal_doc_processing.utils import *
from legal_doc_processing.legal_doc.utils import *
from legal_doc_processing.legal_doc.segmentation.utils import *


def _split_pages(txt: str) -> list:
    """ """

    if "\x0c" in txt:
        pages = txt.split("\x0c")
    else:
        pages = [
            txt,
        ]

    return pages


def _split_lines_pages(pages: list) -> list:
    """ """

    return [i.split("\n") for i in pages]


def alex_clean(raw_txt):

    # 1st split by pages
    pages = _split_pages(raw_txt)

    lines_pages = _split_lines_pages(pages)

    # frist_page
    first_page = lines_pages[0]

    # find a first candidate for a REAL senetence
    # i, len char the line, the line itself
    cands_1st = [(i, len(j), j) for i, j in enumerate(first_page)]

    # then we want the len of this line, the len of the n+1 line, idem n+2, n+3
    cands_2nd = [
        (i, j, cands_1st[i + 1][1], cands_1st[i + 2][1], cands_1st[i + 3][1], k)
        for i, j, k in cands_1st[:-10]
    ]

    # we want to know if the 3 next lines will be len() > threshold
    threshold = 60
    cands_3rd = [
        (i, j >= threshold, k >= threshold, l >= threshold, m >= threshold, n)
        for i, j, k, l, m, n in cands_2nd
    ]

    cands_4rd = [(i, sum([j, k, l, m]), n) for i, j, k, l, m, n in cands_3rd]


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
