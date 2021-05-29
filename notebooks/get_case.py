import legal_doc_processing as ldp
from legal_doc_processing.information_extraction import *
from legal_doc_processing.segmentation import *
from legal_doc_processing.utils import *

from notebooks.packages import *
from notebooks.utils import *


if __name__ == "__main__":

    # file_path
    file_path_list = x_data_files(20, "order")

    # read file
    raw_text_list = [load_data(file_path) for file_path in file_path_list]
    raw_text_list[0]

    # clean and first
    clean_pages_list = [clean_doc(raw_text) for raw_text in raw_text_list]
    first_page_list = [pages[0] for pages in clean_pages_list]
    first_page_list[0]

    # pred case
    case_list = [get_case(fp) for fp in first_page_list]
    case_list

    # zip
    ziped = list(zip(file_path_list, case_list))
