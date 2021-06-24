def predict_monitor(obj: dict) -> list:
    """ """

    "compliance monitor"

    if "monitor" in obj["abstract"]:

        return [("1", 0.5)]

    return [("0", 0.5)]
