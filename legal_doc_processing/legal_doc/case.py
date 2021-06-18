import re


def predict_case(struct_doc, length_treshold=50):
    """parse the first page line by line, matching a
    regex pattern refering to case feature
    example 'NO.: 14-CV-81216'
    return the result"""

    # use header and 1st page
    txt = struct_doc["header"] + struct_doc["pages"][0]

    # split
    first_page = txt.splitlines()

    # dump small char lines
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
