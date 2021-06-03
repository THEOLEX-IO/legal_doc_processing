#! /bin/bash

# clean dist
rm dist/*
rm -rf dist/*

# make dist
python setup.py sdist

# push
twine upload -u $TWINE_USER -p $TWINE_PASSWORD dist/*



# docker run python:3.9-buster


# twine upload --repository testpypi dist/*
# python3 -m pip install --index-url https://test.pypi.org/simple/ your-package