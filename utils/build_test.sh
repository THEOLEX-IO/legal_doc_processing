#! /bin/bash

docker build --no-cache -f ./utils/Dockerfile -t asyoez/legal_doc_processing_repo:latest .
docker run -ti --entrypoint pytest asyoez/legal_doc_processing_repo:latest