#!/bin/bash
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m nltk.downloader stopwords

echo "----------- create package using wheel -----------"  
python setup.py sdist bdist_wheel
echo "------------ package has been created -----------"

echo '-------- check package healthy ------------'
twine check dist/*
check-wheel-contents dist/legal_doc_processing*


echo -e "\033[0;32m-------  create virtual env to test package installation -----------"
python -m venv envtest
source env/bin/activate
echo -e "        \033[0;32m--------- try pip install wheel file -----------        "
pip  install dist/*.whl
deactivate
rm -rf envtest
