import os


def predict_date(
    structured_press_release: list,
) -> str:
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    date = structured_press_release["date"]

    return date


if __name__ == "__main__":

    # import
    from legal_doc_processing.utils import *
    from legal_doc_processing.press_release.segmentation.structure import (
        structure_press_release,
    )

    # file list
    folder_list = os.listdir("./data/files")
    files_list = [
        [
            f"./data/files/{f}/{i}"
            for i in os.listdir(f"./data/files/{f}")
            if ("press" in i) and ("txt" in i)
        ]
        for f in folder_list
    ]
    files_list = [i[0] for i in files_list]

    # structure all press release
    press_txt_list = [load_data(i) for i in files_list]
    structured_press_release_list = [structure_press_release(i) for i in press_txt_list]

    # test one
    structured_press_release = structured_press_release_list[0]
    ans = predict_date(structured_press_release)

    # test others
    ans_list = [predict_date(p) for p in structured_press_release_list]
