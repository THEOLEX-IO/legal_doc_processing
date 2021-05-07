from cleantext import clean
from legal_doc_processing import utils


def clean_doc(file_text):
    pages = []

    for page in file_text.split("\x0c"):
        # clean text
        page_meta = [{'text': clean(para)}
                     for para in page.split('\n')]
        clean_page = []
        previous_line = {}
        text = ""
        # add meta data
        for line in page_meta:
            line['is_section_num'] = utils.is_section_num(str(line['text']))
            line['is_title'] = utils.is_title(str(line['text']))
            line['ends_with_ponc'] = utils.ends_with_ponc(str(line['text']))
            line['is_alpha'] = sum(c.isalpha() for c in str(line['text']))
            line['start_with_upper'] = utils.start_with_upper(str(line['text']))

            # not relevant line
            if not line['is_alpha']:
                continue
            if not utils.same_sentence(previous_line, line):
                # if text:
                clean_page.append(text)
                text = ""
            previous_line = line
            text = " ".join([text, str(line['text'])])
        if clean_page:
            pages.append(clean_page)
    return pages

    # generate documents with headers and paragraphs
    def get_structured_document(file_text):
        return file_text # [{"header": "INTRODUCTION", "content": "The Commodity Futures Trading Commission...","id":1},...]