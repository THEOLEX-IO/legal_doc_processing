import pandas as pd


def filter_juridiction(i: str, jur: str) -> str:
    """ """

    if not isinstance(i, str):
        return ""
    if not str("" + jur.lower() + "/") in i.lower():
        return ""

    return i


def filter_ext(i: str, ext: str) -> str:
    """ """

    ext = ext if ext[0] == "." else str("." + ext)
    if not isinstance(i, str):
        return ""
    if not ext.lower() in i.lower():
        return ""

    return i


def filter_press_release(i: str, press_release: bool) -> str:
    """ """

    press = "press-release"

    if press_release:
        return i if press in i else ""

    return "" if press in i else i


def get_document_link(doc_list):
    docs = [doc for doc in doc_list if "press-release" not in doc]
    accepted_words = ["deferred", "order", "complaint", "agreement", "indictment"]
    for word in accepted_words:
        for doc in doc_list:
            if word in doc:
                return doc

    return docs[0] if docs else None


def select_best_file(l: list) -> str:
    if not len(l):
        return ""
    if len(l) == 1:
        return l[0]

    return get_document_link(l)


def handle_multiple_file_problem(doc_pair_list: list) -> list:
    """ """

    # we are gonna, make a df
    tmp_list = [{"folder": i, "filename": j} for i, j in doc_pair_list]
    tmp_df = pd.DataFrame(tmp_list)
    tmp_df.head(10)

    # group by and render a list(tupple(str, list)) object
    tmp_clean_list = list()
    for k, sub_df in tmp_df.groupby("folder"):
        tu = (k, list(sub_df.filename.values))
        tmp_clean_list.append(tu)
    tmp_clean_list[:5]

    # clean
    tmp_clean_list = [(i, select_best_file(j)) for i, j in tmp_clean_list]
    print(tmp_clean_list[:5])

    return tmp_clean_list