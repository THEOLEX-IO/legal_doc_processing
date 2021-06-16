from cleantext import clean

# from legal_doc_processing import utils

# from legal_doc_processing.utils import *
# from legal_doc_processing.legal_doc.utils import *
# from legal_doc_processing.legal_doc.segmentation.utils import *


def _del_bouble_breaks_and_spaces(txt: str) -> str:
    """ """

    new_txt = (
        txt.replace("\n\n", "\n")
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
        .replace("  ", " ")
        .replace("  ", " ")
        .replace("  ", " ")
        .replace("  ", " ")
        .replace("  ", " ")
        .replace("  ", " ")
        .replace("  ", " ")
        .replace("  ", " ")
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
    )

    return new_txt


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


def _detect_true_text_id(first_page: list, true_txt=60) -> int:
    """ """

    # find a first candidate for a REAL senetence
    # i, len char the line, the line itself
    cands_1st = [(i, len(j), j) for i, j in enumerate(first_page)]

    # then we want the len of this line, the len of the n+1 line, idem n+2, n+3
    cands_2nd = [
        (i, j, cands_1st[i + 1][1], cands_1st[i + 2][1], cands_1st[i + 3][1], k)
        for i, j, k in cands_1st[:-10]
    ]

    # we want to know if the 3 next lines will be len() > threshold
    cands_3rd = [
        (i, j >= true_txt, k >= true_txt, l >= true_txt, m >= true_txt, n)
        for i, j, k, l, m, n in cands_2nd
    ]

    # make the sum of len line line +1, line +2 etc
    cands_4th = [(i, sum([j, k, l, m]), n) for i, j, k, l, m, n in cands_3rd]

    cands_5th = [(i, j, k) for i, j, k in cands_4th if j >= 4]

    if not len(cands_5th):
        return -1
    else:
        return cands_5th[0][0]


def _ultimate_clean(txt: str) -> str:
    """ """

    txt = txt.splitlines()
    txt = [i for i in txt if i and i != " "]
    txt = "\n".join(txt)

    return txt


def alex_clean(raw_txt):

    # 1st split by pages
    pages = _split_pages(raw_txt)

    lines_pages = _split_lines_pages(pages)

    # frist_page
    first_page = lines_pages[0]

    # id suposed begining of  true text
    _id = _detect_true_text_id(first_page)

    # cand header and txt
    cand_header = first_page[:_id]
    cand_text = first_page[_id:]

    # regroup
    cand_header = "\n".join([i for i in cand_header if i])
    cand_text = "\n".join([i for i in cand_text if i])

    # dump doubles lines
    cand_header = _del_bouble_breaks_and_spaces(cand_header)
    cand_text = _del_bouble_breaks_and_spaces(cand_text)

    # ultimate  clean

    dd = {"header": cand_header, "text": cand_text}

    return dd


# def clean_doc(file_text):
#     pages = []


#     for page in file_text.split("\x0c"):
#         # clen text
#         page_meta = [{"text": clean(para)} for para in page.split("\n")]
#         clean_page = []
#         previous_line = {}
#         text = ""
#         # add meta data
#         for line in page_meta:
#             line["is_section_num"] = is_section_num(str(line["text"]))
#             line["is_title"] = is_title(str(line["text"]))
#             line["ends_with_ponc"] = ends_with_ponc(str(line["text"]))
#             line["is_alpha"] = sum(c.isalpha() for c in str(line["text"]))
#             line["start_with_upper"] = starts_with_upper(str(line["text"]))

#             # not relevant line
#             if not line["is_alpha"]:
#                 continue

#             if not same_sentence(previous_line, line):
#                 if text:
#                     clean_page.append(text)
#                     text = ""

#             previous_line = line
#             text = " ".join([text, str(line["text"])])
#         if len(clean_page):
#             pages.append(clean_page)
#     return pages


# def clean(file):
#     article_text = re.sub(r"\[[0-9]*\]", " ", file)
#     article_text = re.sub(r"\s+", " ", article_text)

#     formatted_article_text = re.sub("[^a-zA-Z]", " ", article_text)
#     formatted_article_text = re.sub(r"\s+", " ", formatted_article_text)
#     return article_text, formatted_article_text


if __name__ == "__main__":

    # import
    from legal_doc_processing.legal_doc.utils import legal_doc_X_y

    #  dataframe and structured_legal_doc_
    df = legal_doc_X_y(features="defendant")
    df["structured_txt"] = [alex_clean(i) for i in df.txt.values]

    df["header"] = df.structured_txt.apply(lambda i: i["header"])
    df["first_page"] = df.structured_txt.apply(lambda i: i["text"])

    keys = ["folder", "header", "first_page"]
    result = df.loc[:, keys]
    result.to_csv("./data/csv/alex_work_21-06-16.csv", index=False)
