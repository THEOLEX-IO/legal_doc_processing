#!/usr/bin/env python
# coding: utf-8

# ## 1 - INTRO
# --------------------

# ### 1.1 - import builtin packages


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


# ### 1.2 - import external packages

# request and web parse
import requests
import bs4 as bs

# data
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

# nlp
import nltk
from nltk.tokenize import sent_tokenize
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer
from cleantext import clean
import spacy
import textsplit
from textsplit.tools import SimpleSentenceTokenizer
from textsplit.tools import get_penalty, get_segments
from textsplit.algorithm import split_optimal, split_greedy, get_total
import word2vec


# ### 1.3 - Import local packages


import legal_doc_processing as ldp
from legal_doc_processing.information_extraction import *
from legal_doc_processing.segmentation import *
from legal_doc_processing.utils import *


# ### 1.4 - Bootstrap packages


nltk.download("popular")
nlp = spacy.load("en_core_web_sm")
get_ipython().run_line_magic("matplotlib", "inline")


# ### 1.5 paths

from notebooks.paths import *


# ## 2 - GET CASE
# --------------------
from notebooks.get_case import *


# ## 3 - GET DEFENDANT
# --------------------
from notebooks.get_defendant import *
