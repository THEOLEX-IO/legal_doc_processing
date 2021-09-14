# import
import os
from collections import Counter

import requests

import pandas as pd

from legal_doc_processing.downloader.google import files
from legal_doc_processing.downloader.filters import (
    filter_juridiction,
    filter_ext,
    filter_press_release,
    select_best_file,
    handle_multiple_file_problem,
)
from legal_doc_processing.downloader.clean import clean_url
from legal_doc_processing.downloader.get import get_text
from legal_doc_processing.downloader.save import save_files


SOURCE = "cftc"


def first_example():
    """ """

    url = "https://storage.googleapis.com/theolex_documents_processing/cftc/text/7100-15/press-release.txt"
    req = requests.get(url)

    return req.text


def download_text_from_bucket(SOURCE, STOP=10):
    """ """

    # check args
    if SOURCE not in ["doj", "sec", "cftc", "cfbp"]:
        raise AssertionError

    # filters
    filter__txt = lambda i: filter_juridiction(filter_ext(i, "txt"), SOURCE)
    _txt = [i for i in files if filter__txt(i)]
    print(str(_txt[:3]) + "\n")
    # print(str(sec_txt[:3]) + "\n")

    # sep press release
    doc_list_ = [i for i in _txt if filter_press_release(i, False)]
    press_list_ = [i for i in _txt if filter_press_release(i, True)]
    print(doc_list_[:3])
    print(press_list_[:3])

    # pairs folder / url
    make_dict = lambda i: [i.split("/")[-2], i]
    #
    doc_pairs_ = [(i, j) for i, j in map(make_dict, doc_list_)]
    press_pairs_ = [(i, j) for i, j in map(make_dict, press_list_)]
    # check
    print(doc_pairs_[:5])
    print(press_pairs_[:5])

    # we have multiple 'legal doc' files for each folder complaint-allied-markets-llc-et-al.txt' and order-allied-markets-llc-et-al.txt
    # proof count folder
    # counts_before = Counter([i for i, j in doc_pairs_])
    # counts_before = [(i, j) for i, j in counts_before.items() if j > 1]
    # counts_before[:10]
    # do clean
    doc_pairs__cleaned = handle_multiple_file_problem(doc_pairs_)
    # proof count folder -> only unique
    # counts_after = Counter([i for i, j in doc_pairs__cleaned])
    # counts_after = [(i, j) for i, j in counts_after.items() if j > 1]
    # counts_after[:5]

    # make a dict of each
    doc_dict_ = {i: j for i, j in doc_pairs__cleaned}
    press_dict_ = {i: j for i, j in press_pairs_}

    print([(i, j) for i, j in doc_dict_.items()][:3])
    print([(i, j) for i, j in press_dict_.items()][:3])

    # build a df
    doc_df_dict_ = pd.DataFrame(
        [{"folder": i, "document_link": j} for i, j in doc_pairs__cleaned]
    )
    press_df_dict_ = pd.DataFrame(
        [{"folder": i, "press_release_link": j} for i, j in press_pairs_]
    )
    original_df = pd.merge(doc_df_dict_, press_df_dict_, how="outer", on="folder")
    sorted_df = original_df.sort_values("folder", axis=0, inplace=False)
    sorted_df.head(5)

    # clean url to have ok urls
    sorted_df["document_link_new"] = sorted_df.document_link.apply(clean_url)
    sorted_df["press_release_link_new"] = sorted_df.press_release_link.apply(clean_url)
    # check
    print(sorted_df.shape)
    print(sorted_df["document_link_new"].iloc[:5].values)
    print(sorted_df["press_release_link_new"].iloc[:5].values)
    sorted_df.head(5).T

    # keep ok url press link OR ok url doc link
    _idx = sorted_df.document_link_new.apply(
        bool
    ) + sorted_df.press_release_link_new.apply(bool)
    final_df = sorted_df.loc[_idx, :]
    final_df.head(5)

    # shuffle and reindex
    sample_df = final_df.sample(frac=1).reset_index(drop=True)

    # SOURCE
    sample_df["juridiction"] = SOURCE

    # SELECT
    if STOP > 0:
        sample_df = sample_df.iloc[:STOP, :]
    print(sample_df.shape)
    sample_df = sample_df.sort_values("folder", axis=0, inplace=False)

    # do download
    sample_df["legal_doc_text"] = sample_df.document_link_new.apply(get_text)
    sample_df["press_release_text"] = sample_df.press_release_link_new.apply(get_text)

    # # save
    # tmp_filename = f"{SOURCE}/data/csv/o00_{SOURCE}_text_from_bucket.csv"
    # sample_df.to_csv(tmp_filename, index=False)
    # sample_df = pd.read_csv(tmp_filename)

    # # save in files
    # sample_df["document_link_new"] = sample_df.document_link_new.fillna("")
    # sample_df["press_release_link_new"] = sample_df.press_release_link_new.fillna("")
    # save_files(sample_df, path=f"{SOURCE}/data/files/")


class Downloader:
    first_example = first_example