def predict_compliance_obligations(data: dict) -> list:
    """ """

    # make sent list, and filter not cooperat in sent
    sent_list = data.content_sents
    compliant_ok = lambda j: ("complian" in j.lower())
    compl_sent_list = [(i, j) for i, j in enumerate(sent_list) if compliant_ok(j)]

    # if no sents :
    if not len(compl_sent_list):
        return [(-1, 1)]

    clean = lambda j: j.replace(".\n", ". \n").replace("\n", "")
    return [(clean(j), 1) for _, j in compl_sent_list]