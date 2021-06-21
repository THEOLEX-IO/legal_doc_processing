def predict_currency(struct_doc) -> list:

    # items
    h1 = struct_doc["h1"]
    sub_article = "\n".join(struct_doc["article"].split("\n")[:2])

    # dollar
    if ("$" in h1) or ("$" in sub_article):
        return [("$", 1)]

    return [(-1, -1)]