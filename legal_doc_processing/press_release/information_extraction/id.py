def predict_id(
    structured_press_release: list,
) -> str:
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    _id = structured_press_release["id"]

    _id = _id.split(" ")[-1]
    return _id
