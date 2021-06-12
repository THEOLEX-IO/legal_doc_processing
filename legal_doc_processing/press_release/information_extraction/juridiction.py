from legal_doc_processing.utils import (
    _if_not_pipe,
    _ask,
)

import os

import pandas as pd

from legal_doc_processing.utils import (
    _if_not_pipe,
    _ask,
)




def predict_juridiction(structured_press_release: list, nlpipe=None):
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    # choose the item
    h1 = structured_press_release["h1"]
    h2 = structured_press_release["h2"]


    if "CFTC" in h1 : 
        return "CFTC"


    if "SEC" in h1 : 
        return "SEC"

    if "DOJ" in h1 : 
        return "DOJ"


    # ask all and get all possible response
    ans = _ask_all(txt, nlpipe)

    # group by ans, make cumulative sum of accuracy for eash ans and filter best ones
    ll = _clean_ans(ans)

    # reponse
    resp = ", ".join([i["answer"] for i in ll])

    return resp


if __name__ == "__main__":

    # # import
    # from legal_doc_processing.utils import *
    # from legal_doc_processing.press_release.utils import *
    # from legal_doc_processing.press_release.segmentation.structure import (
    #     structure_press_release,
    # )

    # # pipe
    # nlpipe = get_pipeline()

    # # structured_press_release_list
    # press_txt_list = load_press_release_text_list()
    # structured_press_release_list = [structure_press_release(i) for i in press_txt_list]

    # # test one
    # structured_press_release = structured_press_release_list[0]

    # all_ans_h1 = _ask_all(structured_press_release["h1"], nlpipe)
    # all_ans_h2 = _ask_all(structured_press_release["h2"], nlpipe)
    # all_ans_article = _ask_all(structured_press_release["article"], nlpipe)

    # ans = predict_plaintiff(structured_press_release, nlpipe)

    # # test others
    # ans_list = [predict_plaintiff(p, nlpipe) for p in structured_press_release_list]
    # clean_ans_list = [[d["answer"] for d in ll] for ll in ans_list]
    # clean_ans_list = [", ".join(ll) for ll in clean_ans_list]
