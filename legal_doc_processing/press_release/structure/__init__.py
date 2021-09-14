from legal_doc_processing import logger

from legal_doc_processing.utils import get_spacy, get_pipeline, get_label_

from legal_doc_processing.press_release.structure.cftc import (
    structure_press_release as structure_cftc,
)
from legal_doc_processing.press_release.structure.doj import (
    structure_press_release as structure_doj,
)

from legal_doc_processing.press_release.structure.cfbp import (
    structure_press_release as structure_cfbp,
)

from legal_doc_processing.press_release.structure.sec import (
    structure_press_release as structure_sec,
)


def structure_press_release(txt, juridiction="", nlspa=None):
    """ """

    # spacy
    if not nlspa:
        nlspa = get_spacy()
    try:
        nlspa.add_pipe("sentencizer")
    except Exception as e:
        pass

    # if  juridiction --> EASY
    if juridiction == "cfbp":
        return structure_cfbp(txt, nlspa=nlspa)
    if juridiction == "cftc":
        return structure_cftc(txt, nlspa=nlspa)
    if juridiction == "doj":
        return structure_doj(txt, nlspa=nlspa)
    if juridiction == "sec":
        return structure_sec(txt, nlspa=nlspa)

    # ELSE TRY TO FIND JURIDICTION
    # identifiers
    cftc_pairs = (
        "cftc",
        ["CFTC", "Commodity Futures Trading Commission"],
    )

    doj_pairs = (
        "doj",
        ["DOJ", "Department of Justice"],
    )

    cfbp_pairs = (
        "cfbp",
        ["cfbp", "Consumer Financial Protection Bureau"],
    )

    sec_pairs = (
        "sec",
        ["Securities and Exchange Commission", "S.E.C", " SEC"],
    )

    # pairs and cands
    pairs = [cftc_pairs, doj_pairs, cfbp_pairs, sec_pairs]
    final_cands = list()

    # find a auth
    for auth, auth_cands in pairs:
        extract = [auth for cand in auth_cands if cand.lower() in txt.lower()]
        final_cands.extend(extract)

    if len(final_cands) <= 0:
        raise AssertionError
    auth = final_cands[0]

    # return funct
    if auth == "cfbp":
        return structure_cfbp(txt, nlspa=nlspa)
    if auth == "cftc":
        return structure_cftc(txt, nlspa=nlspa)
    if auth == "doj":
        return structure_doj(txt, nlspa=nlspa)
    if auth == "sec":
        return structure_sec(txt, nlspa=nlspa)
