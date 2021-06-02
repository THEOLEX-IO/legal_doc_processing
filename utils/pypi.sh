#! /bin/bash

# clean dist
rm dist/*
rm -rf dist/*

# make dist
python setup.py sdist

# push
twine upload -u TWINE_USER -p TWINE_PASSWORD dist/*