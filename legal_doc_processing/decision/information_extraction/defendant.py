from legal_doc_processing import logger


from collections import Counter
from legal_doc_processing.utils import softmax, merge_ans


def predict_defendant(
    press: dict,
    legal: dict,
    threshold: float = 0.1,
    softmax_threshold: float = 0.2,
) -> list:
    """ """

    press_def = press["_defendant"]
    legal_def = legal["_defendant"]

    ans = []

    # both null
    if (not press_def) and not (legal_def):
        ans = [(-1, -1)]
    # one null
    elif not press_def:
        ans = legal_def
    elif not (legal_def):
        ans = press_def

    if ans:
        return ans

    # join preds
    all_def = press_def + legal_def

    # non null
    selected_def = [(i, j) for i, j in all_def if j > 0.1]
    if not selected_def:
        ans = [(-2, -1)]

    if ans:
        return ans

    # counter
    counter = Counter([i for i, _ in selected_def])
    twos = [i for i, j in counter.items() if j > 1]

    # both the same
    if len(press_def) == len(legal_def):
        if len(twos) == len(press_def):
            both = [{"answer": i, "score": j} for i, j in selected_def]
            merged_both = merge_ans(both, "answer")
            ans = [(i["answer"], i["cum_score"]) for i in merged_both]

    if ans:
        return ans

    # softmax
    keys, values = zip(*press_def)
    _values = [round(i, 4) for i in softmax(values)]
    softmax_press = zip(keys, _values)
    keys, values = zip(*legal_def)
    _values = [round(i, 4) for i in softmax(values)]
    softmax_legal = zip(keys, _values)

    # over weight ans in both
    update_tuple = lambda i, j: (i, j) if (i not in twos) else (i, j + 0.3)
    new_press = [update_tuple(i, j) for i, j in softmax_press]
    new_legal = [update_tuple(i, j) for i, j in softmax_legal]

    # new_selected_df as dict
    new_selected_df = new_legal + new_press
    new_selected_df = [{"answer": i, "score": j} for i, j in new_selected_df]
    merged_new = merge_ans(new_selected_df, "answer")
    ans = [(i["answer"], i["cum_score"]) for i in merged_new]

    # softmax threshold if len 4
    if len(ans) >= 4:
        keys, values = zip(*ans)
        _values = [round(i, 4) for i in softmax(values)]
        ans = zip(keys, _values)
        ans = [(i, j) for i, j in ans if j > softmax_threshold]

    return ans
