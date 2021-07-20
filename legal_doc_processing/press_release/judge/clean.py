def clean_ans(ans: str) -> str:
    """ """

    ans = ans.lower()

    clean_list = [
        "district judge",
        "federal judge",
        "judge",
        "general attorney",
        "attorney",
    ]

    # filter judge or attorney
    for item in clean_list:
        ans = ans.replace(item, "").strip()

    # capitalize
    ans = ans.title()

    # dummy \n
    ans = ans.replace(".\n", ". \n").replace("\n", " ").replace("  ", " ").strip()

    return ans


def clean_ans_list(ans_list: list) -> list:
    """ """

    _ = [d.update({"new_answer": clean_ans(d["answer"])}) for d in ans_list]

    return ans_list