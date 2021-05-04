import re


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

