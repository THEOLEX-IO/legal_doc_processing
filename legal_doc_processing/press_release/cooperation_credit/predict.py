from legal_doc_processing import logger

from legal_doc_processing.utils import uniquize as _u

# from legal_doc_processing.utils import merge_ans, ask_all

from legal_doc_processing.press_release.cooperation_credit.clean import final_clean


def predict_cooperation_credit(
    data: dict, threshold: float = 0.25, n_sents: int = 5
) -> list:
    """  """

    # make sent list, and filter not cooperat in sent :
    sent_list = data.content_sents
    filter_coop = lambda txt: "cooperat" in txt.lower()
    coop_sent_list = [i for i in sent_list if filter_coop(i)]

    # if no sents :
    if not coop_sent_list:
        return [("", 1)]

    # clean
    coop_sent_list = [final_clean(j) for j in coop_sent_list]

    return [(j, 1) for j in coop_sent_list]
