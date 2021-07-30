from legal_doc_processing.press_release.extracted_authorities import juridiction_pairs


def _filter_jur(token, cands: list = None):
    """ """

    if not cands:
        cands = juridiction_pairs()

    for k, v in cands.items():
        if token.lower().strip() == k.lower().strip():
            return v.upper()

    return ""
