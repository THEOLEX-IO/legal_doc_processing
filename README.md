# Legal-doc-processing

[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![codecov](https://codecov.io/gh/THEOLEX-IO/legal_doc_processing/branch/master/graph/badge.svg)](https://codecov.io/gh/THEOLEX-IO/legal_doc_processing)
[![Build Status](https://travis-ci.org/mtchavez/python-package-boilerplate.png?branch=master)](https://travis-ci.org/mtchavez/python-package-boilerplate)
[![Requires.io](https://requires.io/github/mtchavez/python-package-boilerplate/requirements.svg?branch=master)](https://requires.io/github/mtchavez/python-package-boilerplate/requirements?branch=master)
[![DeepSource](https://deepsource.io/gh/THEOLEX-IO/legal_doc_processing.svg/?label=active+issues&show_trend=true)](https://deepsource.io/gh/THEOLEX-IO/legal_doc_processing/?ref=repository-badge)


## What is it ? 
-----------------------------------
<br>

**legal-doc-processing** is an open source NLP library dedicated to legal documents. It offers a large and various tools to analyse, structure and extract information from legal documents surch as orders, complaints, press release etc etc.
<br>
<br>

## Installation
-------------------------------------
<br>

go in your project directory and activate virtual environnement
```
cd my-project/
python3 -m venv env
source ./env/bin/activate
```

then install with pypi
```
pip install legal-doc-processing
```

or install with git 
```
git clone https://github.com/THEOLEX-IO/legal_doc_processing.git
pip install -r requirements.txt
```

at frist usage please write following command to bootstrap the package
```
python -c "from legal_doc_processing import boot; boot()"
```
this command will download data collections and mandory web assets, it can take 1/2 minutes (depends of your web  connection)
<br>
<br>

## Usage
----------------------------------------------------
<br>

There is 2 main modules in legal-doc-processing : 
- ld for LegalDoc objects ie order, complaint, etc etc official documents
- pr for PressRelease objects for legal press release related to each case

so you can 
```
from legal_doc_processing import *  # import all
from legal_doc_processing import ld # import legal document module
from legal_doc_processing import pr # import press release module
```
<br>

### Instanciation
youn can init an object in 2 ways.
* with text directly
```
from legal_doc_processing import ld
doc = ld.LegalDoc("this is a document")
```
* with path to a file
```
doc = ld.read_LegalDoc("this/is/my/file.txt")
```

for press release, same pattern: 
```
from legal_doc_processing import pr
press = ld.PressRelease("this is a press release")
```
* with path to a file
```
press = ld.read_PressRelease("this/is/my/file.txt")
```

once instanciated, you can print : 
```
print(doc)
```
<br>

all interessing features are in feature_dict attribute
```
print(doc.feature_dict)
```
<br>

### Predictions

you can now make predictions : 
```
defendant = doc.predict("defendant")
print(defendant)
case = doc.predict("case")
print(case)
```
<br>

predict method return a something but alson work on the object itself : 
```
print(doc)
print(doc.feature_dict)
```
<br>

of course most easy is to predict all : 
```
features = doc.predict("all")
print(features)
print(doc)
print(doc.feature_dict)
```
<br>
<br>

## Requirements
-----------------------------------------------------
<br>

Package requirements are handled using pip. To install them do
```
pip install -r requirements.txt
```
<br>
<br>

## Tests
---------------------------------------------------------
<br>

Testing is set up using [pytest](http://pytest.org) and coverage is handled
with the pytest-cov plugin.

Run your tests with ```pytest``` in the root directory.

Coverage is ran by default and is set in the ```pytest.ini``` file.
To see an html output of coverage open ```htmlcov/index.html``` after running the tests.
<br>
<br>

## Pipe steps:  
-----------------------------------
<br>

Cleaning and feature engineering --> segmentation --> classification --> information extraction
<br>
<br>

## Licence:  
-----------------------------------
<br>

lorem ipsum
<br>
<br>

## Getting Help and discussion:  
-----------------------------------
<br>

lorem ipsum
<br>
<br>


## Contributing:  
-----------------------------------
<br>
lorem ipsum
<br>
<br>

## Documentation:  
-----------------------------------
lorem ipsum
<br>
<br>
