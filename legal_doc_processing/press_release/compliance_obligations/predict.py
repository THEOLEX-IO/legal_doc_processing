from legal_doc_processing import logger

from legal_doc_processing.press_release.compliance_obligations.clean import final_clean


def predict_compliance_obligations(data: dict) -> list:
    """ """

    # make sent list, and filter not compliant in sent
    sent_list = data.content_sents
    filter_compliant = lambda j: "complian" in j.lower()
    compl_sent_list = [j for j in sent_list if filter_compliant(j)]

    # if no sents :
    if not compl_sent_list:
        return [("", 1)]

    # clean
    compl_sent_list = [final_clean(j) for j in compl_sent_list]

    return [(j, 1) for j in compl_sent_list]