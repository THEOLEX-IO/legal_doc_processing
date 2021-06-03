#! /bin/bash

# clean dist
rm dist/*
rm -rf dist/*

# make dist
python setup.py sdist

# push
twine upload -u $TWINE_USER -p $TWINE_PASSWORD dist/*



# instructions
# docker run -ti python:3.9-buster /bin/bash 
# pip install ipython legal-doc-processing==0.1.6.4

# ipython 
# from legal_doc_processing import boot
# boot()

# TESTPypu
# twine upload --repository testpypi dist/*
# python3 -m pip install --index-url https://test.pypi.org/simple/ your-package