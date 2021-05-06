#!/bin/bash

pip install check-wheel-contents

echo "----------- create package using wheel ------------"  
python setup.py bdist_wheel
echo "------------ package has been created -----------"

echo '-------- check package healthy ------------'
check-wheel-contents dist/theolex_document_processing*

echo "--------- try pip install wheel file -----------"
pip  install dist/theolex_document_processing*