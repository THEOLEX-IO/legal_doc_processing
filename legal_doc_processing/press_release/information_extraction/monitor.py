def predict_monitor(obj: dict) -> list:
    """ """

    monitor = 0

    for sent in obj["all_text_sents"]:
        if ("indepen" in sent) and ("complian" in sent) and ("monitor" in sent):
            monitor += 1

    return [("1", 0.5)] if monitor else [("0", 0.5)]
