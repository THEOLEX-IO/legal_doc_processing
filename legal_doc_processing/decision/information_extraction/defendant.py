from collections import Counter


def predict_defendant(press: dict, legal: dict, threshold: float = 0.1) -> list:
    """ """
    try:
        all_def = (
            press["_feature_dict"]["defendant"] + legal["_feature_dict"]["defendant"]
        )
        if not len(all_def):
            return [(-1, -1)]
        selected_def = [(i, j) for i, j in all_def if j > threshold]
        counter = Counter([i for i, _ in selected_def])
        twos = [i for i, j in counter.items() if j > 1]
        return twos

    except Exception as e:
        return [(-2, -1)]