import legal_doc_processing as ldp
from legal_doc_processing.information_extraction import *
from legal_doc_processing.segmentation import *
from legal_doc_processing.utils import *

from notebooks.packages import *
from notebooks.utils import *


# pipe
nlpipe = pipeline(
    "question-answering",
    model="distilbert-base-cased-distilled-squad",
    tokenizer="distilbert-base-cased",
)
if __name__ == "__main__":

    # file_path
    file_path_list = x_data_files(30, "order")

    # read file
    raw_text_list = [load_data(file_path) for file_path in file_path_list]
    raw_text_list[0]

    # clean and first
    clean_pages_list = [clean_doc(raw_text) for raw_text in raw_text_list]
    first_page_list = [pages[0] for pages in clean_pages_list]
    first_page_list[0]

    # clean first join
    joined_first_page_list = ["\n".join(first_page) for first_page in first_page_list]

    # # violated
    # violeted_ans_list = [
    #     nlpipe(question="Who violeted?", context=jfp, topk=3)
    #     for jfp in joined_first_page_list
    # ]
    # violeted_ans_list[:1]

    # violated_ans_peds = [preds[0].get("answer") for preds in violeted_ans_list]

    # defendant
    defendant_ans_list = [
        nlpipe(question="Who is the defendant?", context=jfp, topk=3)
        for jfp in joined_first_page_list
    ]
    defendant_ans_list[:1]

    defendant_ans_preds = [preds[0].get("answer") for preds in defendant_ans_list]

    # zip
    ziped = list(zip(file_path_list, defendant_ans_preds))
