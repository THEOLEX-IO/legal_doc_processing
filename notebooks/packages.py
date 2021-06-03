# builtin
import os
import sys
import dateparser
import string
import re
import urllib.request
import json
import glob
import heapq

# request and web parse
import requests

# import bs4 as bs

# data
import pandas as pd
import numpy as np

# from sklearn.feature_extraction.text import CountVectorizer

# nlp
import nltk
from nltk.tokenize import sent_tokenize
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer
from cleantext import clean
import spacy

# import textsplit
# from textsplit.tools import SimpleSentenceTokenizer
# from textsplit.tools import get_penalty, get_segments
# from textsplit.algorithm import split_optimal, split_greedy, get_total
import word2vec

# local packages
import legal_doc_processing as ldp
from legal_doc_processing.information_extraction import *
from legal_doc_processing.segmentation import *
from legal_doc_processing.utils import *

# bootstrap packages
# nltk.download("stopwords")
# nltk.download("popular")
# nlp = spacy.load("en_core_web_sm")
# get_ipython().run_line_magic("matplotlib", "inline")