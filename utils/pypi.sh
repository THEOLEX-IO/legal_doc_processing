#! /bin/bash

# clean dist

sudo rm -rf dist

# make dist
# python setup.py sdist
./utils/create_package.sh

# push
twine upload -u $TWINE_USER -p $TWINE_PASSWORD dist/*

# instructions
# docker run -ti python:3.9-buster /bin/bash 
# pip install ipython legal-doc-processing==2.1.4

# ipython 
# from legal_doc_processing import boot ; boot()

# TESTPypu
# twine upload -u $TWINE_USER -p $TWINE_PASSWORD --repository testpypi dist/*
# python3 -m pip install --index-url https://test.pypi.org/simple/ your-package