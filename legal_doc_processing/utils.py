import re
import heapq

import nltk

from cleantext import clean


stopwords = nltk.corpus.stopwords.words("english")


def hello():
    """dummy  """

    return "world"


def load_data(file_path: str) -> str:
    """from file_path open read and return text; return text """

    with open(file_path) as f:
        txt = f.read()

    return txt


def clean_spec_chars(text: str) -> tuple:
    """first text cleaning based on regex, just keep text not spec chars
    return tupple of text"""

    # article text
    article_text = re.sub(r"\[[0-9]*\]", " ", text)
    article_text = re.sub(r"\s+", " ", article_text)

    # formated text
    formatted_article_text = re.sub("[^a-zA-Z]", " ", article_text)
    formatted_article_text = re.sub(r"\s+", " ", formatted_article_text)

    return article_text, formatted_article_text


# def handle_encoding(text: str) -> str:
#     """handle encoding problems and force ascii conversion ; return clean text """

#     # encoding the text to ASCII format
#     text_encode = text.encode(encoding="ascii", errors="ignore")

#     # decoding the text
#     text_decode = text_encode.decode()

#     # cleaning the text to remove extra whitespace
#     clean_text = " ".join([word for word in text_decode.split()])

#     return clean_text


def is_section_num(text: str) -> bool:
    """detect if a paragrath start with Roman letter ie is a section; return bool """

    return re.search(r"^[MDCLXVIAB]+\.$", text) is not None


def ends_with_ponc(text: str, punctuation: str = "!.?") -> bool:
    """detect if a text finsih with punctation end of sentence; return bool"""

    return text[-1] in punctuation if text else False


def starts_with_upper(text: str) -> bool:
    """fist letter of a text is upper; return bool"""

    return re.match("^[A-Z]", text) is not None


def is_title(text: str, threshold=0.6) -> bool:
    """detect if text is a title if threshold % of the letters are upper; return bool """

    uppers = [word.isupper() for word in text.split(" ")]

    return sum(uppers) / len(uppers) > threshold


def same_sentence(sent1, sent2):
    # print(sent1,"\n",sent2)

    # sent empty
    if (not sent1) or (not sent1["text"]):
        return True
    # section number
    if sent1["is_section_num"]:
        return True

    # very short sentence
    if len(sent1["text"]) < 50:
        return False

    # ponctuation
    if sent1["ends_with_ponc"]:
        return False

    if sent1["is_title"]:
        return False

    if sent2["is_title"]:
        return False

    return True


def get_token(text):
    sentence_list = nltk.sent_tokenize(text)
    sentence_list
    return sentence_list

def get_section_indx(list_token):

    idx=[]
    for i in range(len(list_token)):
        if is_title(list_token[i]):
            idx.append(i)
            
    return idx

def get_structure(text):     
    list_token=get_token(text)
    idx=get_section_indx(list_token)
    j=0
    structure=[]
    k=0
    for i in idx:
        section={}
        section['content']=list_token[j:i+1]
        section['header']=list_token[i]
        section['id']=k
        structure.append(section)
        j=i+1
        k=k+1
        
    return structure
    def get_header(section):
        sec0="".join(section[0]['content'])
        sec1="".join(section[1]['content'])
        entete=[sec0]
        entete.append(sec1)
        header="".join(entete)
        return header

def clean_doc(
    file_text,
):
    """ """

    pages = []
    for page in file_text.split("\x0c"):

        # clen text
        page_meta = [{"text": clean(para)} for para in page.split("\n")]
        clean_page = []
        previous_line = {}
        text = ""

        # add meta data
        for line in page_meta:
            line["is_section_num"] = is_section_num(str(line["text"]))
            line["is_title"] = is_title(str(line["text"]))
            line["ends_with_ponc"] = ends_with_ponc(str(line["text"]))
            line["is_alpha"] = sum(c.isalpha() for c in str(line["text"]))
            line["start_with_upper"] = starts_with_upper(str(line["text"]))

            # not relevant line
            if not line["is_alpha"]:
                continue

            if not same_sentence(previous_line, line):
                if text:
                    clean_page.append(text)
                    text = ""

            previous_line = line
            text = " ".join([text, str(line["text"])])

        if len(clean_page):
            pages.append(clean_page)

    return pages




def word_frequency(text):
    stopwords = nltk.corpus.stopwords.words('english')
    word_frequencies = {}
    for word in nltk.word_tokenize(text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    return word_frequencies


def sentence_score(sentence_list, word_frequencies):
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(" ")) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    return sentence_scores
