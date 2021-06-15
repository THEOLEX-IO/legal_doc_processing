import pandas as pd

from legal_doc_processing.utils import (
    _if_not_pipe,
    _ask,
)


def _dummy_pred(txt):
    return 1


def predict_violation(structured_press_release: list, nlpipe=None):
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    # # pipe
    # nlpipe = _if_not_pipe(nlpipe)

    # # section cands
    # cands = [
    #     structured_press_release["h1"].lower(),
    #     structured_press_release["h2"].lower(),
    #     # article = structured_press_release["article"].lower()
    # ]

    # # eval
    # is_good = lambda sec: (
    #     (("accuse" in sec) and ("for" in sec))
    #     or (("accuse" in sec) and ("of" in sec))
    #     or (("charg" in sec) and ("for" in sec))
    #     or (("charg" in sec) and ("with" in sec))
    #     or (("order" in sec) and ("from" in sec))
    #     or (("impose" in sec) and ("for" in sec))
    #     or (("pay" in sec) and ("for" in sec))
    #     or (("judgment" in sec) and ("for" in sec))
    #     or (("judgment" in sec) and ("in" in sec)) in sec
    # )

    # # parse sections to know if ok
    # txt = ""
    # for section in cands:
    #     txt = section if is_good(section) else ""
    #     if txt:
    #         break

    # # if  nothing ok
    # if not txt:
    #     return "--None--"

    # # make dummy pred
    # ans = _dummy_pred(txt)

    # return ans
    return "-- None --"


if __name__ == "__main__":

    # import
    from legal_doc_processing.utils import *
    from legal_doc_processing.press_release.utils import load_press_release_text_list
    from legal_doc_processing.press_release.segmentation.structure import (
        structure_press_release,
    )

    # pipe
    nlpipe = get_pipeline()

    # # structured_press_release_list
    # press_txt_list = load_press_release_text_list()
    # structured_press_release_list = [structure_press_release(i) for i in press_txt_list]

    # # test one
    # structured_press_release = structured_press_release_list[0]

    # all_ans_h1 = _ask_all(structured_press_release["h1"], nlpipe)
    # all_ans_h2 = _ask_all(structured_press_release["h2"], nlpipe)
    # all_ans_article = _ask_all(structured_press_release["article"], nlpipe)

    # ans = predict_cost(structured_press_release, nlpipe)

    # # test others
    # ans_list = [predict_cost(p, nlpipe) for p in structured_press_release_list]

    # clean_ans_list = [[d["answer"] for d in ll] for ll in ans_list]
    # clean_ans_list = [", ".join(ll) for ll in clean_ans_list]
