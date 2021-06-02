import os


def clean_data_folder(root="data/files/"):
    """read all data/*/*, delete .pdf, keep only .txt """

    folders = os.listdir(f"{root}")
    all_files = list()

    _ = [
        all_files.extend([f"{root}{fold}/{fi}" for fi in os.listdir(f"{root}{fold}")])
        for fold in folders
    ]

    # files
    not_text = [i for i in all_files if ".txt" not in i]
    only_text = [i for i in all_files if ".txt" in i]

    # remove not .txt
    _ = [os.remove(i) for i in not_text]


def find_files_type(root="data/files/"):
    """ """

    # all files
    folders = os.listdir(f"root")
    all_files = list()

    _ = [
        all_files.extend([f"{root}/{fold}/{fi}" for fi in os.listdir(f"{root}/{fold}")])
        for fold in folders
    ]

    # files text not text
    not_text = [i for i in all_files if ".txt" not in i]
    only_text = [i for i in all_files if ".txt" in i]

    # press / not press
    text_not_press = [i for i in only_text if "press" not in i]
    text_only_press = [i for i in only_text if "press" in i]

    # files
    files = sorted(["-".join(fn.split("/")[-1].split("-")[:2]) for fn in text_not_press])

    # ans is
    files_types = [
        "amended-complaint",
        "cftc-whistleblower",
        "complaint",
        "commissioner",
        "consent-final",
        "concurring-statement",
        "consent-order",
        "contempt-order",
        "default-judgment",
        "enforcement-advisory",
        "final-judgment",
        "final-order",
        "judgment",
        "memorandum",
        "non-prosecution",
        "notice",
        "opinion-and",
        "opinion-order",
        "order",
        "proposed-consent",
        "remarks-of",
        "report-and",
        "statutory-restraining",
        "supplement-order",
        "supplemental-consent",
    ]


def x_data_files(num: int = 10, _type: str = "order", root="data/files/") -> list:
    """find in the -num- st data folders the files with good type (ie order or press) make a filter
    and retunr the list of files with usable paths"""

    # sanity check
    assert _type in ["press", "order", "complaint"]

    # list of data/*
    x_file_paths = os.listdir(root)[:num]

    # for each path, list dir and filter
    x_files_list = list()
    _ = [
        x_files_list.extend(
            [
                root + path_ + "/" + i
                for i in os.listdir(root + path_)
                if ((_type in i) and (".pdf" not in i))
            ]
        )
        for path_ in x_file_paths
    ]

    return x_files_list