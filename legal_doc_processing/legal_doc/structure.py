from cleantext import clean as _clean


from legal_doc_processing import logger


def _del_dummy_breaklines(txt: str):
    """ """

    new_txt = (
        txt.replace("\n.", "$$$$")
        .replace("\n", " ")
        .replace("  ", " ")
        .replace("  ", " ")
        .replace("  ", " ")
        .replace("$$$$", "\n")
    )

    return new_txt


def _transform_double_breaks(txt: str, sep="\n----\n") -> str:
    """ """

    new_txt = (
        txt.replace("\n\n", sep)
        .replace("\n\n", sep)
        .replace("\n\n", sep)
        .replace("\n\n", sep)
        .replace("\n\n", sep)
    )

    return new_txt


def _del_double_spaces(txt: str) -> str:
    """ """

    new_txt = (
        txt.replace("  ", " ")
        .replace("  ", " ")
        .replace("  ", " ")
        .replace("  ", " ")
        .replace("  ", " ")
        .replace("  ", " ")
        .replace("  ", " ")
        .replace("  ", " ")
    )

    return new_txt


def _del_bouble_breaks(txt: str) -> str:
    """ """

    new_txt = (
        txt.replace("\n\n", "\n")
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
        .replace("\n\n", "\n")
    )

    return new_txt


def _detect_chapter(txt: str, threshold: int = 5, sep="----") -> str:
    """ """

    txt = txt.splitlines()

    cand_chapter = lambda i: i if ((len(i) >= threshold) or (i == sep)) else "!!!!\n" + i
    txt = [cand_chapter(i) for i in txt]

    return "\n".join(txt)


def _del_double_section(txt, sep="\n----\n"):
    """ """

    new_txt = (
        txt.replace(sep + sep, sep)
        .replace(sep + sep, sep)
        .replace(sep + sep, sep)
        .replace(sep + sep, sep)
        .replace(sep + sep, sep)
    )

    return new_txt


def _strip(txt: str) -> str:
    """ """

    txt = txt.splitlines()
    txt = [i.strip() for i in txt]

    return "\n".join(txt)


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


def _detect_true_text_id(first_page: str, line_length_txt=60, n_lines=4) -> int:
    """ """

    first_page = first_page.splitlines()

    # find a first candidate for a REAL senetence
    # i, len char the line, the line itself
    cands_1st = [(i, len(j), j) for i, j in enumerate(first_page)]

    # then we want the len of this line, the len of the n+1 line, idem n+2, n+3
    cands_2nd = [
        (
            i,
            [cands_1st[i + k][1] for k in range(n_lines)],
            k,
        )
        for i, j, k in cands_1st[: -(n_lines + 1)]
    ]

    # we want to know if the 3 next lines will be len() > threshold
    cands_3rd = [(i, sum([kk > line_length_txt for kk in j]), k) for i, j, k in cands_2nd]

    # if not all then True
    cands_5th = [(i, j, k) for i, j, k in cands_3rd if j >= n_lines]

    if not cands_5th:
        return -1
    return cands_5th[0][0]


def _do_split_header_page(txt, _id):
    """ """

    txt = txt.splitlines()

    header = txt[:_id]
    page = txt[_id:]

    return "\n".join(header), "\n".join(page)


def _ultimate_clean(txt: str) -> str:
    """ """

    txt = txt.splitlines()
    txt = [i.strip() for i in txt]
    txt = [i for i in txt if (i and (i != ")"))]
    txt = "\n".join(txt)

    return txt


def _transfert_title_from_head_to_page(header: str, page: str) -> tuple:
    """ """

    last_title = False

    one_of_in = lambda i: any(char in i for char in list("1il.,"))
    if len(header[-1]) <= 3 and one_of_in(header[-1].lower()):
        last_title = True

    if "introduc" in header[-1].lower():
        last_title = True

    if not last_title:
        return header, page

    # transfert last line to 1st line
    header, page = header.splitlines(), page.splitlines()
    title = header[-1]
    header = header[:-1]
    page = [
        title,
    ] + page

    header = "\n".join(header)
    page = "\n".join(page)

    return header, page


def structure_legal_doc(
    raw_txt, juridiction="", nlspa=None, line_length_txt=50, n_lines=5
):
    """ """

    # 1st split by pages
    pages = _split_pages(raw_txt)

    # frist_page
    first_page = pages[0]

    # clean
    first_page = _ultimate_clean(first_page)

    # id suposed begining of  true text
    i = _detect_true_text_id(first_page, line_length_txt=line_length_txt, n_lines=n_lines)
    # cand header and txt
    cand_header, cand_page_1 = _do_split_header_page(first_page, i)

    # pages
    pages[0] = cand_page_1

    # dump doubles lines
    cand_header = _del_bouble_breaks_and_spaces(cand_header)
    pages = [_del_bouble_breaks_and_spaces(i) for i in pages]

    # ultimate  clean
    cand_header = _ultimate_clean(cand_header)
    pages = [_del_dummy_breaklines(i) for i in pages]
    pages = [_ultimate_clean(i) for i in pages]

    # transfert last line if needed
    cand_header, pages[0] = _transfert_title_from_head_to_page(cand_header, pages[0])

    # detect section
    pages = [_detect_chapter(i) for i in pages]

    dd = {
        "header": cand_header,
        "pages": pages,
    }

    return dd


if __name__ == "__main__":

    # import
    from legal_doc_processing.legal_doc.utils import legal_doc_X_y

    #  dataframe and structured_legal_doc_
    df = legal_doc_X_y(features="defendant")
    df["structured_txt"] = [
        structure_legal_doc(i, line_length_txt=50, n_lines=5) for i in df.txt.values
    ]

    df["header"] = df.structured_txt.apply(lambda i: i["header"])
    df["first_page"] = df.structured_txt.apply(lambda i: i["pages"][0])

    keys = ["folder", "header", "first_page"]
    result = df.loc[:, keys]
    result.to_csv("./data/csv/alex_work_21-06-16.csv", index=False)
