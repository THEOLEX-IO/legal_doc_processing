from legal_doc_processing.press_release.utils import press_release_X_y
from legal_doc_processing.legal_doc.loader import legal_doc_X_y


def decision_X_y():
    # Press df
    press_df = press_release_X_y()
    # press_df = press_df.iloc[:4, :]
    new_cols = [i.replace("txt", "press_txt") for i in press_df.columns]
    press_df.columns = new_cols

    # Legal df
    legal_df = legal_doc_X_y()
    # legal_df = legal_df.iloc[:4, :]
    new_cols = [i.replace("txt", "legal_txt") for i in legal_df.columns]
    legal_df.columns = new_cols
    drop_cols = [i for i in legal_df.columns if (i != "folder") and (i != "legal_txt")]
    droped_legal_df = legal_df.drop(drop_cols, axis=1, inplace=False)

    # merged df
    assert ("folder" in droped_legal_df.columns) and ("folder" in press_df.columns)
    merged_df = press_df.merge(droped_legal_df, on="folder")

    return merged_df