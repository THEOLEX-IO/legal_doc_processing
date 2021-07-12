def clean(txt: str) -> str:
    """ """


def final_clean(txt: str) -> str:
    """ """

    # US
    txt = txt.replace("United States", "U.S")

    # errors
    errors_list = ["court of law", "judgment and order"]
    if txt.lower().strip() in errors_list:
        return ""

    # mandatories
    mand_list = ["court", "district", "federal", "tribunal", "us", "u.s", "united states"]
    _txt = txt.lower()
    if not any([(i in _txt) for i in mand_list]):
        return ""

    # \n
    slash_n_clean = (
        lambda j: j.replace(".\n", ". \n")
        .replace("\n", " ")
        .replace("  ", " ")
        .replace("  ", " ")
        .strip()
    )

    return slash_n_clean(txt)