import legal_doc_processing as ldp
from legal_doc_processing.information_extraction import *
from legal_doc_processing.segmentation import *
from legal_doc_processing.utils import *

from notebooks.packages import *
from notebooks.paths import *

# ## 2 - Defendant
# -------------------------------------

# ### 2.1 - One file


# read file
raw_text = load_data(one_file_path)
raw_text[:300]


# clean first join
clean_pages = clean_doc(raw_text)
first_page = clean_pages[0]
joined_first_page = "\n".join(first_page)


# Process whole documents
doc = nlp(joined_first_page)


# Analyze syntax
# print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
# print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

# Find named entities, phrases and concepts
for entity in doc.ents:
    if entity.label_ == "ORG":
        #  print(entity.text,":       ", entity.label_)
        print(f"{entity.text[:30].ljust(40)} :  {entity.label_} ")


# Question answering pipeline, specifying the checkpoint identifier
nlpipe = pipeline(
    "question-answering",
    model="distilbert-base-cased-distilled-squad",
    tokenizer="distilbert-base-cased",
)


first_page_100 = [text for text in first_page if len(text) > 100]
first_page_100[:10]


violeted_ans = nlpipe(question="Who violeted?", context=".".join(first_page_100), topk=3)
violeted_ans


defendant_ans = nlpipe(
    question="Who is the defendant?", context=".".join(first_page_100), topk=3
)
defendant_ans[:3]


# # STOP HERE


DEPRECATED = """
import spacy

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

# Process whole documents
text = "\n".join(first_page)
doc = nlp(text)

# Analyze syntax
# print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
# print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

# Find named entities, phrases and concepts
for entity in doc.ents:
    if entity.label_ == "ORG":
        print(entity.text, ":       ", entity.label_)


# print("\n".join(first_page))


# In[19]:


from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer

# Question answering pipeline, specifying the checkpoint identifier
nlp = pipeline(
    "question-answering",
    model="distilbert-base-cased-distilled-squad",
    tokenizer="distilbert-base-cased",
)

first_page_100 = [text for text in first_page if len(text) > 100]


# In[20]:


# first_page_100

print(nlp(question="Who violeted?", context=".".join(first_page_100)))

print(nlp(question="Who is the defendant?", context=".".join(first_page_100), topk=3))
"""
