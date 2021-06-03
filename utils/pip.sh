#! /bin/bash

docker build --no-cache -f utils/Dockerfile.pip -t python3-pip:latest .

docker run -ti python3-pip:latest ipython
#  "from legal_doc_processing import LegalDoc; LegalDoc('hello world')"


