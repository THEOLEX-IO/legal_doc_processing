#!/bin/bash

pip install check-wheel-contents
pip install wheel-inspect

echo "----------- create package using wheel ------------"  
python setup.py bdist_wheel
echo "------------ package has been created -----------"

echo '-------- check package healthy ------------'
check-wheel-contents dist/legal_doc_processing*

echo "json file presentation for the library"
wheel2json dist/legal_doc_processing*

echo "--------- try pip install wheel file -----------"
pip  install dist/legal_doc_processing*