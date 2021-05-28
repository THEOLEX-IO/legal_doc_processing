import os


# ### 1.5 - paths

one_file_path = "data/7162-15/"
one_file_path = os.getcwd() + "/" + one_file_path

order = "order-inter-global-currency.txt"
press = "press-release.txt"
one_file_order = one_file_path + order
one_file_press = one_file_path + press

assert os.path.isfile(one_file_order)
assert os.path.isfile(one_file_press)


def x_data_files(num: int = 10, _type: str = "order") -> list:
    """find in the -num- st data folders the files with good type (ie order or press) make a filter
    and retunr the list of files with usable paths"""

    # sanity check
    assert _type in ["press", "order", "complaint"]

    # list of data/*
    x_file_paths = os.listdir(os.getcwd() + "/data/")[:num]

    # for each path, list dir and filter
    x_files_list = list()
    _ = [
        x_files_list.extend(
            ["data/" + path_ + "/" + i for i in os.listdir("data/" + path_) if _type in i]
        )
        for path_ in x_file_paths
    ]

    return x_files_list
