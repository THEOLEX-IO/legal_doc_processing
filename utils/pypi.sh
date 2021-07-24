#! /bin/bash

##################################################
#   How To Deploy on Pypi
##################################################


# clean dist
sudo rm -rf dist build legal_doc_processing.egg-info

# test readme
twine check dist/*

# make dist
./utils/create_package.sh

# push
twine upload -u $TWINE_USER -p $TWINE_PASSWORD dist/*

# test
# docker run -ti python:3.9-buster /bin/bash 
# pip install ipython legal-doc-processing==2.2.2
# ipython 
# from legal_doc_processing import boot ; boot()

# TESTPypu
# twine upload -u $TWINE_USER -p $TWINE_PASSWORD --repository testpypi dist/*
# python3 -m pip install --index-url https://test.pypi.org/simple/ your-package