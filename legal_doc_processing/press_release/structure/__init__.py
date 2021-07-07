from legal_doc_processing import logger

from legal_doc_processing.utils import get_spacy, get_pipeline, get_label_

from legal_doc_processing.press_release.structure.cftc import (
    structure_press_release as structure_cftc,
)
from legal_doc_processing.press_release.structure.doj import (
    structure_press_release as structure_doj,
)


def structure_press_release(txt, nlspa=""):
    """ """

    # spacy
    if not nlspa:
        nlspa = get_spacy()
    try:
        nlspa.add_pipe("sentencizer")
    except Exception as e:
        pass

    # identifiers
    cftc_pairs = (
        "cftc",
        ["CFTC", "Commodity Futures Trading Commission"],
    )

    doj_pairs = (
        "doj",
        ["DOJ", "Department of Justice"],
    )

    # pairs and cands
    pairs = [cftc_pairs, doj_pairs]
    final_cands = list()

    # find a auth
    for auth, auth_cands in pairs:
        extract = [auth for cand in auth_cands if cand.lower() in txt.lower()]
        final_cands.extend(extract)

    assert len(final_cands) > 0
    auth = final_cands[0]

    # return funct
    if auth == "doj":
        return structure_doj(txt, nlspa=nlspa)
    if auth == "cftc":
        return structure_cftc(txt, nlspa=nlspa)
