#! /bin/bash



# dowload collections
python -c "import nltk; import spacy; nltk.download('stopwords'); nltk.download('popular'); "

# bootsrap all
python -c "from legal_doc_processing import LegalDoc; LegalDoc('hello world')"

