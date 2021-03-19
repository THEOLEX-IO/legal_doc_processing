import re
from cleantext import clean


def is_section_num(text):
    return re.search(r'^[MDCLXVIAB]+\.$', text) is not None


def ends_with_ponc(text):
    punctuation = '!.?'
    return text[-1] in punctuation if text else False


def start_with_upper(text):
    return re.match('^[A-Z]', text) is not None


def is_title(text):
    uppers = [word.isupper() for word in text.split(" ")]
    return sum(uppers) / len(uppers) > 0.6


def same_sentence(sent1, sent2):
    # sent empty
    if (not sent1) or (not sent1['text']):
        return True
    # section number
    if sent1['is_section_num']:
        return True
    # very short sentence
    if len(sent1['text']) < 50:
        return False
    # ponctuation
    if sent1['ends_with_ponc']:
        return False
    if sent1['is_title']:
        return False
    if sent2['is_title']:
        return False
    return True


def clean_doc(file_text):
    pages = []
    for page in file_text.split("\x0c"):
        # clen text
        page_meta = [{'text': clean(para, lower=False, no_line_breaks=True).replace("_", "")}
                     for para in page.split('\n')]
        clean_page = []
        previous_line = {}
        text = ""
        # add meta data
        for line in page_meta:
            line['is_section_num'] = is_section_num(line['text'])
            line['is_title'] = is_title(line['text'])
            line['ends_with_ponc'] = ends_with_ponc(line['text'])
            line['is_alpha'] = sum(c.isalpha() for c in line['text'])
            line['start_with_upper'] = start_with_upper(line['text'])

            # not relevant line
            if not line['is_alpha']:
                continue

            if not same_sentence(previous_line, line):
                if text:
                    clean_page.append(text)
                    text = ""

            previous_line = line
            text = " ".join([text, line['text']])
        if len(clean_page):
            pages.append(clean_page)
    return pages
