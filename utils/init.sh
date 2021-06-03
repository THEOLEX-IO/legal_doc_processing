#! /bin/bash



# dowload collections
<<<<<<< HEAD
python -c "import nltk; import spacy; nltk.download('stopwords'); nltk.download('popular'); nlp = spacy.load('en_core_web_sm')"
=======
python -c "import nltk; import spacy; nltk.download('stopwords'); nltk.download('popular'); "
>>>>>>> release/v0.1.6.1

# bootsrap all
python -c "from legal_doc_processing import LegalDoc; LegalDoc('hello world')"

