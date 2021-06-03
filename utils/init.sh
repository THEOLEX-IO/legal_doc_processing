#! /bin/bash



# dowload collections
python -c "import nltk; import spacy; nltk.download('stopwords'); nltk.download('popular'); nlp = spacy.load('en_core_web_sm')"

# bootsrap all
python -c "from legal_doc_processing import LegalDoc; LegalDoc('hello world')"

