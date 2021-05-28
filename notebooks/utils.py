import os


def clean_data_folder():
    """read all data/*/*, delete .pdf, keep only .txt """

    folders = os.listdir("data/")
    all_files = list()

    _ = [
        all_files.extend([f"data/{fold}/{fi}" for fi in os.listdir(f"data/{fold}")])
        for fold in folders
    ]

    # files
    not_text = [i for i in all_files if ".txt" not in i]
    only_text = [i for i in all_files if ".txt" in i]

    # remove not .txt
    _ = [os.remove(i) for i in not_text]


def find_files_type():
    """ """

    # all files
    folders = os.listdir("data/")
    all_files = list()

    _ = [
        all_files.extend([f"data/{fold}/{fi}" for fi in os.listdir(f"data/{fold}")])
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
