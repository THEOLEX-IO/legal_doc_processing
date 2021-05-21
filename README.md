[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![codecov](https://codecov.io/gh/THEOLEX-IO/legal_doc_processing/branch/master/graph/badge.svg)](https://codecov.io/gh/THEOLEX-IO/legal_doc_processing)
[![Build Status](https://travis-ci.org/mtchavez/python-package-boilerplate.png?branch=master)](https://travis-ci.org/mtchavez/python-package-boilerplate)
[![Requires.io](https://requires.io/github/mtchavez/python-package-boilerplate/requirements.svg?branch=master)](https://requires.io/github/mtchavez/python-package-boilerplate/requirements?branch=master)
[![DeepSource](https://deepsource.io/gh/THEOLEX-IO/legal_doc_processing.svg/?label=active+issues&show_trend=true)](https://deepsource.io/gh/THEOLEX-IO/legal_doc_processing/?ref=repository-badge)

## Requirements

Package requirements are handled using pip. To install them do

```
pip install -r requirements.txt
```

## Tests

Testing is set up using [pytest](http://pytest.org) and coverage is handled
with the pytest-cov plugin.

Run your tests with ```pytest``` in the root directory.

Coverage is ran by default and is set in the ```pytest.ini``` file.
To see an html output of coverage open ```htmlcov/index.html``` after running the tests.


## Pipe steps:  

Cleaning and feature engineering --> segmentation --> classification --> information extraction


## Usage:


```import legal_doc_processing as ldp```


### in case you have a text :
```ld = ldp.LegalDoc(your_text)```


### in case you have a filepath :
```ld = ldp.read_file(your_filepath)```


### make a prediction :
```case = ld.predict_case()```

```defendant = ld.defendant()```


### make all predictions
```preds = ld.predict_all()```


### after a predict_"feature" or after predict_all method you can find your predictions as attributes : 
```case = ld.case```
