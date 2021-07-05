from legal_doc_processing import logger


def _you_shall_not_pass(date: str) -> str:
    """avoid passing for a studid algo """

    # validation funct
    funct = lambda i: True if str(i) in date else False

    # features to validate
    features = [(range(1979, 2023), "years"), (range(1, 32), "day")]

    # if a feature not in date retunr --None--
    for feat, _ in features:
        is_ok = bool(sum([funct(i) for i in feat]))
        if not is_ok:
            return "--None--"

    return date