import os

from legal_doc_processing import logger


def predict_folder(data: dict) -> list:
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    # _folder = obj["struct_text"]["folder"]
    # _folder = _folder.split(" ")[-1]
    # return [(_folder, 1)]

    return [(-1, -1)]
