import re

from legal_doc_processing import logger


def predict_reference(obj: dict, length_treshold=50) -> list:
    """parse the first page line by line, matching a
    regex pattern refering to case feature
    example 'NO.: 14-CV-81216'
    return the result"""

    # use header and 1st page
    txt = obj["h1"] + obj["abstract"]
    first_page = txt.splitlines()
    first_page = [i for i in first_page if len(i) >= 4]

    # format result
    format_result = (
        lambda i: i.group(0)
        .upper()
        .replace("NO.", "")
        .replace("NO", "")
        .replace(":", "")
        .strip()
    )

    rr = None

    # first search smthg with - 99-CV-99999 -
    p = re.compile("\d*-?CV-\d+.*")
    for line in first_page:
        result = p.search(line.upper())
        if result:
            rr = format_result(result)
            break

    # first search smthg with - No.: -
    p = re.compile("NO[\.:]\s*.+")
    for line in first_page:
        result = p.search(line.upper())
        if result:
            rr = format_result(result)
            break

    if not rr:
        return [("--None--", -1)]

    rr = rr.split(",")[0].strip().replace("'", "")
    rr = rr.replace("—", "-")

    if "-" in rr:
        r_spilt = rr.split("-")
        rr = "-".join([i.strip() for i in r_spilt])

    return [(rr, 1)]


if __name__ == "__main__":

    # import
    import time
    from legal_doc_processing.utils import get_pipeline, get_spacy
    from legal_doc_processing.legal_doc.loader import legal_doc_X_y
    from legal_doc_processing.legal_doc.legal_doc import LegalDoc

    # laod
    nlpipe = get_pipeline()
    nlspa = get_spacy()
    nlspa.add_pipe("sentencizer")

    # data
    threshold = 0.2
    n_sents = 7
    feature = "reference"

    # structured_press_release_r
    df = legal_doc_X_y(features="defendant")
    df = df.iloc[:2, :]
    df["ld"] = [LegalDoc(i, nlpipe=nlpipe, nlspa=nlspa) for i in df.txt.values]

    # preds
    t = time.time()
    # 28 objects --> 181 secondes so --> +/-10 secondes per objects
    df["pred_" + feature] = df.ld.apply(lambda i: i.predict(feature))
    t = time.time() - t

    # 1st one
    one = df.iloc[0, :]
    one_txt = one.txt
    one_ld = self = one.ld
    obj = self.data