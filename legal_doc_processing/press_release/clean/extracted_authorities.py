from legal_doc_processing import logger

from legal_doc_processing.press_release.utils import product_juridiction_pairs


def _filter_jur(token, cands: list = None):
    """ """

    if not cands:
        cands = product_juridiction_pairs()

    for k, v in cands.items():
        if token.lower().strip() == k.lower().strip():
            return v.upper()

    return ""
