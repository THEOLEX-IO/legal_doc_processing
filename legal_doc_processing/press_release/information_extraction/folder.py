import os


def predict_folder(obj: dict) -> list:
    """init a pipe if needed, then ask all questions and group all questions ans in a list sorted py accuracy """

    _folder = obj["struct_text"]["folder"]
    _folder = _folder.split(" ")[-1]
    return [(_folder, 1)]


# if __name__ == "__main__":

#     # import
#     from legal_doc_processing.utils import get_pipeline, get_spacy, get_orgs, get_pers
#     from legal_doc_processing.press_release.loader import press_release_X_y
#     from legal_doc_processing.press_release.structure import structure_press_release

#     # structured_press_release_r
#     df = press_release_X_y()
#     df["structured_txt"] = [structure_press_release(i) for i in df.txt.values]

#     # one
#     one = df.iloc[0, :]
#     one_defendant = one.defendant
#     one_struct = struct_doc = one.structured_txt
#     one_h1 = one_struct["h1"]
#     one_article = one_struct["article"]
#     sub_one_article = "\n".join(one_article.split("\n")[:2])
#     pred = predict_id(one_struct)