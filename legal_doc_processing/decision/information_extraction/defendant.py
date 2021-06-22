from collections import Counter


def predict_defendant(press: dict, legal: dict, threshold: float = 0.1) -> list:
    """ """

    # print(press)
    # print(legal)
    all_def = press["_defendant"] + legal["_defendant"]

    try:

        if not len(all_def):
            return [(-1, -1)]
        selected_def = [(i, j) for i, j in all_def if j > threshold]
        counter = Counter([i for i, _ in selected_def])
        twos = [i for i, j in counter.items() if j > 1]
        return twos

    except Exception as e:
        return [(-2, -1)]