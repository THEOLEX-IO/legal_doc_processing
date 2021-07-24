from legal_doc_processing import logger
import dateparser


def _you_shall_not_pass(date: str) -> str:
    """avoid passing for a studid algo """

    # validation funct
    funct = lambda i: True if str(i) in date else False

    # features to validate
    features = [(range(1979, 2023), "years"), (range(1, 32), "day")]

    # if a feature not in date retunr --None--
    for feat, _ in features:
        is_ok = any([funct(i) for i in feat])
        if not is_ok:
            return "--None--"

    return date


def force_dateformat(i: str) -> str:
    """force a date parse and if not working return dummt value """

    try:
        dd = dateparser.parse(i)

        if not 2025 >= int(dd.year) >= 1950:
            dd = "1900-01-01"

        str_dd = str(dd)[:10]
        return str_dd

    except Exception as e:

        logger.error(f"e : {e} for date  : {i} ")

        return "1900-01-01"
