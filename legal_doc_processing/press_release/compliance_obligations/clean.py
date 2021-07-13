def final_clean(txt: str) -> str:
    """ """

    clean = (
        lambda txt: txt.replace(".\n", ". \n")
        .replace("\n", " ")
        .replace("  ", " ")
        .replace("  ", " ")
    )

    return clean(txt)